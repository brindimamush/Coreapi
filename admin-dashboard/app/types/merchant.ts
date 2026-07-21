export type MerchantStatus = 'REGISTERING' | 'REGISTERED';

export interface Merchant {
  id: string;
  telegram_id: number;
  telegram_username?: string | null;
  telegram_first_name: string;
  telegram_last_name?: string | null;
  business_name: string;
  business_email: string;
  phone_number: string;
  telebirr_name: string;
  telebirr_phone: string;
  status: MerchantStatus;
  created_at: string;
  updated_at?: string;
}

export interface MerchantStats {
  totalMerchants: number;
  registeredToday: number;
  activeRate: number;
  registrationTrend: { date: string; count: number }[];
}

export interface PaginatedMerchantResponse {
  data: Merchant[];
  total: number;
  page: number;
  limit: number;
}