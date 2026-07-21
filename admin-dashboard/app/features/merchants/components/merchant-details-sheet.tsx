'use client';

import { format } from 'date-fns';
import { X, Building2, Phone, Mail, Send, Smartphone } from 'lucide-react';
import { useMerchantDetails } from '../hooks/use-merchants';

interface Props {
  merchantId: string | null;
  onClose: () => void;
}

export function MerchantDetailsSheet({ merchantId, onClose }: Props) {
  const { data: merchant, isLoading } = useMerchantDetails(merchantId);

  if (!merchantId) return null;

  return (
    <div className="fixed inset-0 z-50 flex justify-end bg-black/50">
      <div className="h-full w-full max-w-md bg-background p-6 shadow-xl overflow-y-auto">
        <div className="flex items-center justify-between border-b pb-4">
          <h2 className="text-lg font-semibold">Merchant Profile</h2>
          <button onClick={onClose} className="rounded-lg p-1 hover:bg-muted">
            <X className="h-5 w-5" />
          </button>
        </div>

        {isLoading ? (
          <div className="mt-8 space-y-4">
            <div className="h-6 bg-muted animate-pulse rounded" />
            <div className="h-20 bg-muted animate-pulse rounded" />
          </div>
        ) : merchant ? (
          <div className="mt-6 space-y-6">
            <div>
              <span className="inline-block rounded-full bg-emerald-100 px-3 py-1 text-xs font-semibold text-emerald-800">
                {merchant.status}
              </span>
              <h3 className="mt-2 text-xl font-bold">{merchant.business_name}</h3>
              <p className="text-sm text-muted-foreground">ID: {merchant.id}</p>
            </div>

            <div className="space-y-4 rounded-lg border p-4">
              <div className="flex items-center gap-3 text-sm">
                <Mail className="h-4 w-4 text-muted-foreground" />
                <span>{merchant.business_email}</span>
              </div>
              <div className="flex items-center gap-3 text-sm">
                <Phone className="h-4 w-4 text-muted-foreground" />
                <span>{merchant.phone_number}</span>
              </div>
            </div>

            <div className="space-y-3">
              <h4 className="text-sm font-semibold text-muted-foreground">Telebirr Details</h4>
              <div className="rounded-lg bg-muted/50 p-4 space-y-2">
                <div className="flex items-center gap-2 text-sm">
                  <Smartphone className="h-4 w-4 text-primary" />
                  <span className="font-medium">Name:</span> {merchant.telebirr_name}
                </div>
                <div className="flex items-center gap-2 text-sm">
                  <Phone className="h-4 w-4 text-primary" />
                  <span className="font-medium">Number:</span> {merchant.telebirr_phone}
                </div>
              </div>
            </div>

            <div className="space-y-3">
              <h4 className="text-sm font-semibold text-muted-foreground">Telegram Identity</h4>
              <div className="rounded-lg bg-muted/50 p-4 space-y-2 text-sm">
                <p><span className="font-medium">Telegram ID:</span> {merchant.telegram_id}</p>
                <p><span className="font-medium">Name:</span> {merchant.telegram_first_name} {merchant.telegram_last_name || ''}</p>
                {merchant.telegram_username && (
                  <p><span className="font-medium">Username:</span> @{merchant.telegram_username}</p>
                )}
              </div>
            </div>

            <div className="border-t pt-4 text-xs text-muted-foreground">
              Registered on {format(new Date(merchant.created_at), 'PPP')}
            </div>
          </div>
        ) : null}
      </div>
    </div>
  );
}