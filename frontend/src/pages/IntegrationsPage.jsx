import { useState, useCallback } from 'react';
import {
  Puzzle,
  ExternalLink,
  Check,
  Info,
  ChevronDown,
  ChevronUp,
  Database,
  FileText,
  RefreshCw,
  Eye,
} from 'lucide-react';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import StatusBadge from '../components/ui/StatusBadge';
import Modal from '../components/ui/Modal';
import Loader from '../components/ui/Loader';
import DataTable from '../components/ui/DataTable';
import { useFetch } from '../hooks/useFetch';
import { integrationApi } from '../api/integrationApi';
import { PLATFORM_LIST, PLATFORMS } from '../utils/constants';
import { formatCurrency, formatDate } from '../utils/formatters';

const demoPreviewData = {
  zoho_books: [
    { id: 'INV-001', date: '2026-05-15', description: 'Website Development', amount: 245000, status: 'paid' },
    { id: 'INV-002', date: '2026-05-12', description: 'Consulting Services', amount: 180000, status: 'pending' },
    { id: 'INV-003', date: '2026-05-10', description: 'Annual Maintenance', amount: 95000, status: 'paid' },
    { id: 'INV-004', date: '2026-05-08', description: 'Cloud Services', amount: 65000, status: 'overdue' },
    { id: 'INV-005', date: '2026-05-05', description: 'Training Program', amount: 120000, status: 'paid' },
  ],
  tally: [
    { id: 'VCH-001', date: '2026-05-15', ledger: 'Sales Account', debit: 0, credit: 245000, narration: 'Sales invoice' },
    { id: 'VCH-002', date: '2026-05-14', ledger: 'Rent Account', debit: 120000, credit: 0, narration: 'Office rent' },
    { id: 'VCH-003', date: '2026-05-13', ledger: 'Salary Account', debit: 450000, credit: 0, narration: 'May payroll' },
  ],
  gst_portal: [
    { id: 'GSTR1-2026-04', period: 'Apr 2026', type: 'GSTR-1', status: 'Filed', taxable_value: 1850000, tax: 333000 },
    { id: 'GSTR3B-2026-04', period: 'Apr 2026', type: 'GSTR-3B', status: 'Filed', taxable_value: 1850000, tax: 333000 },
    { id: 'GSTR1-2026-03', period: 'Mar 2026', type: 'GSTR-1', status: 'Filed', taxable_value: 2100000, tax: 378000 },
  ],
  income_tax: [
    { id: 'AY-2026-27', assessment_year: 'AY 2026-27', form: 'ITR-3', status: 'Not Filed', due_date: '2026-07-31' },
    { id: 'AY-2025-26', assessment_year: 'AY 2025-26', form: 'ITR-3', status: 'Filed', due_date: '2025-07-31' },
  ],
};

const previewColumns = {
  zoho_books: [
    { key: 'id', label: 'Invoice ID', render: (val) => <span className="font-medium text-brand-cyan">{val}</span> },
    { key: 'date', label: 'Date', render: (val) => formatDate(val) },
    { key: 'description', label: 'Description' },
    { key: 'amount', label: 'Amount', align: 'right', render: (val) => formatCurrency(val) },
    {
      key: 'status', label: 'Status', render: (val) => (
        <StatusBadge
          status={val === 'paid' ? 'connected' : val === 'pending' ? 'syncing' : 'error'}
          label={val}
          size="sm"
        />
      ),
    },
  ],
  tally: [
    { key: 'id', label: 'Voucher', render: (val) => <span className="font-medium text-brand-cyan">{val}</span> },
    { key: 'date', label: 'Date', render: (val) => formatDate(val) },
    { key: 'ledger', label: 'Ledger' },
    { key: 'debit', label: 'Debit', align: 'right', render: (val) => val ? formatCurrency(val) : '—' },
    { key: 'credit', label: 'Credit', align: 'right', render: (val) => val ? formatCurrency(val) : '—' },
    { key: 'narration', label: 'Narration' },
  ],
  gst_portal: [
    { key: 'id', label: 'ID', render: (val) => <span className="font-medium text-brand-cyan">{val}</span> },
    { key: 'period', label: 'Period' },
    { key: 'type', label: 'Return Type' },
    { key: 'taxable_value', label: 'Taxable Value', align: 'right', render: (val) => formatCurrency(val) },
    { key: 'tax', label: 'Tax Amount', align: 'right', render: (val) => formatCurrency(val) },
    { key: 'status', label: 'Status', render: (val) => <StatusBadge status={val === 'Filed' ? 'connected' : 'syncing'} label={val} size="sm" /> },
  ],
  income_tax: [
    { key: 'assessment_year', label: 'Assessment Year' },
    { key: 'form', label: 'Form' },
    { key: 'due_date', label: 'Due Date', render: (val) => formatDate(val) },
    { key: 'status', label: 'Status', render: (val) => <StatusBadge status={val === 'Filed' ? 'connected' : 'error'} label={val} size="sm" /> },
  ],
};

