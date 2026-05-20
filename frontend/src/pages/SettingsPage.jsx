import { useState } from 'react';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import { useAuth } from '../hooks/useAuth';
import authApi from '../api/authApi';

export default function SettingsPage() {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState('profile');
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');

  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    setMessage('');
    try {
      // simulate save
      await new Promise(r => setTimeout(r, 1000));
      setMessage('Settings saved successfully!');
    } catch (err) {
      setMessage('Failed to save settings.');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div>
        <h2 className="text-xl font-bold text-slate-900">Settings</h2>
        <p className="text-sm text-slate-500 mt-1">Manage your account and preferences.</p>
      </div>

      <div className="flex gap-4 border-b border-slate-200">
        <button
          onClick={() => setActiveTab('profile')}
          className={`pb-3 text-sm font-medium border-b-2 transition-colors ${
            activeTab === 'profile' ? 'border-brand-cyan text-brand-cyan' : 'border-transparent text-slate-500 hover:text-slate-700'
          }`}
        >
          Profile
        </button>
        <button
          onClick={() => setActiveTab('security')}
          className={`pb-3 text-sm font-medium border-b-2 transition-colors ${
            activeTab === 'security' ? 'border-brand-cyan text-brand-cyan' : 'border-transparent text-slate-500 hover:text-slate-700'
          }`}
        >
          Security
        </button>
      </div>

      {message && (
        <div className="p-4 bg-emerald-50 text-emerald-600 rounded-xl text-sm">
          {message}
        </div>
      )}

      {activeTab === 'profile' && (
        <Card>
          <form onSubmit={handleSave} className="space-y-4">
            <h3 className="text-lg font-semibold text-slate-900 mb-4">Profile Information</h3>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Full Name</label>
              <input
                type="text"
                defaultValue={user?.name || user?.full_name || ''}
                className="input-dark bg-white border-slate-200 text-slate-900"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Email Address</label>
              <input
                type="email"
                defaultValue={user?.email || ''}
                disabled
                className="input-dark bg-slate-50 border-slate-200 text-slate-500 cursor-not-allowed"
              />
            </div>
            <div className="pt-4 flex justify-end">
              <Button type="submit" loading={saving}>Save Changes</Button>
            </div>
          </form>
        </Card>
      )}

      {activeTab === 'security' && (
        <Card>
          <form onSubmit={handleSave} className="space-y-4">
            <h3 className="text-lg font-semibold text-slate-900 mb-4">Change Password</h3>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Current Password</label>
              <input
                type="password"
                className="input-dark bg-white border-slate-200 text-slate-900"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">New Password</label>
              <input
                type="password"
                className="input-dark bg-white border-slate-200 text-slate-900"
              />
            </div>
            <div className="pt-4 flex justify-end">
              <Button type="submit" loading={saving}>Update Password</Button>
            </div>
          </form>
        </Card>
      )}
    </div>
  );
}
