'use client';

import { useState } from 'react';
import { usePlans, usePlanStats, usePlanMutations } from '@/features/plans/hooks/use-plans';
import { PlanFormData, PlanStatus, SubscriptionPlan } from '@/types/plan';
import { Plus, Search, CheckCircle, Archive, AlertCircle, Layers } from 'lucide-react';

export default function PlansPage() {
  const [search, setSearch] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);

  const { data: plansData, isLoading } = usePlans({ search });
  const { data: stats } = usePlanStats();
  const { createPlan, transitionStatus } = usePlanMutations();

  // ONLY declare this ONCE, inside the component, and include <PlanFormData>
  const [formData, setFormData] = useState<PlanFormData>({
    name: '',
    description: '',
    price: 199,
    currency: 'ETB',
    duration_days: 30,
    max_api_keys: 1,
    max_services: 2,
    max_monthly_invoices: 500,
    display_order: 1,
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await createPlan.mutateAsync(formData);
    setIsModalOpen(false);
  };

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Subscription Plans</h1>
          <p className="text-sm text-gray-500">Configure catalog limits and availability for merchants.</p>
        </div>
        <button
          onClick={() => setIsModalOpen(true)}
          className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-700"
        >
          <Plus className="w-4 h-4" /> Create Plan
        </button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="border p-4 rounded-xl bg-card">
          <p className="text-sm font-medium text-gray-500">Total Plans</p>
          <p className="text-2xl font-bold mt-1">{stats?.totalPlans ?? 0}</p>
        </div>
        <div className="border p-4 rounded-xl bg-card">
          <p className="text-sm font-medium text-green-600">Active Plans</p>
          <p className="text-2xl font-bold mt-1">{stats?.activePlans ?? 0}</p>
        </div>
        <div className="border p-4 rounded-xl bg-card">
          <p className="text-sm font-medium text-yellow-600">Draft Plans</p>
          <p className="text-2xl font-bold mt-1">{stats?.draftPlans ?? 0}</p>
        </div>
        <div className="border p-4 rounded-xl bg-card">
          <p className="text-sm font-medium text-gray-400">Archived</p>
          <p className="text-2xl font-bold mt-1">{stats?.archivedPlans ?? 0}</p>
        </div>
      </div>

      {/* Table */}
      <div className="border rounded-xl bg-card overflow-hidden">
        <table className="w-full text-left text-sm">
          <thead className="bg-gray-50 border-b text-gray-600">
            <tr>
              <th className="p-4">Name</th>
              <th className="p-4">Price</th>
              <th className="p-4">Duration</th>
              <th className="p-4">Status</th>
              <th className="p-4">Order</th>
              <th className="p-4 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y">
            {plansData?.data.map((plan: SubscriptionPlan) => (
              <tr key={plan.id}>
                <td className="p-4 font-medium">{plan.name}</td>
                <td className="p-4">{plan.price} {plan.currency}</td>
                <td className="p-4">{plan.duration_days} Days</td>
                <td className="p-4">
                  <span className={`px-2.5 py-1 text-xs font-semibold rounded-full ${
                    plan.status === 'ACTIVE' ? 'bg-green-100 text-green-800' :
                    plan.status === 'DRAFT' ? 'bg-yellow-100 text-yellow-800' :
                    plan.status === 'INACTIVE' ? 'bg-gray-100 text-gray-800' :
                    'bg-red-100 text-red-800'
                  }`}>
                    {plan.status}
                  </span>
                </td>
                <td className="p-4">{plan.display_order}</td>
                <td className="p-4 text-right gap-2 flex justify-end">
                  {plan.status === 'DRAFT' && (
                    <button
                      onClick={() => transitionStatus.mutate({ id: plan.id, status: 'ACTIVE' })}
                      className="px-3 py-1 bg-green-50 text-green-600 rounded-md text-xs font-medium hover:bg-green-100"
                    >
                      Publish
                    </button>
                  )}
                  {plan.status === 'ACTIVE' && (
                    <button
                      onClick={() => transitionStatus.mutate({ id: plan.id, status: 'INACTIVE' })}
                      className="px-3 py-1 bg-yellow-50 text-yellow-600 rounded-md text-xs font-medium hover:bg-yellow-100"
                    >
                      Disable
                    </button>
                  )}
                  {plan.status === 'INACTIVE' && (
                    <button
                      onClick={() => transitionStatus.mutate({ id: plan.id, status: 'ACTIVE' })}
                      className="px-3 py-1 bg-green-50 text-green-600 rounded-md text-xs font-medium hover:bg-green-100"
                    >
                      Re-enable
                    </button>
                  )}
                  {plan.status !== 'ARCHIVED' && (
                    <button
                      onClick={() => transitionStatus.mutate({ id: plan.id, status: 'ARCHIVED' })}
                      className="px-3 py-1 bg-red-50 text-red-600 rounded-md text-xs font-medium hover:bg-red-100"
                    >
                      Archive
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Creation Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-xl p-6 max-w-md w-full space-y-4">
            <h2 className="text-lg font-bold">Create New Plan</h2>
            <form onSubmit={handleSubmit} className="space-y-3">
              <input
                type="text"
                placeholder="Plan Name"
                required
                className="w-full border p-2 rounded-md text-sm"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              />
              <div className="grid grid-cols-2 gap-2">
                <input
                  type="number"
                  placeholder="Price"
                  required
                  className="border p-2 rounded-md text-sm"
                  value={formData.price}
                  onChange={(e) => setFormData({ ...formData, price: Number(e.target.value) })}
                />
                <input
                  type="number"
                  placeholder="Duration (Days)"
                  required
                  className="border p-2 rounded-md text-sm"
                  value={formData.duration_days}
                  onChange={(e) => setFormData({ ...formData, duration_days: Number(e.target.value) })}
                />
              </div>
              <div className="grid grid-cols-3 gap-2">
                <input
                  type="number"
                  placeholder="Max Keys"
                  className="border p-2 rounded-md text-sm"
                  value={formData.max_api_keys ?? ''}
                  onChange={(e) => setFormData({ ...formData, max_api_keys: e.target.value ? Number(e.target.value) : null })}
                />
                <input
                  type="number"
                  placeholder="Max Services"
                  className="border p-2 rounded-md text-sm"
                  value={formData.max_services ?? ''}
                  onChange={(e) => setFormData({ ...formData, max_services: e.target.value ? Number(e.target.value) : null })}
                />
                <input
                  type="number"
                  placeholder="Max Invoices"
                  className="border p-2 rounded-md text-sm"
                  value={formData.max_monthly_invoices ?? ''}
                  onChange={(e) => setFormData({ ...formData, max_monthly_invoices: e.target.value ? Number(e.target.value) : null })}
                />
              </div>
              <div className="flex justify-end gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="px-4 py-2 border rounded-md text-sm"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 text-white rounded-md text-sm"
                >
                  Save Draft
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}