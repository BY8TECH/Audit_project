"""Reconciliation service - compare data between sources and find mismatches."""

from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
import uuid

from app.core.database import mongodb
from app.schemas.reconciliation import (
    ReconciliationRequest,
    ReconciliationResult,
    MismatchItem,
    ReconciliationReport,
)


class ReconciliationService:
    """Service for data reconciliation between platforms."""

    @staticmethod
    async def compare_sources(
        user_id: str, request: ReconciliationRequest
    ) -> ReconciliationResult:
        """Compare data between two sources and identify mismatches."""
        financial_data = mongodb.get_collection("financial_data")

        # Fetch data from source A
        source_a_cursor = financial_data.find({
            "user_id": user_id,
            "source_platform": request.source_a_platform,
            "data_type": request.data_type,
        })
        source_a_data = await source_a_cursor.to_list(1000)

        # Fetch data from source B
        source_b_cursor = financial_data.find({
            "user_id": user_id,
            "source_platform": request.source_b_platform,
            "data_type": request.data_type,
        })
        source_b_data = await source_b_cursor.to_list(1000)

        # Build lookup dicts based on match criteria
        mismatches: List[MismatchItem] = []
        matched = 0
        missing_in_a = 0
        missing_in_b = 0
        total_difference = 0.0

        if request.match_by == "reference_number":
            mismatches, matched, missing_in_a, missing_in_b, total_difference = (
                ReconciliationService._match_by_reference(
                    source_a_data, source_b_data, request.tolerance_amount
                )
            )
        elif request.match_by == "amount_date":
            mismatches, matched, missing_in_a, missing_in_b, total_difference = (
                ReconciliationService._match_by_amount_date(
                    source_a_data, source_b_data, request.tolerance_amount
                )
            )
        else:  # party_name
            mismatches, matched, missing_in_a, missing_in_b, total_difference = (
                ReconciliationService._match_by_party(
                    source_a_data, source_b_data, request.tolerance_amount
                )
            )

        total_a = len(source_a_data)
        total_b = len(source_b_data)
        total_compared = max(total_a, total_b)
        match_pct = round((matched / total_compared * 100), 2) if total_compared > 0 else 0

        result_id = str(uuid.uuid4())

        result = ReconciliationResult(
            id=result_id,
            source_a_platform=request.source_a_platform,
            source_b_platform=request.source_b_platform,
            data_type=request.data_type,
            run_at=datetime.now(timezone.utc),
            status="completed",
            total_source_a=total_a,
            total_source_b=total_b,
            matched=matched,
            mismatched=len(mismatches),
            missing_in_a=missing_in_a,
            missing_in_b=missing_in_b,
            match_percentage=match_pct,
            total_difference_amount=round(total_difference, 2),
            mismatches=mismatches,
            summary={
                "source_a_total_amount": sum(d.get("total_amount", 0) for d in source_a_data),
                "source_b_total_amount": sum(d.get("total_amount", 0) for d in source_b_data),
                "tolerance_used": request.tolerance_amount,
                "match_criteria": request.match_by,
            },
        )

        # Save result to database
        reconciliations = mongodb.get_collection("reconciliations")
        await reconciliations.insert_one({
            "result_id": result_id,
            "user_id": user_id,
            **result.model_dump(),
        })

        # Log audit
        audit_logs = mongodb.get_collection("audit_logs")
        await audit_logs.insert_one({
            "user_id": user_id,
            "action": "run_reconciliation",
            "resource_type": "reconciliation",
            "resource_id": result_id,
            "details": {
                "source_a": request.source_a_platform,
                "source_b": request.source_b_platform,
                "matched": matched,
                "mismatched": len(mismatches),
            },
            "status": "success",
            "timestamp": datetime.now(timezone.utc),
        })

        return result

    @staticmethod
    def _match_by_reference(
        source_a: List[Dict], source_b: List[Dict], tolerance: float
    ) -> tuple:
        """Match records by reference number."""
        mismatches = []
        matched = 0
        missing_in_b = 0
        total_diff = 0.0

        b_by_ref = {}
        for item in source_b:
            ref = item.get("reference_number", "")
            if ref:
                b_by_ref[ref] = item

        matched_b_refs = set()

        for a_item in source_a:
            ref = a_item.get("reference_number", "")
            if not ref:
                continue

            if ref in b_by_ref:
                b_item = b_by_ref[ref]
                matched_b_refs.add(ref)
                a_amount = a_item.get("total_amount", 0)
                b_amount = b_item.get("total_amount", 0)
                diff = abs(a_amount - b_amount)

                if diff > tolerance:
                    mismatches.append(MismatchItem(
                        mismatch_type="amount_mismatch",
                        reference_number=ref,
                        party_name=a_item.get("party_name"),
                        source_a_amount=a_amount,
                        source_b_amount=b_amount,
                        difference=round(diff, 2),
                        source_a_date=a_item.get("date"),
                        source_b_date=b_item.get("date"),
                        source_a_id=str(a_item.get("_id", "")),
                        source_b_id=str(b_item.get("_id", "")),
                        severity="high" if diff > 10000 else ("medium" if diff > 1000 else "low"),
                        details={"tolerance": tolerance},
                    ))
                    total_diff += diff
                else:
                    matched += 1
            else:
                missing_in_b += 1
                mismatches.append(MismatchItem(
                    mismatch_type="missing_in_b",
                    reference_number=ref,
                    party_name=a_item.get("party_name"),
                    source_a_amount=a_item.get("total_amount", 0),
                    source_a_date=a_item.get("date"),
                    source_a_id=str(a_item.get("_id", "")),
                    severity="high",
                ))

        # Find items in B not in A
        missing_in_a = 0
        for ref, b_item in b_by_ref.items():
            if ref not in matched_b_refs:
                a_has_ref = any(a.get("reference_number") == ref for a in source_a)
                if not a_has_ref:
                    missing_in_a += 1
                    mismatches.append(MismatchItem(
                        mismatch_type="missing_in_a",
                        reference_number=ref,
                        party_name=b_item.get("party_name"),
                        source_b_amount=b_item.get("total_amount", 0),
                        source_b_date=b_item.get("date"),
                        source_b_id=str(b_item.get("_id", "")),
                        severity="high",
                    ))

        return mismatches, matched, missing_in_a, missing_in_b, total_diff

    @staticmethod
    def _match_by_amount_date(
        source_a: List[Dict], source_b: List[Dict], tolerance: float
    ) -> tuple:
        """Match records by amount and date proximity."""
        mismatches = []
        matched = 0
        total_diff = 0.0
        used_b_indices = set()

        for a_item in source_a:
            a_amount = a_item.get("total_amount", 0)
            a_date = a_item.get("date")
            found_match = False

            for idx, b_item in enumerate(source_b):
                if idx in used_b_indices:
                    continue
                b_amount = b_item.get("total_amount", 0)
                if abs(a_amount - b_amount) <= tolerance:
                    matched += 1
                    used_b_indices.add(idx)
                    found_match = True
                    break

            if not found_match:
                mismatches.append(MismatchItem(
                    mismatch_type="missing_in_b",
                    reference_number=a_item.get("reference_number"),
                    party_name=a_item.get("party_name"),
                    source_a_amount=a_amount,
                    source_a_date=a_date,
                    severity="medium",
                ))

        missing_in_a = len(source_b) - len(used_b_indices)
        missing_in_b = len(source_a) - matched

        for idx, b_item in enumerate(source_b):
            if idx not in used_b_indices:
                mismatches.append(MismatchItem(
                    mismatch_type="missing_in_a",
                    reference_number=b_item.get("reference_number"),
                    party_name=b_item.get("party_name"),
                    source_b_amount=b_item.get("total_amount", 0),
                    source_b_date=b_item.get("date"),
                    severity="medium",
                ))

        return mismatches, matched, missing_in_a, missing_in_b, total_diff

    @staticmethod
    def _match_by_party(
        source_a: List[Dict], source_b: List[Dict], tolerance: float
    ) -> tuple:
        """Match records by party name and aggregate amounts."""
        mismatches = []
        matched = 0
        total_diff = 0.0

        # Aggregate by party name
        a_by_party: Dict[str, float] = {}
        for item in source_a:
            name = (item.get("party_name") or "").strip().lower()
            if name:
                a_by_party[name] = a_by_party.get(name, 0) + item.get("total_amount", 0)

        b_by_party: Dict[str, float] = {}
        for item in source_b:
            name = (item.get("party_name") or "").strip().lower()
            if name:
                b_by_party[name] = b_by_party.get(name, 0) + item.get("total_amount", 0)

        all_parties = set(list(a_by_party.keys()) + list(b_by_party.keys()))
        missing_in_a = 0
        missing_in_b = 0

        for party in all_parties:
            a_amt = a_by_party.get(party, 0)
            b_amt = b_by_party.get(party, 0)

            if party not in a_by_party:
                missing_in_a += 1
                mismatches.append(MismatchItem(
                    mismatch_type="missing_in_a",
                    party_name=party.title(),
                    source_b_amount=b_amt,
                    severity="high",
                ))
            elif party not in b_by_party:
                missing_in_b += 1
                mismatches.append(MismatchItem(
                    mismatch_type="missing_in_b",
                    party_name=party.title(),
                    source_a_amount=a_amt,
                    severity="high",
                ))
            elif abs(a_amt - b_amt) > tolerance:
                diff = abs(a_amt - b_amt)
                total_diff += diff
                mismatches.append(MismatchItem(
                    mismatch_type="amount_mismatch",
                    party_name=party.title(),
                    source_a_amount=a_amt,
                    source_b_amount=b_amt,
                    difference=round(diff, 2),
                    severity="high" if diff > 50000 else "medium",
                ))
            else:
                matched += 1

        return mismatches, matched, missing_in_a, missing_in_b, total_diff

    @staticmethod
    async def get_mismatches(
        user_id: str, reconciliation_id: Optional[str] = None
    ) -> List[MismatchItem]:
        """Get mismatches from a reconciliation run."""
        reconciliations = mongodb.get_collection("reconciliations")

        query: Dict[str, Any] = {"user_id": user_id}
        if reconciliation_id:
            query["result_id"] = reconciliation_id

        result = await reconciliations.find_one(query, sort=[("run_at", -1)])
        if not result:
            return []

        return [MismatchItem(**m) for m in result.get("mismatches", [])]

    @staticmethod
    async def generate_report(
        user_id: str, reconciliation_id: str
    ) -> ReconciliationReport:
        """Generate a detailed reconciliation report."""
        reconciliations = mongodb.get_collection("reconciliations")
        result_doc = await reconciliations.find_one({
            "user_id": user_id,
            "result_id": reconciliation_id,
        })

        if not result_doc:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reconciliation result not found",
            )

        # Remove MongoDB _id for serialization
        result_doc.pop("_id", None)
        result_doc.pop("user_id", None)

        result = ReconciliationResult(**result_doc)

        # Generate recommendations
        recommendations = []
        if result.missing_in_a > 0:
            recommendations.append(
                f"Found {result.missing_in_a} records in {result.source_b_platform} "
                f"missing from {result.source_a_platform}. Verify these entries."
            )
        if result.missing_in_b > 0:
            recommendations.append(
                f"Found {result.missing_in_b} records in {result.source_a_platform} "
                f"missing from {result.source_b_platform}. Cross-check with source."
            )
        if result.total_difference_amount > 0:
            recommendations.append(
                f"Total amount difference of ₹{result.total_difference_amount:,.2f} detected. "
                f"Review individual mismatches for correction."
            )
        if result.match_percentage >= 95:
            recommendations.append("High match rate — data appears consistent across sources.")
        elif result.match_percentage >= 80:
            recommendations.append("Moderate match rate — some discrepancies need investigation.")
        else:
            recommendations.append("Low match rate — significant data discrepancies detected. Immediate review recommended.")

        return ReconciliationReport(
            result=result,
            recommendations=recommendations,
            generated_at=datetime.now(timezone.utc),
        )
