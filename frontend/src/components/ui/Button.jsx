import { Loader2 } from 'lucide-react';

const variants = {
  primary:
    'bg-gradient-to-r from-brand-cyan to-brand-teal text-white shadow-lg shadow-brand-cyan/20 hover:shadow-brand-cyan/30 hover:brightness-110',
  secondary:
    'bg-gradient-to-r from-brand-purple to-brand-indigo text-white shadow-lg shadow-brand-purple/20 hover:shadow-brand-purple/30 hover:brightness-110',
  outline:
    'bg-transparent border border-slate-300 text-slate-600 hover:bg-slate-50 hover:text-slate-900 hover:border-slate-400',
  danger:
    'bg-rose-500/10 text-rose-500 border border-rose-500/20 hover:bg-rose-500/20 hover:border-rose-500/30',
  ghost:
    'bg-transparent text-slate-500 hover:text-slate-900 hover:bg-slate-100',
  success:
    'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 hover:bg-emerald-500/20',
};

const sizes = {
  sm: 'px-3 py-1.5 text-xs rounded-lg gap-1.5',
  md: 'px-5 py-2.5 text-sm rounded-xl gap-2',
  lg: 'px-7 py-3 text-base rounded-xl gap-2.5',
};

export default function Button({
  children,
  variant = 'primary',
  size = 'md',
  loading = false,
  disabled = false,
  icon: Icon,
  iconRight: IconRight,
  className = '',
  ...props
}) {
  return (
    <button
      disabled={disabled || loading}
      className={`
        inline-flex items-center justify-center font-medium transition-all duration-200 
        active:scale-[0.97] disabled:opacity-50 disabled:cursor-not-allowed disabled:active:scale-100
        ${variants[variant] || variants.primary}
        ${sizes[size] || sizes.md}
        ${className}
      `}
      {...props}
    >
      {loading ? (
        <Loader2 className="w-4 h-4 animate-spin" />
      ) : (
        Icon && <Icon className={`${size === 'sm' ? 'w-3.5 h-3.5' : 'w-4 h-4'}`} />
      )}
      {children}
      {IconRight && !loading && (
        <IconRight className={`${size === 'sm' ? 'w-3.5 h-3.5' : 'w-4 h-4'}`} />
      )}
    </button>
  );
}
