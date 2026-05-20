import { useState, useCallback } from 'react';
import {
  RefreshCw,
  Plus,
  Unplug,
  CheckCircle2,
  AlertTriangle,
  Clock,
  Database,
  Wifi,
  WifiOff,
  Zap,
} from 'lucide-react';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import StatusBadge from '../components/ui/StatusBadge';
import Modal from '../components/ui/Modal';
import Loader from '../components/ui/Loader';
import { useFetch } from '../hooks/useFetch';
import { integrationApi } from '../api/integrationApi';
import { PLATFORM_LIST } from '../utils/constants';
import { formatRelativeTime } from '../utils/formatters';

const demoPlatforms = [
  {
    id: 'zoho_books',
    name: 'Zoho Books',
    icon: '📗',
    color: '#1CA450',
    status: 'connected',
    last_sync: '2026-05-20T06:30:00Z',
    record_count: 1234,
    health: 'good',
    description: 'Cloud-based accounting software',
  },
  {
    id: 'tally',
    name: 'Tally Prime',
    icon: '📊',
    color: '#FF6B35',
    status: 'connected',
    last_sync: '2026-05-20T04:15:00Z',
    record_count: 856,
    health: 'good',
    description: 'Business management software',
  },
  {
    id: 'gst_portal',
    name: 'GST Portal',
    icon: '🏛️',
    color: '#2563EB',
    status: 'syncing',
    last_sync: '2026-05-19T10:00:00Z',
    record_count: 342,
    health: 'warning',
    description: 'Government GST compliance platform',
  },
  {
    id: 'income_tax',
    name: 'Income Tax Portal',
    icon: '📋',
    color: '#7C3AED',
    status: 'disconnected',
    last_sync: null,
    record_count: 0,
    health: 'offline',
    description: 'Income tax filing portal',
  },
];

