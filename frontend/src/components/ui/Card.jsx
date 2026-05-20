export default function Card({
  children,
  title,
  subtitle,
  icon: Icon,
  footer,
  className = '',
  hover = true,
  padding = true,
  gradient = false,
  onClick,
}) {
  return (
    <div
      onClick={onClick}
      className={`
        ${hover ? 'glass-card-hover' : 'glass-card'}
        ${padding ? 'p-6' : ''}
        ${gradient ? 'gradient-border' : ''}
        ${onClick ? 'cursor-pointer' : ''}
        ${className}
      `}
    >
      {/* Header */}
      {(title || Icon) && (
        <div className="flex items-start justify-between mb-4">
          <div>
            {title && (
              <h3 className="text-base font-semibold text-slate-900">{title}</h3>
            )}
            {subtitle && (
              <p className="text-sm text-slate-500 mt-0.5">{subtitle}</p>
            )}
          </div>
          {Icon && (
            <div className="p-2.5 rounded-xl bg-slate-100 text-brand-cyan">
              <Icon className="w-5 h-5" />
            </div>
          )}
        </div>
      )}

      {/* Content */}
      {children}

      {/* Footer */}
      {footer && (
        <div className="mt-4 pt-4 border-t border-slate-200">
          {footer}
        </div>
      )}
    </div>
  );
}
