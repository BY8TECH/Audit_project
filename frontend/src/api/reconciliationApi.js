import api from './axiosConfig';

export const reconciliationApi = {
  compare: async (sourceA, sourceB, dateRange) => {
    const response = await api.post('/reconciliation/compare', {
      source_a_platform: sourceA,
      source_b_platform: sourceB,
      date_from: dateRange?.from,
      date_to: dateRange?.to,
    });
    return response.data;
  },

  getMismatches: async (comparisonId) => {
    const response = await api.get(`/reconciliation/mismatches/${comparisonId}`);
    return response.data;
  },

  getReport: async (comparisonId, format = 'json') => {
    const response = await api.get(`/reconciliation/report/${comparisonId}`, {
      params: { format },
    });
    return response.data;
  },

  getHistory: async () => {
    const response = await api.get('/reconciliation/history');
    return response.data;
  },

  exportReport: async (comparisonId) => {
    const response = await api.get(`/reconciliation/export/${comparisonId}`, {
      responseType: 'blob',
    });
    return response.data;
  },
};

export default reconciliationApi;
