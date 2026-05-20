import api from './axiosConfig';

export const integrationApi = {
  getPlatforms: async () => {
    const response = await api.get('/connections/');
    return response.data;
  },

  connectPlatform: async (platformId, credentials) => {
    const response = await api.post(`/integrations/connect`, { 
      platform: platformId, 
      display_name: credentials.org_id || platformId,
      credentials 
    });
    return response.data;
  },

  disconnectPlatform: async (connectionId) => {
    const response = await api.delete(`/integrations/${connectionId}`);
    return response.data;
  },

  syncData: async (platformId) => {
    const response = await api.post(`/integrations/${platformId}/sync`);
    return response.data;
  },

  getData: async (platformId, params = {}) => {
    const response = await api.get(`/integrations/${platformId}/data`, { params });
    return response.data;
  },

  getConnectionStatus: async (platformId) => {
    const response = await api.get(`/integrations/${platformId}/status`);
    return response.data;
  },

  getSyncHistory: async (platformId) => {
    const response = await api.get(`/integrations/${platformId}/sync-history`);
    return response.data;
  },
};

export default integrationApi;
