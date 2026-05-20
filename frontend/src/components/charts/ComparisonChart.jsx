import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { formatCurrency } from '../../utils/formatters';

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;

  return (
    <div className="bg-white border border-slate-200 rounded-xl px-4 py-3 shadow-2xl shadow-black/5">
      <p className="text-xs text-slate-400 mb-2">{label}</p>
      {payload.map((entry, idx) => (
        <div key={idx} className="flex items-center gap-2 mb-1">
          <span className="w-2.5 h-2.5 rounded-sm" style={{ backgroundColor: entry.color }} />
          <span className="text-sm text-slate-700">{entry.name}:</span>
          <span className="text-sm font-semibold text-slate-900">{formatCurrency(entry.value)}</span>
        </div>
      ))}
      {payload.length === 2 && (
        <div className="mt-2 pt-2 border-t border-slate-200">
          <p className={`text-xs font-medium ${
            payload[0].value === payload[1].value 
              ? 'text-emerald-400' 
              : 'text-rose-400'
          }`}>
            Difference: {formatCurrency(Math.abs(payload[0].value - payload[1].value))}
          </p>
        </div>
      )}
    </div>
  );
};

const CustomLegend = ({ payload }) => {
  return (
    <div className="flex items-center justify-center gap-6 mt-4">
      {payload?.map((entry, idx) => (
        <div key={idx} className="flex items-center gap-2">
          <span className="w-3 h-3 rounded-sm" style={{ backgroundColor: entry.color }} />
          <span className="text-xs text-slate-400">{entry.value}</span>
        </div>
      ))}
    </div>
  );
};

export default function ComparisonChart({ data = [], sourceALabel = 'Source A', sourceBLabel = 'Source B', height = 320 }) {
  // Fallback demo data
  const chartData = data.length > 0 ? data : [
    { category: 'Revenue', sourceA: 2500000, sourceB: 2480000 },
    { category: 'COGS', sourceA: 950000, sourceB: 960000 },
    { category: 'Operating', sourceA: 380000, sourceB: 375000 },
    { category: 'Tax', sourceA: 290000, sourceB: 295000 },
    { category: 'Net Profit', sourceA: 880000, sourceB: 850000 },
  ];

  return (
    <ResponsiveContainer width="100%" height={height}>
      <BarChart data={chartData} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="rgba(0,0,0,0.04)" vertical={false} />
        <XAxis
          dataKey="category"
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
        <Legend content={<CustomLegend />} />
        <Bar
          dataKey="sourceA"
          name={sourceALabel}
          fill="#06b6d4"
          radius={[4, 4, 0, 0]}
          maxBarSize={40}
        />
        <Bar
          dataKey="sourceB"
          name={sourceBLabel}
          fill="#8b5cf6"
          radius={[4, 4, 0, 0]}
          maxBarSize={40}
        />
      </BarChart>
    </ResponsiveContainer>
  );
}
