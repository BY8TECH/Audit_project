export const API_BASE_URL = 'http://localhost:8000/api/v1';

export const PLATFORMS = {
  ZOHO_BOOKS: {
    id: 'zoho_books',
    name: 'Zoho Books',
    description: 'Cloud-based accounting software for small businesses',
    color: '#1CA450',
    icon: '📗',
    capabilities: ['Invoices', 'Expenses', 'Bank Transactions', 'Contacts', 'Tax Reports'],
  },
  TALLY: {
    id: 'tally',
    name: 'Tally Prime',
    description: 'Complete business management software for Indian businesses',
    color: '#FF6B35',
    icon: '📊',
    capabilities: ['Ledgers', 'Vouchers', 'Stock Items', 'GST Reports', 'Balance Sheet'],
  },
  GST_PORTAL: {
    id: 'gst_portal',
    name: 'GST Portal',
    description: 'Government GST compliance and filing platform',
    color: '#2563EB',
    icon: '🏛️',
    capabilities: ['GSTR-1', 'GSTR-3B', 'ITC Claims', 'E-Way Bills', 'Returns Status'],
  },
  INCOME_TAX: {
    id: 'income_tax',
    name: 'Income Tax Portal',
    description: 'Income tax filing and compliance portal',
    color: '#7C3AED',
    icon: '📋',
    capabilities: ['ITR Forms', 'Tax Computation', 'TDS Details', 'Refund Status', 'Notices'],
  },
};

export const PLATFORM_LIST = Object.values(PLATFORMS);

export const STATUS_COLORS = {
  connected: {
    bg: 'bg-emerald-500/10',
    text: 'text-emerald-600',
    border: 'border-emerald-500/30',
    dot: 'bg-emerald-500',
  },
  disconnected: {
    bg: 'bg-slate-500/10',
    text: 'text-slate-600',
    border: 'border-slate-500/30',
    dot: 'bg-slate-500',
  },
  error: {
    bg: 'bg-rose-500/10',
    text: 'text-rose-600',
    border: 'border-rose-500/30',
    dot: 'bg-rose-500',
  },
  syncing: {
    bg: 'bg-amber-500/10',
    text: 'text-amber-600',
    border: 'border-amber-500/30',
    dot: 'bg-amber-500',
  },
};

export const NAV_ITEMS = [
  { label: 'Dashboard', path: '/dashboard', icon: 'LayoutDashboard' },
  { label: 'Connections', path: '/connections', icon: 'Link2' },
  { label: 'Integrations', path: '/integrations', icon: 'Puzzle' },
  { label: 'Reconciliation', path: '/reconciliation', icon: 'GitCompare' },
];

export const CHART_COLORS = ['#06b6d4', '#8b5cf6', '#14b8a6', '#f59e0b', '#f43f5e', '#6366f1', '#10b981', '#ec4899'];

export const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
