import { Loader2 } from 'lucide-react';

export default function Loader({ text = 'Loading...', fullPage = false, size = 'md' }) {
  const sizeClasses = {
    sm: 'w-5 h-5',
    md: 'w-8 h-8',
    lg: 'w-12 h-12',
  };

  const content = (
    <div className="flex flex-col items-center justify-center gap-3">
      <div className="relative">
        <Loader2 className={`${sizeClasses[size]} text-brand-cyan animate-spin`} />
        <div className={`absolute inset-0 ${sizeClasses[size]} rounded-full border-2 border-brand-cyan/20`} />
      </div>
      {text && <p className="text-sm text-slate-500 animate-pulse">{text}</p>}
    </div>
  );

  if (fullPage) {
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-white/80 backdrop-blur-sm">
        {content}
      </div>
    );
  }

  return (
    <div className="flex items-center justify-center py-12">
      {content}
    </div>
  );
}

export function InlineLoader({ text }) {
  return (
    <span className="inline-flex items-center gap-2 text-sm text-slate-500">
      <Loader2 className="w-4 h-4 animate-spin text-brand-cyan" />
      {text}
    </span>
  );
}
