import { useState } from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import {
  LayoutDashboard,
  Link2,
  Puzzle,
  GitCompare,
  ChevronLeft,
  ChevronRight,
  LogOut,
  Settings,
  Shield,
} from 'lucide-react';
import { useAuth } from '../../hooks/useAuth';

const navIcons = {
  LayoutDashboard,
  Link2,
  Puzzle,
  GitCompare,
};

const navItems = [
  { label: 'Dashboard', path: '/dashboard', icon: 'LayoutDashboard' },
  { label: 'Connections', path: '/connections', icon: 'Link2' },
  { label: 'Integrations', path: '/integrations', icon: 'Puzzle' },
  { label: 'Reconciliation', path: '/reconciliation', icon: 'GitCompare' },
];

export default function Sidebar({ collapsed, onToggle, onLogoutClick }) {
  const location = useLocation();
  const { user } = useAuth();
  const [hoveredItem, setHoveredItem] = useState(null);

  return (
    <aside
      className={`fixed left-0 top-0 h-full z-40 flex flex-col transition-all duration-300 ease-out
        ${collapsed ? 'w-20' : 'w-64'}
        bg-white/95 backdrop-blur-xl border-r border-slate-200`}
    >
      {/* Logo */}
      <div className="flex items-center gap-3 px-5 h-16 border-b border-slate-200 flex-shrink-0">
        <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-brand-cyan to-brand-purple flex items-center justify-center flex-shrink-0 shadow-sm">
          <Shield className="w-5 h-5 text-white" />
        </div>
        {!collapsed && (
          <div className="animate-fade-in">
            <h1 className="text-base font-bold gradient-text leading-tight">AuditFlow</h1>
            <p className="text-[10px] text-slate-500 font-medium tracking-wider uppercase">Pro Platform</p>
          </div>
        )}
      </div>

      {/* Navigation */}
      <nav className="flex-1 py-4 px-3 space-y-1 overflow-y-auto">
        <p className={`text-[11px] font-semibold text-slate-500 uppercase tracking-wider mb-3 
          ${collapsed ? 'text-center' : 'px-3'}`}>
          {collapsed ? '•••' : 'Main Menu'}
        </p>
        {navItems.map((item) => {
          const IconComponent = navIcons[item.icon];
          const isActive = location.pathname === item.path;

          return (
            <NavLink
              key={item.path}
              to={item.path}
              onMouseEnter={() => setHoveredItem(item.path)}
              onMouseLeave={() => setHoveredItem(null)}
              className={`group relative flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all duration-200
                ${isActive
                  ? 'bg-brand-cyan/10 text-brand-cyan'
                  : 'text-slate-500 hover:text-slate-900 hover:bg-slate-50'
                }
                ${collapsed ? 'justify-center' : ''}
              `}
            >
              {/* Active indicator */}
              {isActive && (
                <div className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-6 bg-brand-cyan rounded-r-full" />
              )}

              <IconComponent className={`w-5 h-5 flex-shrink-0 transition-transform duration-200
                ${isActive ? 'text-brand-cyan' : 'group-hover:scale-110'}`} />

              {!collapsed && (
                <span className="text-sm font-medium">{item.label}</span>
              )}

              {/* Tooltip for collapsed state */}
              {collapsed && hoveredItem === item.path && (
                <div className="absolute left-full ml-3 px-3 py-1.5 bg-slate-800 text-white text-sm rounded-lg 
                  shadow-xl border border-slate-700 whitespace-nowrap z-50 animate-fade-in">
                  {item.label}
                </div>
              )}
            </NavLink>
          );
        })}
      </nav>

      {/* Collapse Toggle */}
      <div className="px-3 py-2">
        <button
          onClick={onToggle}
          className="w-full flex items-center justify-center gap-2 px-3 py-2 rounded-xl text-slate-500 
            hover:text-slate-900 hover:bg-slate-50 transition-all duration-200"
        >
          {collapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
          {!collapsed && <span className="text-xs font-medium">Collapse</span>}
        </button>
      </div>

      {/* User Section */}
      <div className="border-t border-slate-200 p-3 flex-shrink-0">
        <div className={`flex items-center gap-3 ${collapsed ? 'justify-center' : ''}`}>
          <div className="w-9 h-9 rounded-full bg-gradient-to-br from-brand-purple to-brand-cyan 
            flex items-center justify-center flex-shrink-0 text-sm font-semibold text-white">
            {user?.name?.charAt(0)?.toUpperCase() || user?.email?.charAt(0)?.toUpperCase() || 'U'}
          </div>
          {!collapsed && (
            <div className="flex-1 min-w-0 animate-fade-in">
              <p className="text-sm font-medium text-slate-900 truncate">
                {user?.name || 'User'}
              </p>
              <p className="text-xs text-slate-500 truncate">
                {user?.email || 'user@email.com'}
              </p>
            </div>
          )}
          {!collapsed && (
            <button
              onClick={onLogoutClick}
              className="p-1.5 rounded-lg text-slate-500 hover:text-rose-400 hover:bg-rose-500/10 
                transition-all duration-200"
              title="Logout"
            >
              <LogOut className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>
    </aside>
  );
}
