import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { planService } from '@/services/plan.service';
import { PlanFormData, PlanStatus } from '@/types/plan';

export function usePlans(params?: { search?: string; status?: PlanStatus }) {
  return useQuery({
    queryKey: ['plans', params],
    queryFn: () => planService.getPlans(params),
  });
}

export function usePlanStats() {
  return useQuery({
    queryKey: ['plan-stats'],
    queryFn: () => planService.getStats(),
  });
}

export function usePlanMutations() {
  const queryClient = useQueryClient();

  const createPlan = useMutation({
    mutationFn: (data: PlanFormData) => planService.createPlan(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['plans'] });
      queryClient.invalidateQueries({ queryKey: ['plan-stats'] });
    },
  });

  const updatePlan = useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<PlanFormData> }) =>
      planService.updatePlan(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['plans'] });
    },
  });

  const transitionStatus = useMutation({
    mutationFn: ({ id, status }: { id: string; status: PlanStatus }) =>
      planService.updateStatus(id, status),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['plans'] });
      queryClient.invalidateQueries({ queryKey: ['plan-stats'] });
    },
  });

  return { createPlan, updatePlan, transitionStatus };
}