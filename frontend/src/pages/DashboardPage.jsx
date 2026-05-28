import { useCallback } from 'react';
import {
  TrendingUp,
  TrendingDown,
  DollarSign,
  Receipt,
  Landmark,
  PiggyBank,
  ArrowUpRight,
  ArrowDownRight,
  RefreshCw,
} from 'lucide-react';
import Card from '../components/ui/Card';
import Loader from '../components/ui/Loader';
import DataTable from '../components/ui/DataTable';
import RevenueChart from '../components/charts/RevenueChart';
import ExpenseChart from '../components/charts/ExpenseChart';
import { useFetch } from '../hooks/useFetch';
import { dashboardApi } from '../api/dashboardApi';
import { formatCurrency, formatCompactNumber, formatDate, formatRelativeTime } from '../utils/formatters';
import StatusBadge from '../components/ui/StatusBadge';

// Demo summary data (fallback)
const demoSummary = {
  total_revenue: 24580000,
  total_expenses: 12450000,
  tax_liability: 3250000,
  net_profit: 8880000,
  revenue_change: 12.5,
  expense_change: -3.2,
  tax_change: 8.1,
  profit_change: 18.4,
};

const demoTransactions = [
  { id: 1, date: '2026-05-18', description: 'Invoice #INV-2024-0156', amount: 245000, type: 'credit', source: 'zoho_books', status: 'completed' },
  { id: 2, date: '2026-05-17', description: 'Office Rent — May 2026', amount: 120000, type: 'debit', source: 'tally', status: 'completed' },
  { id: 3, date: '2026-05-16', description: 'GST Payment Q1', amount: 185000, type: 'debit', source: 'gst_portal', status: 'pending' },
  { id: 4, date: '2026-05-15', description: 'Client Payment — ABC Corp', amount: 380000, type: 'credit', source: 'zoho_books', status: 'completed' },
  { id: 5, date: '2026-05-14', description: 'Software Subscription', amount: 45000, type: 'debit', source: 'tally', status: 'completed' },
  { id: 6, date: '2026-05-13', description: 'TDS Deducted', amount: 28000, type: 'debit', source: 'income_tax', status: 'completed' },
  { id: 7, date: '2026-05-12', description: 'Invoice #INV-2024-0155', amount: 195000, type: 'credit', source: 'zoho_books', status: 'completed' },
  { id: 8, date: '2026-05-11', description: 'Payroll — May 2026', amount: 450000, type: 'debit', source: 'tally', status: 'completed' },
];

const sourceLabels = {
  zoho_books: 'Zoho Books',
  tally: 'Tally',
  gst_portal: 'GST Portal',
  income_tax: 'Income Tax',
};

const sourceColors = {
  zoho_books: 'bg-emerald-500/10 text-emerald-400',
  tally: 'bg-orange-500/10 text-orange-400',
  gst_portal: 'bg-blue-500/10 text-blue-400',
  income_tax: 'bg-purple-500/10 text-purple-400',
};

