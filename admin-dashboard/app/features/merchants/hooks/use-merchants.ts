import { useQuery } from '@tanstack/react-query';
import { merchantService } from '@/services/merchant.service';

export function useMerchants(params: { page: number; limit: number; search: string }) {
  return useQuery({
    queryKey: ['merchants', params],
    queryFn: () => merchantService.getMerchants(params),
  });
}

export function useMerchantDetails(id: string | null) {
  return useQuery({
    queryKey: ['merchant', id],
    queryFn: () => merchantService.getMerchantById(id!),
    enabled: !!id,
  });
}

export function useMerchantStats() {
  return useQuery({
    queryKey: ['merchant-stats'],
    queryFn: merchantService.getStats,
  });
}