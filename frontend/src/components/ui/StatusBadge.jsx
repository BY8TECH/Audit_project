import { STATUS_COLORS } from '../../utils/constants';

export default function StatusBadge({ status = 'disconnected', label, size = 'md' }) {
  const colors = STATUS_COLORS[status] || STATUS_COLORS.disconnected;
  const displayLabel = label || status.charAt(0).toUpperCase() + status.slice(1);

  const sizeClasses = {
    sm: 'text-[10px] px-2 py-0.5 gap-1',
    md: 'text-xs px-2.5 py-1 gap-1.5',
    lg: 'text-sm px-3 py-1.5 gap-2',
  };

  return (
    <span
      className={`inline-flex items-center font-medium rounded-full 
        ${colors.bg} ${colors.text} ${colors.border} border
        ${sizeClasses[size] || sizeClasses.md}`}
    >
      <span
        className={`rounded-full flex-shrink-0 ${colors.dot}
          ${size === 'sm' ? 'w-1.5 h-1.5' : 'w-2 h-2'}
          ${status === 'syncing' ? 'animate-pulse' : ''}
          ${status === 'connected' ? 'shadow-sm shadow-emerald-400/50' : ''}`}
      />
      {displayLabel}
    </span>
  );
}
