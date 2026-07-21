import { apiClient as axios } from '@/lib/axios';
import { SubscriptionPlan, PlanFormData, PlanStatus, PlanStats } from '@/types/plan';

export const planService = {
  getPlans: async (params?: { search?: string; status?: PlanStatus; page?: number; limit?: number }) => {
    const response = await axios.get<{ data: SubscriptionPlan[]; total: number }>(
      '/api/v1/admin/subscription-plans',
      { params }
    );
    return response.data;
  },

  getStats: async () => {
    const response = await axios.get<PlanStats>('/api/v1/admin/subscription-plans/stats');
    return response.data;
  },

  createPlan: async (data: PlanFormData) => {
    const response = await axios.post<SubscriptionPlan>('/api/v1/admin/subscription-plans', data);
    return response.data;
  },

  updatePlan: async (id: string, data: Partial<PlanFormData>) => {
    const response = await axios.put<SubscriptionPlan>(`/api/v1/admin/subscription-plans/${id}`, data);
    return response.data;
  },

  updateStatus: async (id: string, status: PlanStatus) => {
    const response = await axios.patch<SubscriptionPlan>(
      `/api/v1/admin/subscription-plans/${id}/status`,
      { status }
    );
    return response.data;
  },
};