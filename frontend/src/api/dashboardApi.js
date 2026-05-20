import api from './axiosConfig';

export const dashboardApi = {
  getSummary: async () => {
    const response = await api.get('/dashboard/summary');
    return response.data;
  },

  getRecentTransactions: async (limit = 10) => {
    const response = await api.get('/dashboard/recent-transactions', {
      params: { limit },
    });
    return response.data;
  },

  getPlatformBreakdown: async () => {
    const response = await api.get('/dashboard/platform-breakdown');
    return response.data;
  },

  getRevenueTrend: async (months = 12) => {
    const response = await api.get('/dashboard/charts/revenue-trend', {
      params: { months },
    });
    return response.data;
  },

  getExpenseBreakdown: async () => {
    const response = await api.get('/dashboard/charts/expense-breakdown');
    return response.data;
  },
};

export default dashboardApi;
