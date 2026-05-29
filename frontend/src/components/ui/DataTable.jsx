import { useState, useMemo, useEffect } from 'react';
import { ChevronUp, ChevronDown, ChevronLeft, ChevronRight, Inbox } from 'lucide-react';

export default function DataTable({
  columns = [],
  data = [],
  pageSize = 10,
  sortable = true,
  striped = true,
  emptyMessage = 'No data available',
  emptyIcon: EmptyIcon = Inbox,
  onRowClick,
  className = '',
  // Server-side pagination props
  serverSide = false,
  totalItems = 0,
  currentPage = 1,
  onPageChange,
  onPageSizeChange,
}) {
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' });
  
  // Local state for client-side pagination
  const [localPage, setLocalPage] = useState(1);
  const [localPageSize, setLocalPageSize] = useState(pageSize);

  // Synchronize local page size with prop if it changes initially
  useEffect(() => {
    if (!serverSide) setLocalPageSize(pageSize);
  }, [pageSize, serverSide]);

  const activePage = serverSide ? currentPage : localPage;
  const activePageSize = serverSide ? pageSize : localPageSize;
  const activeTotal = serverSide ? totalItems : data.length;

  // Sorting (Only applied client-side if not serverSide)
  const sortedData = useMemo(() => {
    if (serverSide) return data; // Server handles sorting
    if (!sortConfig.key) return data;
    return [...data].sort((a, b) => {
      const aVal = a[sortConfig.key];
      const bVal = b[sortConfig.key];
      if (aVal === bVal) return 0;
      if (aVal === null || aVal === undefined) return 1;
      if (bVal === null || bVal === undefined) return -1;
      const compare = aVal < bVal ? -1 : 1;
      return sortConfig.direction === 'asc' ? compare : -compare;
    });
  }, [data, sortConfig, serverSide]);

  // Pagination
  const totalPages = Math.ceil(activeTotal / activePageSize);
  
  const paginatedData = serverSide 
    ? data 
    : sortedData.slice(
        (activePage - 1) * activePageSize,
        activePage * activePageSize
      );

  const handleSort = (key) => {
    if (!sortable) return;
    setSortConfig((prev) => ({
      key,
      direction: prev.key === key && prev.direction === 'asc' ? 'desc' : 'asc',
    }));
  };

  const handlePageChange = (newPage) => {
    if (serverSide && onPageChange) {
      onPageChange(newPage);
    } else {
      setLocalPage(newPage);
    }
  };

  const handlePageSizeChange = (e) => {
    const newSize = Number(e.target.value);
    if (serverSide && onPageSizeChange) {
      onPageSizeChange(newSize);
    } else {
      setLocalPageSize(newSize);
      setLocalPage(1); // Reset to first page
    }
  };

  const SortIcon = ({ columnKey }) => {
    if (sortConfig.key !== columnKey) {
      return <ChevronUp className="w-3 h-3 text-slate-600" />;
    }
    return sortConfig.direction === 'asc' ? (
      <ChevronUp className="w-3 h-3 text-brand-cyan" />
    ) : (
      <ChevronDown className="w-3 h-3 text-brand-cyan" />
    );
  };

  // Empty state
  if (!data || data.length === 0) {
    return (
      <div className={`glass-card p-12 text-center ${className}`}>
        <EmptyIcon className="w-12 h-12 text-slate-400 mx-auto mb-4" />
        <p className="text-slate-500 text-sm">{emptyMessage}</p>
      </div>
    );
  }

  return (
    <div className={`glass-card overflow-hidden ${className}`}>
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-slate-200">
              {columns.map((col) => (
                <th
                  key={col.key}
                  onClick={() => col.sortable !== false && handleSort(col.key)}
                  className={`px-5 py-3.5 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider
                    ${sortable && col.sortable !== false ? 'cursor-pointer hover:text-slate-700 select-none' : ''}
                    ${col.align === 'right' ? 'text-right' : ''}
                    ${col.align === 'center' ? 'text-center' : ''}`}
                >
                  <div className={`flex items-center gap-1 
                    ${col.align === 'right' ? 'justify-end' : ''}
                    ${col.align === 'center' ? 'justify-center' : ''}`}>
                    {col.label}
                    {sortable && col.sortable !== false && !serverSide && <SortIcon columnKey={col.key} />}
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {paginatedData.map((row, idx) => (
              <tr
                key={row.id || idx}
                onClick={() => onRowClick?.(row)}
                className={`border-b border-slate-100 transition-colors duration-150
                  ${onRowClick ? 'cursor-pointer' : ''}
                  ${striped && idx % 2 === 1 ? 'bg-slate-50' : ''}
                  hover:bg-slate-100`}
              >
                {columns.map((col) => (
                  <td
                    key={col.key}
                    className={`px-5 py-3.5 text-sm text-slate-700
                      ${col.align === 'right' ? 'text-right' : ''}
                      ${col.align === 'center' ? 'text-center' : ''}`}
                  >
                    {col.render ? col.render(row[col.key], row) : row[col.key]}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination & Footer Controls */}
      <div className="flex flex-col sm:flex-row items-center justify-between px-5 py-3 border-t border-slate-200 gap-4">
        
        <div className="flex items-center gap-3">
          <p className="text-xs text-slate-500">
            Showing {((activePage - 1) * activePageSize) + 1}–{Math.min(activePage * activePageSize, activeTotal)} of {activeTotal}
          </p>
          
          <div className="flex items-center gap-2 border-l border-slate-200 pl-3">
            <span className="text-xs text-slate-500">Rows per page:</span>
            <select 
              value={activePageSize}
              onChange={handlePageSizeChange}
              className="text-xs bg-slate-50 border border-slate-200 rounded-lg px-2 py-1 outline-none focus:border-brand-cyan"
            >
              {[10, 25, 50, 100, 200].map(size => (
                <option key={size} value={size}>{size}</option>
              ))}
            </select>
          </div>
        </div>

        {totalPages > 1 && (
          <div className="flex items-center gap-1">
            <button
              onClick={() => handlePageChange(Math.max(1, activePage - 1))}
              disabled={activePage === 1}
              className="p-1.5 rounded-lg text-slate-500 hover:text-slate-900 hover:bg-slate-100 
                disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            
            {/* Logic to show a sliding window of pages could go here. For now, simple array */}
            {Array.from({ length: totalPages }, (_, i) => i + 1)
              .filter(page => page === 1 || page === totalPages || (page >= activePage - 1 && page <= activePage + 1))
              .map((page, index, array) => {
                // Add ellipsis if gap
                if (index > 0 && page - array[index - 1] > 1) {
                  return (
                    <span key={`ellipsis-${page}`} className="px-2 text-slate-400">...</span>
                  );
                }
                return (
                  <button
                    key={page}
                    onClick={() => handlePageChange(page)}
                    className={`w-8 h-8 rounded-lg text-xs font-medium transition-colors
                      ${activePage === page
                        ? 'bg-brand-cyan/20 text-brand-cyan'
                        : 'text-slate-500 hover:text-slate-900 hover:bg-slate-100'}`}
                  >
                    {page}
                  </button>
                );
              })}
              
            <button
              onClick={() => handlePageChange(Math.min(totalPages, activePage + 1))}
              disabled={activePage === totalPages}
              className="p-1.5 rounded-lg text-slate-500 hover:text-slate-900 hover:bg-slate-100 
                disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