export default function DashboardPage() {
  const {
    data: summaryData,
    loading: summaryLoading,
    refetch: refetchSummary,
  } = useFetch(useCallback(() => dashboardApi.getSummary(), []), [], { initialData: null });

  const {
    data: transactionsData,
    loading: transactionsLoading,
  } = useFetch(useCallback(() => dashboardApi.getRecentTransactions(10), []), [], { initialData: null });

  const {
    data: revenueData,
    loading: revenueLoading,
  } = useFetch(useCallback(() => dashboardApi.getRevenueTrend(), []), [], { initialData: null });

  const {
    data: expenseData,
    loading: expenseLoading,
  } = useFetch(useCallback(() => dashboardApi.getExpenseBreakdown(), []), [], { initialData: null });

  const summary = summaryData || demoSummary;
  const transactions = transactionsData?.transactions || transactionsData || demoTransactions;
  const revenueTrend = revenueData?.trend || revenueData || [];
  const expenses = expenseData?.breakdown || expenseData || [];

  const summaryCards = [
    {
      title: 'Total Revenue',
      value: summary.total_revenue,
      change: summary.revenue_change,
      icon: DollarSign,
      color: 'from-brand-cyan/20 to-brand-cyan/5',
      iconBg: 'bg-brand-cyan/10',
      iconColor: 'text-brand-cyan',
    },
    {
      title: 'Total Expenses',
      value: summary.total_expenses,
      change: summary.expense_change,
      icon: Receipt,
      color: 'from-brand-purple/20 to-brand-purple/5',
      iconBg: 'bg-brand-purple/10',
      iconColor: 'text-brand-purple',
    },
    {
      title: 'Tax Liability',
      value: summary.tax_liability,
      change: summary.tax_change,
      icon: Landmark,
      color: 'from-amber-500/20 to-amber-500/5',
      iconBg: 'bg-amber-500/10',
      iconColor: 'text-amber-400',
    },
    {
      title: 'Net Profit',
      value: summary.net_profit,
      change: summary.profit_change,
      icon: PiggyBank,
      color: 'from-emerald-500/20 to-emerald-500/5',
      iconBg: 'bg-emerald-500/10',
      iconColor: 'text-emerald-400',
    },
  ];

  const transactionColumns = [
    { key: 'date', label: 'Date', render: (val) => formatDate(val) },
    { key: 'description', label: 'Description', render: (val) => <span className="font-medium text-slate-900">{val}</span> },
    {
      key: 'amount',
      label: 'Amount',
      align: 'right',
      render: (val, row) => (
        <span className={row.type === 'credit' ? 'text-emerald-400' : 'text-rose-400'}>
          {row.type === 'credit' ? '+' : '-'}{formatCurrency(val)}
        </span>
      ),
    },
    {
      key: 'source_platform',
      label: 'Source',
      render: (val, row) => {
        const sourceVal = val || row.source;
        return (
          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${sourceColors[sourceVal] || 'bg-slate-500/10 text-slate-400'}`}>
            {sourceLabels[sourceVal] || sourceVal}
          </span>
        );
      },
    },
    {
      key: 'status',
      label: 'Status',
      render: (val) => <StatusBadge status={val === 'completed' ? 'connected' : val === 'pending' ? 'syncing' : 'disconnected'} label={val} size="sm" />,
    },
  ];

  return (
    <div className="space-y-6">
      {/* Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        {summaryCards.map((card, idx) => (
          <div
            key={idx}
            className={`glass-card-hover p-5 animate-slide-up`}
            style={{ animationDelay: `${idx * 80}ms` }}
          >
            <div className="flex items-start justify-between mb-4">
              <div className={`p-2.5 rounded-xl ${card.iconBg}`}>
                <card.icon className={`w-5 h-5 ${card.iconColor}`} />
              </div>
              {card.change !== undefined && (
                <div className={`flex items-center gap-0.5 text-xs font-medium 
                  ${card.change >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}
                >
                  {card.change >= 0 ? (
                    <ArrowUpRight className="w-3.5 h-3.5" />
                  ) : (
                    <ArrowDownRight className="w-3.5 h-3.5" />
                  )}
                  {Math.abs(card.change)}%
                </div>
              )}
            </div>
            <p className="text-sm text-slate-500 mb-1">{card.title}</p>
            <p className="text-2xl font-bold text-slate-900">
              {summaryLoading ? (
                <span className="inline-block w-32 h-7 bg-slate-100 rounded shimmer" />
              ) : (
                formatCompactNumber(card.value)
              )}
            </p>
          </div>
        ))}
      </div>

      {/* Revenue Trend */}
      <Card
        title="Revenue Trend"
        subtitle="Monthly revenue vs expenses (last 12 months)"
        className="animate-slide-up animate-delay-200"
      >
        {revenueLoading ? <Loader text="Loading chart..." /> : <RevenueChart data={revenueTrend} />}
      </Card>

      {/* Expense Breakdown + Platform Summary */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card
          title="Expense Breakdown"
          subtitle="By category"
          className="animate-slide-up animate-delay-300"
        >
          {expenseLoading ? <Loader text="Loading..." /> : <ExpenseChart data={expenses} />}
        </Card>

        <Card
          title="Platform Data Summary"
          subtitle="Connected source overview"
          className="animate-slide-up animate-delay-400"
        >
          <div className="space-y-3 mt-2">
            {[
              { name: 'Zoho Books', records: '1,234', status: 'connected', lastSync: '2h ago', color: 'bg-emerald-500' },
              { name: 'Tally Prime', records: '856', status: 'connected', lastSync: '4h ago', color: 'bg-orange-500' },
              { name: 'GST Portal', records: '342', status: 'syncing', lastSync: '1d ago', color: 'bg-blue-500' },
              { name: 'Income Tax', records: '—', status: 'disconnected', lastSync: 'Never', color: 'bg-purple-500' },
            ].map((platform, idx) => (
              <div
                key={idx}
                className="flex items-center justify-between p-3.5 rounded-xl bg-white border border-slate-200
                  hover:bg-slate-50 transition-colors duration-200"
              >
                <div className="flex items-center gap-3">
                  <div className={`w-2 h-2 rounded-full ${platform.color}`} />
                  <div>
                    <p className="text-sm font-medium text-slate-900">{platform.name}</p>
                    <p className="text-xs text-slate-500">{platform.records} records • {platform.lastSync}</p>
                  </div>
                </div>
                <StatusBadge status={platform.status} size="sm" />
              </div>
            ))}
          </div>
        </Card>
      </div>

      {/* Recent Transactions */}
      <div className="animate-slide-up animate-delay-400">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-lg font-semibold text-slate-900">Recent Transactions</h3>
            <p className="text-sm text-slate-500">Latest financial activities across all platforms</p>
          </div>
          <button
            onClick={refetchSummary}
            className="flex items-center gap-2 px-3 py-1.5 text-xs font-medium text-slate-600 
              hover:text-slate-900 bg-slate-50 hover:bg-slate-100 rounded-lg transition-all duration-200"
          >
            <RefreshCw className="w-3.5 h-3.5" /> Refresh
          </button>
        </div>
        {transactionsLoading ? (
          <Loader text="Loading transactions..." />
        ) : (
          <DataTable columns={transactionColumns} data={transactions} pageSize={8} />
        )}
      </div>
    </div>
  );
}
