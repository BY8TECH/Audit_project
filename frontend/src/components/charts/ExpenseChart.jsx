import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts';
import { formatCurrency } from '../../utils/formatters';
import { CHART_COLORS } from '../../utils/constants';

const CustomTooltip = ({ active, payload }) => {
  if (!active || !payload?.length) return null;
  const entry = payload[0];

  return (
    <div className="bg-white border border-slate-200 rounded-xl px-4 py-3 shadow-2xl shadow-black/5">
      <div className="flex items-center gap-2 mb-1">
        <span
          className="w-3 h-3 rounded-full"
          style={{ backgroundColor: entry.payload.fill }}
        />
        <p className="text-sm text-slate-900 font-medium">{entry.name}</p>
      </div>
      <p className="text-sm text-slate-700">{formatCurrency(entry.value)}</p>
      <p className="text-xs text-slate-500">{((entry.payload.percent || 0) * 100).toFixed(1)}%</p>
    </div>
  );
};

const CustomLegend = ({ payload }) => {
  return (
    <div className="flex flex-wrap gap-x-4 gap-y-2 justify-center mt-4">
      {payload?.map((entry, idx) => (
        <div key={idx} className="flex items-center gap-1.5">
          <span
            className="w-2.5 h-2.5 rounded-full"
            style={{ backgroundColor: entry.color }}
          />
          <span className="text-xs text-slate-400">{entry.value}</span>
        </div>
      ))}
    </div>
  );
};

export default function ExpenseChart({ data = [], height = 300 }) {
  // Fallback demo data
  const chartData = data.length > 0 ? data : [
    { name: 'Salaries', value: 450000 },
    { name: 'Rent', value: 120000 },
    { name: 'Utilities', value: 45000 },
    { name: 'Marketing', value: 85000 },
    { name: 'Software', value: 65000 },
    { name: 'Travel', value: 35000 },
    { name: 'Others', value: 50000 },
  ];

  return (
    <ResponsiveContainer width="100%" height={height}>
      <PieChart>
        <Pie
          data={chartData}
          cx="50%"
          cy="45%"
          innerRadius={65}
          outerRadius={100}
          paddingAngle={3}
          dataKey="value"
          stroke="none"
        >
          {chartData.map((_, idx) => (
            <Cell
              key={`cell-${idx}`}
              fill={CHART_COLORS[idx % CHART_COLORS.length]}
              className="transition-opacity duration-200 hover:opacity-80"
            />
          ))}
        </Pie>
        <Tooltip content={<CustomTooltip />} />
        <Legend content={<CustomLegend />} />
      </PieChart>
    </ResponsiveContainer>
  );
}
