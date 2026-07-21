'use client';

import {
  flexRender,
  getCoreRowModel,
  useReactTable,
  ColumnDef,
} from '@tanstack/react-table';
import { Search, Eye } from 'lucide-react';
import { Merchant } from '@/types/merchant';
import { format } from 'date-fns';

interface Props {
  data: Merchant[];
  isLoading: boolean;
  search: string;
  onSearchChange: (val: string) => void;
  onSelectMerchant: (id: string) => void;
}

export function MerchantTable({
  data,
  isLoading,
  search,
  onSearchChange,
  onSelectMerchant,
}: Props) {
  const columns: ColumnDef<Merchant>[] = [
    {
      accessorKey: 'business_name',
      header: 'Business Name',
      cell: (info) => <span className="font-medium">{info.getValue<string>()}</span>,
    },
    {
      accessorKey: 'business_email',
      header: 'Email',
    },
    {
      accessorKey: 'phone_number',
      header: 'Phone',
    },
    {
      accessorKey: 'telebirr_phone',
      header: 'Telebirr Phone',
    },
    {
      accessorKey: 'status',
      header: 'Status',
      cell: (info) => (
        <span className="rounded-full bg-emerald-100 px-2.5 py-0.5 text-xs font-medium text-emerald-800">
          {info.getValue<string>()}
        </span>
      ),
    },
    {
      accessorKey: 'created_at',
      header: 'Registered At',
      cell: (info) => format(new Date(info.getValue<string>()), 'dd MMM yyyy'),
    },
    {
      id: 'actions',
      header: 'Actions',
      cell: ({ row }) => (
        <button
          onClick={() => onSelectMerchant(row.original.id)}
          className="flex items-center gap-1.5 rounded-md px-2.5 py-1.5 text-xs font-medium text-primary hover:bg-primary/10"
        >
          <Eye className="h-3.5 w-3.5" /> View
        </button>
      ),
    },
  ];

  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div className="relative w-72">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <input
            type="text"
            placeholder="Search merchants..."
            value={search}
            onChange={(e) => onSearchChange(e.target.value)}
            className="w-full rounded-md border bg-background pl-9 pr-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
          />
        </div>
      </div>

      <div className="rounded-lg border bg-card shadow-sm">
        <table className="w-full text-left text-sm">
          <thead className="border-b bg-muted/50 text-xs text-muted-foreground">
            {table.getHeaderGroups().map((headerGroup) => (
              <tr key={headerGroup.id}>
                {headerGroup.headers.map((header) => (
                  <th key={header.id} className="p-4 font-semibold">
                    {flexRender(header.column.columnDef.header, header.getContext())}
                  </th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody className="divide-y">
            {isLoading ? (
              <tr>
                <td colSpan={columns.length} className="p-4 text-center text-muted-foreground">
                  Loading merchants...
                </td>
              </tr>
            ) : table.getRowModel().rows.length === 0 ? (
              <tr>
                <td colSpan={columns.length} className="p-4 text-center text-muted-foreground">
                  No merchants found.
                </td>
              </tr>
            ) : (
              table.getRowModel().rows.map((row) => (
                <tr key={row.id} className="hover:bg-muted/50 transition-colors">
                  {row.getVisibleCells().map((cell) => (
                    <td key={cell.id} className="p-4">
                      {flexRender(cell.column.columnDef.cell, cell.getContext())}
                    </td>
                  ))}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}