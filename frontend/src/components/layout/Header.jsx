import { useState, useRef, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Search, Bell, ChevronDown, LogOut, User, Settings } from 'lucide-react';
import { useAuth } from '../../hooks/useAuth';

const pageTitles = {
  '/dashboard': 'Dashboard',
  '/connections': 'Connections',
  '/integrations': 'Integrations',
  '/reconciliation': 'Reconciliation',
};

export default function Header() {
  const location = useLocation();
  const { user, logout } = useAuth();
  const [showDropdown, setShowDropdown] = useState(false);
  const [showSearch, setShowSearch] = useState(false);
  const dropdownRef = useRef(null);

  const pageTitle = pageTitles[location.pathname] || 'Dashboard';

  // Close dropdown on outside click
  useEffect(() => {
    const handleClick = (e) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setShowDropdown(false);
      }
    };
    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, []);

  return (
    <header className="sticky top-0 z-30 h-16 flex items-center justify-between px-6 
      bg-white/80 backdrop-blur-xl border-b border-slate-200">
      {/* Left: Page Title */}
      <div>
        <h2 className="text-xl font-semibold text-slate-900">{pageTitle}</h2>
        <p className="text-xs text-slate-500">
          {new Date().toLocaleDateString('en-IN', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
        </p>
      </div>

      {/* Right: Actions */}
      <div className="flex items-center gap-3">
        {/* Search */}
        <div className={`relative transition-all duration-300 ${showSearch ? 'w-64' : 'w-10'}`}>
          {showSearch ? (
            <div className="flex items-center bg-slate-50 border border-slate-200 rounded-xl overflow-hidden animate-scale-in">
              <Search className="w-4 h-4 text-slate-400 ml-3" />
              <input
                type="text"
                placeholder="Search..."
                autoFocus
                onBlur={() => setShowSearch(false)}
                className="w-full px-3 py-2 bg-transparent text-slate-900 text-sm placeholder-slate-400 
                  focus:outline-none"
              />
            </div>
          ) : (
            <button
              onClick={() => setShowSearch(true)}
              className="w-10 h-10 flex items-center justify-center rounded-xl text-slate-500 
                hover:text-brand-cyan hover:bg-slate-50 transition-all duration-200"
            >
              <Search className="w-5 h-5" />
            </button>
          )}
        </div>

        {/* Notifications */}
        <button className="relative w-10 h-10 flex items-center justify-center rounded-xl text-slate-500 
          hover:text-brand-cyan hover:bg-slate-50 transition-all duration-200">
          <Bell className="w-5 h-5" />
          <span className="absolute top-2 right-2 w-2 h-2 bg-brand-cyan rounded-full animate-pulse" />
        </button>

        {/* Divider */}
        <div className="w-px h-8 bg-slate-200" />

        {/* User Dropdown */}
        <div className="relative" ref={dropdownRef}>
          <button
            onClick={() => setShowDropdown(!showDropdown)}
            className="flex items-center gap-3 px-3 py-1.5 rounded-xl hover:bg-slate-50 
              transition-all duration-200"
          >
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-brand-cyan to-brand-purple 
              flex items-center justify-center text-sm font-semibold text-white">
              {user?.name?.charAt(0)?.toUpperCase() || 'U'}
            </div>
            <div className="hidden sm:block text-left">
              <p className="text-sm font-medium text-slate-900 leading-tight">
                {user?.name || 'User'}
              </p>
              <p className="text-[11px] text-slate-500">Auditor</p>
            </div>
            <ChevronDown className={`w-4 h-4 text-slate-500 transition-transform duration-200 
              ${showDropdown ? 'rotate-180' : ''}`} />
          </button>

          {/* Dropdown Menu */}
          {showDropdown && (
            <div className="absolute right-0 top-full mt-2 w-56 py-2 bg-white border border-slate-200 
              rounded-xl shadow-lg shadow-black/5 animate-slide-down z-50">
              <div className="px-4 py-3 border-b border-slate-100">
                <p className="text-sm font-medium text-slate-900">{user?.name || 'User'}</p>
                <p className="text-xs text-slate-500">{user?.email || 'user@email.com'}</p>
              </div>
              <div className="py-1">
                <Link to="/settings" onClick={() => setShowDropdown(false)} className="w-full flex items-center gap-3 px-4 py-2.5 text-sm text-slate-600 
                  hover:text-brand-cyan hover:bg-slate-50 transition-colors duration-150">
                  <User className="w-4 h-4" /> Profile
                </Link>
                <Link to="/settings" onClick={() => setShowDropdown(false)} className="w-full flex items-center gap-3 px-4 py-2.5 text-sm text-slate-600 
                  hover:text-brand-cyan hover:bg-slate-50 transition-colors duration-150">
                  <Settings className="w-4 h-4" /> Settings
                </Link>
              </div>
              <div className="border-t border-slate-100 pt-1">
                <button
                  onClick={() => { setShowDropdown(false); logout(); }}
                  className="w-full flex items-center gap-3 px-4 py-2.5 text-sm text-rose-500 
                    hover:bg-rose-50 transition-colors duration-150">
                  <LogOut className="w-4 h-4" /> Logout
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