export default function IntegrationsPage() {
  const [expandedPlatform, setExpandedPlatform] = useState(null);
  const [previewPlatform, setPreviewPlatform] = useState(null);
  const [previewData, setPreviewData] = useState(null);
  const [previewLoading, setPreviewLoading] = useState(false);

  const toggleExpand = (platformId) => {
    setExpandedPlatform(expandedPlatform === platformId ? null : platformId);
  };

  const handlePreview = async (platformId) => {
    setPreviewPlatform(platformId);
    setPreviewLoading(true);
    // Simulate network delay for preview
    setTimeout(() => {
      setPreviewData(demoPreviewData[platformId] || []);
      setPreviewLoading(false);
    }, 600);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-xl font-bold text-slate-900">Integrations</h2>
        <p className="text-sm text-slate-500 mt-1">
          Available platforms, their capabilities, and data previews
        </p>
      </div>

      {/* Platform Cards */}
      <div className="space-y-4">
        {PLATFORM_LIST.map((platform, idx) => {
          const isExpanded = expandedPlatform === platform.id;

          return (
            <div
              key={platform.id}
              className="glass-card overflow-hidden animate-slide-up"
              style={{ animationDelay: `${idx * 80}ms` }}
            >
              {/* Platform Header */}
              <div
                className="flex items-center justify-between p-5 cursor-pointer hover:bg-slate-50 transition-colors"
                onClick={() => toggleExpand(platform.id)}
              >
                <div className="flex items-center gap-4">
                  <div
                    className="w-12 h-12 rounded-xl flex items-center justify-center text-2xl"
                    style={{ backgroundColor: `${platform.color}15` }}
                  >
                    {platform.icon}
                  </div>
                  <div>
                    <h3 className="text-base font-semibold text-slate-900">{platform.name}</h3>
                    <p className="text-sm text-slate-500">{platform.description}</p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <Button
                    variant="outline"
                    size="sm"
                    icon={Eye}
                    onClick={(e) => {
                      e.stopPropagation();
                      handlePreview(platform.id);
                    }}
                  >
                    Preview Data
                  </Button>
                  {isExpanded ? (
                    <ChevronUp className="w-5 h-5 text-slate-500" />
                  ) : (
                    <ChevronDown className="w-5 h-5 text-slate-500" />
                  )}
                </div>
              </div>

              {/* Expanded Content */}
              {isExpanded && (
                <div className="px-5 pb-5 border-t border-slate-200 pt-4 animate-slide-down">
                  {/* Capabilities */}
                  <div className="mb-5">
                    <h4 className="text-sm font-semibold text-slate-700 mb-3 flex items-center gap-2">
                      <Database className="w-4 h-4 text-brand-cyan" /> Capabilities
                    </h4>
                    <div className="flex flex-wrap gap-2">
                      {platform.capabilities.map((cap, capIdx) => (
                        <span
                          key={capIdx}
                          className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium
                            bg-slate-50 border border-slate-200 rounded-full text-slate-700"
                        >
                          <Check className="w-3 h-3 text-brand-cyan" />
                          {cap}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Platform Info */}
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                    <div className="p-4 rounded-xl bg-slate-50 border border-slate-100">
                      <div className="flex items-center gap-2 mb-2">
                        <Info className="w-4 h-4 text-slate-500" />
                        <span className="text-xs text-slate-500">Data Format</span>
                      </div>
                      <p className="text-sm font-medium text-slate-900">JSON / REST API</p>
                    </div>
                    <div className="p-4 rounded-xl bg-slate-50 border border-slate-100">
                      <div className="flex items-center gap-2 mb-2">
                        <RefreshCw className="w-4 h-4 text-slate-500" />
                        <span className="text-xs text-slate-500">Sync Frequency</span>
                      </div>
                      <p className="text-sm font-medium text-slate-900">Real-time / Scheduled</p>
                    </div>
                    <div className="p-4 rounded-xl bg-slate-50 border border-slate-100">
                      <div className="flex items-center gap-2 mb-2">
                        <FileText className="w-4 h-4 text-slate-500" />
                        <span className="text-xs text-slate-500">Authentication</span>
                      </div>
                      <p className="text-sm font-medium text-slate-900">API Key + Secret</p>
                    </div>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Data Preview Modal */}
      <Modal
        isOpen={!!previewPlatform}
        onClose={() => {
          setPreviewPlatform(null);
          setPreviewData(null);
        }}
        title="Data Preview"
        subtitle={PLATFORM_LIST.find((p) => p.id === previewPlatform)?.name || ''}
        size="xl"
      >
        {previewLoading ? (
          <Loader text="Loading data preview..." />
        ) : previewData && previewPlatform ? (
          <DataTable
            columns={previewColumns[previewPlatform] || []}
            data={previewData}
            pageSize={5}
            sortable={false}
            emptyMessage="No data available for preview"
          />
        ) : (
          <div className="text-center py-8">
            <Database className="w-10 h-10 text-slate-600 mx-auto mb-3" />
            <p className="text-sm text-slate-500">No preview data available</p>
          </div>
        )}
      </Modal>
    </div>
  );
}
