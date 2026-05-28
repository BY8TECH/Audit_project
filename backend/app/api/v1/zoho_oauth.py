from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
import httpx
from datetime import datetime, timezone
from app.core.security import get_current_user
from app.core.database import mongodb
from app.core.config import settings

router = APIRouter()

class ZohoOAuthCallbackRequest(BaseModel):
    code: str
    location: str  # e.g., 'in' or 'com'
    org_id: str

@router.post("/callback", status_code=status.HTTP_200_OK)
async def zoho_oauth_callback(
    request: ZohoOAuthCallbackRequest,
    current_user: dict = Depends(get_current_user),
):
    """Handle Zoho OAuth callback by exchanging the authorization code for tokens."""
    
    # We must require client_id and secret to be configured centrally
    if not settings.ZOHO_CLIENT_ID or not settings.ZOHO_CLIENT_SECRET:
        raise HTTPException(
            status_code=500, 
            detail="Zoho OAuth credentials are not configured on the server."
        )
        
    domain = request.location
    if domain not in ['in', 'com', 'eu', 'au']:
        domain = 'in'
        
    token_url = f"https://accounts.zoho.{domain}/oauth/v2/token"
    
    data = {
        "grant_type": "authorization_code",
        "client_id": settings.ZOHO_CLIENT_ID,
        "client_secret": settings.ZOHO_CLIENT_SECRET,
        "redirect_uri": settings.ZOHO_REDIRECT_URI,
        "code": request.code
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=data)
        
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail=f"Failed to exchange token: {response.text}")
            
        json_data = response.json()
        if "error" in json_data:
            raise HTTPException(status_code=400, detail=f"Zoho error: {json_data['error']}")
            
        access_token = json_data.get("access_token")
        refresh_token = json_data.get("refresh_token")
        
        if not refresh_token:
            raise HTTPException(status_code=400, detail="Did not receive refresh_token. Ensure access_type=offline was passed.")
            
        # Store in connections collection
        connections = mongodb.get_collection("connections")
        now = datetime.now(timezone.utc)
        
        # Upsert connection
        conn_doc = {
            "user_id": current_user["id"],
            "platform": "zoho_books",
            "display_name": f"Zoho Books Org: {request.org_id}",
            "status": "connected",
            "config": {},
            "credentials": {
                "refresh_token": refresh_token,
                "org_id": request.org_id,
                "location": domain
            },
            "last_sync_at": None,
            "last_sync_status": None,
            "sync_frequency_minutes": 60,
            "records_synced": 0,
            "error_message": None,
            "is_active": True,
            "updated_at": now,
        }
        
        # Check if exists
        existing = await connections.find_one({"user_id": current_user["id"], "platform": "zoho_books"})
        if existing:
            await connections.update_one({"_id": existing["_id"]}, {"$set": conn_doc})
        else:
            conn_doc["created_at"] = now
            await connections.insert_one(conn_doc)
            
        return {"success": True, "message": "Successfully connected Zoho Books!"}
