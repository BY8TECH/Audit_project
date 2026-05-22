import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Home, AlertCircle, ArrowLeft } from 'lucide-react';

const NotFoundPage = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-6 relative overflow-hidden">
      {/* Background Decorative Elements */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-brand-cyan/20 rounded-full mix-blend-multiply filter blur-3xl opacity-70 animate-pulse-slow"></div>
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-brand-purple/20 rounded-full mix-blend-multiply filter blur-3xl opacity-70 animate-pulse-slow animate-delay-200"></div>

      <div className="glass-card p-10 md:p-16 max-w-2xl w-full text-center z-10 relative overflow-hidden animate-scale-in">
        <div className="absolute inset-0 bg-gradient-glass-light opacity-50 z-0 pointer-events-none"></div>
        
        <div className="relative z-10 flex flex-col items-center">
          <div className="w-24 h-24 mb-8 bg-brand-cyan/10 rounded-full flex items-center justify-center glow-cyan animate-bounce">
            <AlertCircle className="w-12 h-12 text-brand-cyan" />
          </div>

          <h1 className="text-8xl md:text-9xl font-black gradient-text tracking-tighter mb-4 select-none">
            404
          </h1>
          
          <h2 className="text-2xl md:text-3xl font-bold text-slate-800 mb-4 text-balance">
            Oops! Page not found
          </h2>
          
          <p className="text-slate-600 mb-10 max-w-md mx-auto text-balance">
            The page you are looking for might have been removed, had its name changed, or is temporarily unavailable.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 w-full sm:w-auto">
            <button
              onClick={() => navigate(-1)}
              className="px-6 py-3 rounded-xl border border-slate-200 bg-white text-slate-700 font-medium hover:bg-slate-50 hover:text-slate-900 transition-all duration-200 flex items-center justify-center gap-2 shadow-sm"
            >
              <ArrowLeft className="w-4 h-4" />
              Go Back
            </button>
            
            <button
              onClick={() => navigate('/dashboard')}
              className="px-6 py-3 rounded-xl bg-gradient-to-r from-brand-cyan to-brand-purple text-white font-medium hover:shadow-lg hover:shadow-brand-cyan/30 transition-all duration-300 flex items-center justify-center gap-2"
            >
              <Home className="w-4 h-4" />
              Back to Dashboard
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NotFoundPage;
