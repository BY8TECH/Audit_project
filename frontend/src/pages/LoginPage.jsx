import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Shield, Eye, EyeOff, ArrowRight, Loader2, CheckCircle2, BarChart3, Link2, GitCompare } from 'lucide-react';
import { useAuth } from '../hooks/useAuth';

export default function LoginPage() {
  const navigate = useNavigate();
  const { login, register, error, clearError } = useAuth();

  const [isLogin, setIsLogin] = useState(true);
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [formError, setFormError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [form, setForm] = useState({
    name: '',
    email: '',
    password: '',
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    setFormError('');
    setSuccessMessage('');
    clearError?.();
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setFormError('');
    setSuccessMessage('');

    // Validation
    if (!form.email || !form.password) {
      setFormError('Please fill in all required fields');
      return;
    }
    if (!isLogin && !form.name) {
      setFormError('Please enter your name');
      return;
    }
    if (form.password.length < 6) {
      setFormError('Password must be at least 6 characters');
      return;
    }

    setLoading(true);
    try {
      if (isLogin) {
        await login(form.email, form.password);
        navigate('/dashboard');
      } else {
        await register(form.name, form.email, form.password);
        setIsLogin(true);
        setForm({ ...form, password: '' });
        setSuccessMessage('Registration successful! Please sign in.');
      }
    } catch (err) {
      setFormError(err.message || 'Something went wrong');
    } finally {
      setLoading(false);
    }
  };

  const toggleMode = () => {
    setIsLogin(!isLogin);
    setFormError('');
    setSuccessMessage('');
    clearError?.();
  };

  const features = [
    { icon: BarChart3, title: 'Real-time Analytics', desc: 'Live dashboards with financial insights' },
    { icon: Link2, title: 'Multi-platform Sync', desc: 'Connect Zoho, Tally, GST & more' },
    { icon: GitCompare, title: 'Data Reconciliation', desc: 'Cross-platform data matching' },
  ];

  return (
    <div className="min-h-screen flex">
      {/* Left Panel — Branding */}
      <div className="hidden lg:flex lg:w-1/2 relative overflow-hidden">
        {/* Animated Gradient Background */}
        <div className="absolute inset-0 bg-gradient-to-br from-indigo-50 via-white to-cyan-50" />
        <div className="absolute inset-0 bg-gradient-to-tr from-brand-purple/5 via-transparent to-brand-cyan/5" />

        {/* Grid pattern overlay */}
        <div
          className="absolute inset-0 opacity-[0.03]"
          style={{
            backgroundImage: `linear-gradient(rgba(0,0,0,0.05) 1px, transparent 1px),
              linear-gradient(90deg, rgba(0,0,0,0.05) 1px, transparent 1px)`,
            backgroundSize: '40px 40px',
          }}
        />

        {/* Glowing orbs */}
        <div className="absolute top-1/4 left-1/4 w-64 h-64 bg-brand-cyan/20 rounded-full blur-[128px] animate-pulse-slow" />
        <div className="absolute bottom-1/4 right-1/4 w-48 h-48 bg-brand-purple/20 rounded-full blur-[96px] animate-pulse-slow" />

        {/* Content */}
        <div className="relative z-10 flex flex-col justify-center px-16 w-full">
          {/* Logo */}
          <div className="flex items-center gap-3 mb-12">
            <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-brand-cyan to-brand-purple flex items-center justify-center shadow-lg shadow-brand-cyan/25">
              <Shield className="w-7 h-7 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold gradient-text">AuditFlow Pro</h1>
              <p className="text-xs text-slate-500 font-medium tracking-widest uppercase">Auditor Platform</p>
            </div>
          </div>

          <h2 className="text-4xl font-bold text-slate-900 leading-tight mb-4">
            Streamline your<br />
            <span className="gradient-text">audit workflow</span>
          </h2>
          <p className="text-slate-600 text-lg mb-12 max-w-md">
            Integrate multiple data sources, reconcile financial records, and generate insights—all in one place.
          </p>

          {/* Feature Cards */}
          <div className="space-y-4">
            {features.map((feature, idx) => (
              <div
                key={idx}
                className="flex items-center gap-4 p-4 rounded-xl bg-white/60 border border-slate-200 
                  backdrop-blur-sm animate-slide-up shadow-sm"
                style={{ animationDelay: `${idx * 100}ms` }}
              >
                <div className="p-2.5 rounded-xl bg-brand-cyan/10">
                  <feature.icon className="w-5 h-5 text-brand-cyan" />
                </div>
                <div>
                  <h3 className="text-sm font-semibold text-slate-900">{feature.title}</h3>
                  <p className="text-xs text-slate-500">{feature.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Right Panel — Form */}
      <div className="flex-1 flex items-center justify-center px-6 py-12 bg-white lg:bg-slate-50">
        <div className="w-full max-w-md animate-fade-in">
          {/* Mobile Logo */}
          <div className="flex items-center gap-3 mb-8 lg:hidden">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-brand-cyan to-brand-purple flex items-center justify-center">
              <Shield className="w-6 h-6 text-white" />
            </div>
            <h1 className="text-xl font-bold gradient-text">AuditFlow Pro</h1>
          </div>

          <div className="mb-8">
            <h2 className="text-2xl font-bold text-slate-900">
              {isLogin ? 'Welcome back' : 'Create account'}
            </h2>
            <p className="text-slate-500 mt-1">
              {isLogin ? 'Sign in to continue to your dashboard' : 'Get started with your free account'}
            </p>
          </div>

          {/* Error Display */}
          {(formError || error) && (
            <div className="mb-6 px-4 py-3 rounded-xl bg-rose-500/10 border border-rose-500/20 animate-slide-down">
              <p className="text-sm text-rose-400">{formError || error}</p>
            </div>
          )}

          {/* Success Display */}
          {successMessage && (
            <div className="mb-6 px-4 py-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20 animate-slide-down">
              <p className="text-sm text-emerald-600">{successMessage}</p>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            {/* Name (Register only) */}
            {!isLogin && (
              <div className="animate-slide-down">
                <label className="block text-sm font-medium text-slate-700 mb-2">Full Name</label>
                <input
                  type="text"
                  name="name"
                  value={form.name}
                  onChange={handleChange}
                  placeholder="John Doe"
                  className="input-dark"
                />
              </div>
            )}

            {/* Email */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Email Address</label>
              <input
                type="email"
                name="email"
                value={form.email}
                onChange={handleChange}
                placeholder="you@example.com"
                className="input-dark"
                autoComplete="email"
              />
            </div>

            {/* Password */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Password</label>
              <div className="relative">
                <input
                  type={showPassword ? 'text' : 'password'}
                  name="password"
                  value={form.password}
                  onChange={handleChange}
                  placeholder="••••••••"
                  className="input-dark pr-12"
                  autoComplete={isLogin ? 'current-password' : 'new-password'}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 p-1 text-slate-400 hover:text-slate-600 transition-colors"
                >
                  {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
            </div>

            {/* Submit */}
            <button
              type="submit"
              disabled={loading}
              className="w-full flex items-center justify-center gap-2 px-6 py-3 
                bg-gradient-to-r from-brand-cyan to-brand-teal text-white font-semibold rounded-xl
                shadow-lg shadow-brand-cyan/20 hover:shadow-brand-cyan/30 hover:brightness-110
                transition-all duration-200 active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <>
                  {isLogin ? 'Sign In' : 'Create Account'}
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </form>

          {/* Toggle Mode */}
          <p className="mt-8 text-center text-sm text-slate-500">
            {isLogin ? "Don't have an account?" : 'Already have an account?'}{' '}
            <button
              onClick={toggleMode}
              className="text-brand-cyan hover:text-brand-teal font-medium transition-colors"
            >
              {isLogin ? 'Sign up' : 'Sign in'}
            </button>
          </p>

          {/* Divider */}
          <div className="mt-8 flex items-center gap-4">
            <div className="flex-1 h-px bg-slate-200" />
            <span className="text-xs text-slate-400">SECURED</span>
            <div className="flex-1 h-px bg-slate-200" />
          </div>

          <div className="mt-4 flex items-center justify-center gap-2 text-xs text-slate-500">
            <CheckCircle2 className="w-3.5 h-3.5" />
            256-bit SSL encrypted connection
          </div>
        </div>
      </div>
    </div>
  );
}
