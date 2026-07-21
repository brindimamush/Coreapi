import { apiClient } from '@/lib/axios';
import { Merchant, MerchantStats, PaginatedMerchantResponse } from '@/types/merchant';

export const merchantService = {
  getMerchants: async (params?: { page?: number; limit?: number; search?: string }) => {
    const response = await apiClient.get<PaginatedMerchantResponse>('/internal/merchants', { params });
    return response.data;
  },

  getMerchantById: async (id: string) => {
    const response = await apiClient.get<Merchant>(`/internal/merchants/${id}`);
    return response.data;
  },

  getStats: async () => {
    const response = await apiClient.get<MerchantStats>('/internal/merchants/stats');
    return response.data;
  },
};