export default function ConnectionsPage() {
  const [syncingIds, setSyncingIds] = useState(new Set());
  const [showConnectModal, setShowConnectModal] = useState(false);
  const [selectedPlatform, setSelectedPlatform] = useState(null);
  const [connectForm, setConnectForm] = useState({ api_key: '', api_secret: '', org_id: '' });
  const [connecting, setConnecting] = useState(false);
  const [connectionError, setConnectionError] = useState('');

  const {
    data: platformsData,
    loading,
    refetch,
  } = useFetch(useCallback(() => integrationApi.getPlatforms(), []), [], { initialData: null });

  const platforms = platformsData?.platforms || platformsData || demoPlatforms;

  const handleSync = async (platformId) => {
    setSyncingIds((prev) => new Set([...prev, platformId]));
    try {
      await integrationApi.syncData(platformId);
      refetch();
    } catch {
      // Sync attempted
    } finally {
      setTimeout(() => {
        setSyncingIds((prev) => {
          const next = new Set(prev);
          next.delete(platformId);
          return next;
        });
      }, 2000);
    }
  };

  const handleConnect = async () => {
    if (!selectedPlatform) return;
    setConnecting(true);
    setConnectionError('');
    try {
      await integrationApi.connectPlatform(selectedPlatform.id, connectForm);
      setShowConnectModal(false);
      setConnectForm({ api_key: '', api_secret: '', org_id: '' });
      refetch();
    } catch (err) {
      setConnectionError(err.response?.data?.detail || err.message || 'Failed to connect platform');
    } finally {
      setConnecting(false);
    }
  };

  const handleDisconnect = async (platformId) => {
    try {
      await integrationApi.disconnectPlatform(platformId);
      refetch();
    } catch {
      // Disconnect attempted
    }
  };

  const healthIndicator = (health) => {
    switch (health) {
      case 'good':
        return <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 shadow-sm shadow-emerald-400/50" />;
      case 'warning':
        return <span className="w-2.5 h-2.5 rounded-full bg-amber-400 animate-pulse" />;
      default:
        return <span className="w-2.5 h-2.5 rounded-full bg-slate-500" />;
    }
  };

  if (loading) return <Loader text="Loading connections..." />;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900">Platform Connections</h2>
          <p className="text-sm text-slate-500 mt-1">
            Manage your data source connections and sync status
          </p>
        </div>
        <Button
          icon={Plus}
          onClick={() => {
            setSelectedPlatform(null);
            setConnectionError('');
            setShowConnectModal(true);
          }}
        >
          Add Connection
        </Button>
      </div>

      {/* Stats Bar */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        {[
          { label: 'Total Platforms', value: platforms.length, icon: Database, color: 'text-brand-cyan' },
          { label: 'Connected', value: platforms.filter((p) => p.status === 'connected').length, icon: Wifi, color: 'text-emerald-400' },
          { label: 'Syncing', value: platforms.filter((p) => p.status === 'syncing').length, icon: RefreshCw, color: 'text-amber-400' },
          { label: 'Disconnected', value: platforms.filter((p) => p.status === 'disconnected').length, icon: WifiOff, color: 'text-slate-400' },
        ].map((stat, idx) => (
          <div key={idx} className="glass-card p-4 flex items-center gap-3">
            <stat.icon className={`w-5 h-5 ${stat.color}`} />
            <div>
              <p className="text-2xl font-bold text-slate-900">{stat.value}</p>
              <p className="text-xs text-slate-500">{stat.label}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Connection Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {platforms.map((platform, idx) => {
          const isSyncing = syncingIds.has(platform.id) || platform.status === 'syncing';

          return (
            <div
              key={platform.id}
              className="glass-card-hover p-6 animate-slide-up"
              style={{ animationDelay: `${idx * 80}ms` }}
            >
              {/* Card Header */}
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div
                    className="w-12 h-12 rounded-xl flex items-center justify-center text-2xl"
                    style={{ backgroundColor: `${platform.color}15` }}
                  >
                    {platform.icon}
                  </div>
                  <div>
                    <h3 className="text-base font-semibold text-slate-900">{platform.name}</h3>
                    <p className="text-xs text-slate-500">{platform.description}</p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  {healthIndicator(platform.health)}
                  <StatusBadge status={platform.status} size="sm" />
                </div>
              </div>

              {/* Stats */}
              <div className="grid grid-cols-2 gap-3 mb-5">
                <div className="p-3 rounded-xl bg-slate-50 border border-slate-100">
                  <div className="flex items-center gap-1.5 text-slate-500 mb-1">
                    <Clock className="w-3.5 h-3.5" />
                    <span className="text-xs">Last Sync</span>
                  </div>
                  <p className="text-sm font-medium text-slate-900">
                    {platform.last_sync ? formatRelativeTime(platform.last_sync) : 'Never'}
                  </p>
                </div>
                <div className="p-3 rounded-xl bg-slate-50 border border-slate-100">
                  <div className="flex items-center gap-1.5 text-slate-500 mb-1">
                    <Database className="w-3.5 h-3.5" />
                    <span className="text-xs">Records</span>
                  </div>
                  <p className="text-sm font-medium text-slate-900">
                    {platform.record_count?.toLocaleString('en-IN') || '0'}
                  </p>
                </div>
              </div>

              {/* Actions */}
              <div className="flex items-center gap-2">
                {platform.status === 'connected' || platform.status === 'syncing' ? (
                  <>
                    <Button
                      variant="outline"
                      size="sm"
                      icon={RefreshCw}
                      loading={isSyncing}
                      onClick={() => handleSync(platform.id)}
                      className="flex-1"
                    >
                      {isSyncing ? 'Syncing...' : 'Sync Now'}
                    </Button>
                    <Button
                      variant="danger"
                      size="sm"
                      icon={Unplug}
                      onClick={() => handleDisconnect(platform.id)}
                    >
                      Disconnect
                    </Button>
                  </>
                ) : (
                  <Button
                    size="sm"
                    icon={Zap}
                    onClick={() => {
                      setSelectedPlatform(platform);
                      setConnectionError('');
                      setShowConnectModal(true);
                    }}
                    className="flex-1"
                  >
                    Connect
                  </Button>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Add Connection Modal */}
      <Modal
        isOpen={showConnectModal}
        onClose={() => setShowConnectModal(false)}
        title="Connect Platform"
        subtitle={selectedPlatform ? `Configure ${selectedPlatform.name} connection` : 'Select a platform to connect'}
        footer={
          selectedPlatform && (
            <>
              <Button variant="ghost" onClick={() => setShowConnectModal(false)}>Cancel</Button>
              <Button loading={connecting} onClick={handleConnect}>Connect Platform</Button>
            </>
          )
        }
      >
        {!selectedPlatform ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {PLATFORM_LIST.map((platform) => (
              <button
                key={platform.id}
                onClick={() => setSelectedPlatform(platform)}
                className="flex items-center gap-3 p-4 rounded-xl bg-white border border-slate-200
                  hover:bg-slate-50 hover:border-slate-300 transition-all duration-200 text-left"
              >
                <span className="text-2xl">{platform.icon}</span>
                <div>
                  <p className="text-sm font-medium text-slate-900">{platform.name}</p>
                  <p className="text-xs text-slate-500">{platform.description}</p>
                </div>
              </button>
            ))}
          </div>
        ) : (
          <div className="space-y-4">
            {connectionError && (
              <div className="p-3 bg-rose-50 border border-rose-200 text-rose-600 rounded-xl text-sm">
                {connectionError}
              </div>
            )}
            <div className="flex items-center gap-3 p-4 rounded-xl bg-slate-50 border border-slate-200 mb-6">
              <span className="text-2xl">{selectedPlatform.icon}</span>
              <div>
                <p className="text-sm font-medium text-slate-900">{selectedPlatform.name}</p>
                <p className="text-xs text-slate-500">{selectedPlatform.description}</p>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">API Key</label>
              <input
                type="text"
                value={connectForm.api_key}
                onChange={(e) => setConnectForm({ ...connectForm, api_key: e.target.value })}
                placeholder="Enter your API key"
                className="input-dark"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">API Secret</label>
              <input
                type="password"
                value={connectForm.api_secret}
                onChange={(e) => setConnectForm({ ...connectForm, api_secret: e.target.value })}
                placeholder="Enter your API secret"
                className="input-dark"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Organization ID</label>
              <input
                type="text"
                value={connectForm.org_id}
                onChange={(e) => setConnectForm({ ...connectForm, org_id: e.target.value })}
                placeholder="Enter your organization ID"
                className="input-dark"
              />
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
}
