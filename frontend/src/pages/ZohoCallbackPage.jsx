import { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { CheckCircle2, XCircle } from 'lucide-react';
import Loader from '../components/ui/Loader';
import api from '../api/axiosConfig';
import toast from 'react-hot-toast';

export default function ZohoCallbackPage() {
  const [status, setStatus] = useState('processing');
  const [errorMsg, setErrorMsg] = useState('');
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const processCallback = async () => {
      const searchParams = new URLSearchParams(location.search);
      const code = searchParams.get('code');
      const state = searchParams.get('state') || 'in'; // e.g., location 'in', 'com'
      const error = searchParams.get('error');

      if (error) {
        setStatus('error');
        setErrorMsg(`Zoho returned an error: ${error}`);
        return;
      }

      if (!code) {
        setStatus('error');
        setErrorMsg('No authorization code received from Zoho.');
        return;
      }

      try {
        // Send to backend
        // We prompt the user for org_id quickly or extract it if stored in localStorage before redirect
        const orgId = localStorage.getItem('zoho_pending_org_id') || 'UNKNOWN';
        
        const response = await api.post('/integrations/zoho/callback', {
          code,
          location: state,
          org_id: orgId
        });

        if (response.data.success) {
          setStatus('success');
          toast.success('Successfully connected to Zoho Books!');
          setTimeout(() => {
            navigate('/connections');
          }, 2000);
        } else {
          throw new Error('Failed to connect');
        }
      } catch (err) {
        setStatus('error');
        setErrorMsg(err.response?.data?.detail || err.message || 'Failed to exchange token');
      }
    };

    processCallback();
  }, [location, navigate]);

  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh]">
      <div className="glass-card p-8 max-w-md w-full text-center space-y-4">
        {status === 'processing' && (
          <>
            <Loader text="Connecting to Zoho Books..." />
            <p className="text-sm text-slate-500 mt-4">Please wait while we secure your connection.</p>
          </>
        )}
        
        {status === 'success' && (
          <div className="flex flex-col items-center space-y-3">
            <CheckCircle2 className="w-16 h-16 text-emerald-500" />
            <h2 className="text-xl font-bold text-slate-900">Connection Successful!</h2>
            <p className="text-sm text-slate-500">Redirecting you back to connections...</p>
          </div>
        )}
        
        {status === 'error' && (
          <div className="flex flex-col items-center space-y-3">
            <XCircle className="w-16 h-16 text-rose-500" />
            <h2 className="text-xl font-bold text-slate-900">Connection Failed</h2>
            <p className="text-sm text-rose-500">{errorMsg}</p>
            <button 
              onClick={() => navigate('/connections')}
              className="mt-4 px-4 py-2 bg-slate-900 text-white rounded-lg text-sm font-medium hover:bg-slate-800 transition-colors"
            >
              Return to Connections
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
