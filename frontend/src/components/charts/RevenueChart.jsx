import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import { formatCompactNumber } from '../../utils/formatters';

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;

  return (
    <div className="bg-white border border-slate-200 rounded-xl px-4 py-3 shadow-2xl shadow-black/5">
      <p className="text-xs text-slate-400 mb-1">{label}</p>
      {payload.map((entry, idx) => (
        <p key={idx} className="text-sm font-semibold" style={{ color: entry.color }}>
          {entry.name}: {formatCompactNumber(entry.value)}
        </p>
      ))}
    </div>
  );
};

export default function RevenueChart({ data = [], height = 320 }) {
  // Fallback demo data
  const chartData = data.length > 0 ? data : [
    { month: 'Jan', revenue: 1250000, expenses: 800000 },
    { month: 'Feb', revenue: 1420000, expenses: 850000 },
    { month: 'Mar', revenue: 1380000, expenses: 920000 },
    { month: 'Apr', revenue: 1650000, expenses: 880000 },
    { month: 'May', revenue: 1800000, expenses: 950000 },
    { month: 'Jun', revenue: 1720000, expenses: 1020000 },
    { month: 'Jul', revenue: 1950000, expenses: 980000 },
    { month: 'Aug', revenue: 2100000, expenses: 1100000 },
    { month: 'Sep', revenue: 1980000, expenses: 1050000 },
    { month: 'Oct', revenue: 2250000, expenses: 1150000 },
    { month: 'Nov', revenue: 2400000, expenses: 1200000 },
    { month: 'Dec', revenue: 2680000, expenses: 1300000 },
  ];

  return (
    <ResponsiveContainer width="100%" height={height}>
      <AreaChart data={chartData} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
        <defs>
          <linearGradient id="revenueGradient" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#06b6d4" stopOpacity={0.3} />
            <stop offset="100%" stopColor="#06b6d4" stopOpacity={0} />
          </linearGradient>
          <linearGradient id="expenseGradient" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#8b5cf6" stopOpacity={0.2} />
            <stop offset="100%" stopColor="#8b5cf6" stopOpacity={0} />
          </linearGradient>
        </defs>
        <CartesianGrid strokeDasharray="3 3" stroke="rgba(0,0,0,0.04)" vertical={false} />
        <XAxis
          dataKey="month"
          axisLine={false}
          tickLine={false}
          tick={{ fill: '#64748b', fontSize: 12 }}
        />
        <YAxis
          axisLine={false}
          tickLine={false}
          tick={{ fill: '#64748b', fontSize: 12 }}
          tickFormatter={(val) => `₹${(val / 100000).toFixed(0)}L`}
        />
        <Tooltip content={<CustomTooltip />} />
        <Area
          type="monotone"
          dataKey="revenue"
          name="Revenue"
          stroke="#06b6d4"
          strokeWidth={2.5}
          fill="url(#revenueGradient)"
          dot={false}
          activeDot={{ r: 6, stroke: '#06b6d4', strokeWidth: 2, fill: '#ffffff' }}
        />
        <Area
          type="monotone"
          dataKey="expenses"
          name="Expenses"
          stroke="#8b5cf6"
          strokeWidth={2}
          fill="url(#expenseGradient)"
          dot={false}
          activeDot={{ r: 5, stroke: '#8b5cf6', strokeWidth: 2, fill: '#ffffff' }}
        />
      </AreaChart>
    </ResponsiveContainer>
  );
}
