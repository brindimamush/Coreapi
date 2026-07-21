export type PlanStatus = 'DRAFT' | 'ACTIVE' | 'INACTIVE' | 'ARCHIVED';

export interface SubscriptionPlan {
  id: string;
  name: string;
  slug: string;
  description?: string;
  price: string;
  currency: string;
  duration_days: number;
  max_api_keys: number | null;
  max_services: number | null;
  max_monthly_invoices: number | null;
  status: PlanStatus;
  display_order: number;
  created_at: string;
  updated_at: string;
}

export interface PlanFormData {
  name: string;
  description?: string;
  price: number;
  currency: string;
  duration_days: number;
  max_api_keys?: number | null;
  max_services?: number | null;
  max_monthly_invoices?: number | null;
  display_order: number;
}

export interface PlanStats {
  totalPlans: number;
  activePlans: number;
  draftPlans: number;
  archivedPlans: number;
}