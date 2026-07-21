'use client';

import { useState } from 'react';
import { useMerchants, useMerchantStats } from '@/features/merchants/hooks/use-merchants';
import { MerchantTable } from '@/features/merchants/components/merchant-table';
import { MerchantStatsOverview } from '@/features/merchants/components/merchant-stats';
import { MerchantDetailsSheet } from '@/features/merchants/components/merchant-details-sheet';

export default function MerchantsPage() {
  const [page] = useState(1);
  const [search, setSearch] = useState('');
  const [selectedMerchantId, setSelectedMerchantId] = useState<string | null>(null);

  const { data: merchantData, isLoading: isMerchantsLoading } = useMerchants({
    page,
    limit: 10,
    search,
  });

  const { data: statsData, isLoading: isStatsLoading } = useMerchantStats();

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Merchant Management</h1>
        <p className="text-sm text-muted-foreground">
          Monitor registered merchants and platform usage statistics.
        </p>
      </div>

      <MerchantStatsOverview stats={statsData} isLoading={isStatsLoading} />

      <MerchantTable
        data={merchantData?.data || []}
        isLoading={isMerchantsLoading}
        search={search}
        onSearchChange={setSearch}
        onSelectMerchant={(id) => setSelectedMerchantId(id)}
      />

      <MerchantDetailsSheet
        merchantId={selectedMerchantId}
        onClose={() => setSelectedMerchantId(null)}
      />
    </div>
  );
}