import { useState } from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Header from './Header';
import Modal from '../ui/Modal';
import { LogOut } from 'lucide-react';
import { useAuth } from '../../hooks/useAuth';

export default function MainLayout() {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [showLogoutModal, setShowLogoutModal] = useState(false);
  const { logout } = useAuth();

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Sidebar */}
      <Sidebar
        collapsed={sidebarCollapsed}
        onToggle={() => setSidebarCollapsed(!sidebarCollapsed)}
        onLogoutClick={() => setShowLogoutModal(true)}
      />

      {/* Main Content */}
      <div
        className={`transition-all duration-300 ${sidebarCollapsed ? 'ml-20' : 'ml-64'}`}
      >
        <Header onLogoutClick={() => setShowLogoutModal(true)} />
        <main className="p-6 min-h-[calc(100vh-4rem)]">
          <div className="max-w-7xl mx-auto animate-fade-in">
            <Outlet />
          </div>
        </main>
      </div>

      {/* Logout Confirmation Modal */}
      <Modal
        isOpen={showLogoutModal}
        onClose={() => setShowLogoutModal(false)}
        title="Confirm Logout"
        subtitle="Are you sure you want to log out?"
        footer={
          <>
            <button
              onClick={() => setShowLogoutModal(false)}
              className="px-4 py-2 rounded-xl text-sm font-medium text-slate-700 bg-white border border-slate-300 hover:bg-slate-50 transition-colors"
            >
              Cancel
            </button>
            <button
              onClick={() => {
                setShowLogoutModal(false);
                logout();
              }}
              className="px-4 py-2 rounded-xl text-sm font-medium text-white bg-rose-500 hover:bg-rose-600 transition-colors flex items-center gap-2 shadow-sm"
            >
              <LogOut className="w-4 h-4" />
              Yes, Logout
            </button>
          </>
        }
      >
        <div className="py-2">
          <p className="text-slate-600">You will be securely signed out of your account. You will need to enter your credentials to log back in.</p>
        </div>
      </Modal>
    </div>
  );
}
