/**
 * Format a number as Indian Rupee currency
 */
export const formatCurrency = (amount) => {
  if (amount === null || amount === undefined) return '₹0';
  
  const num = Number(amount);
  if (isNaN(num)) return '₹0';

  // Indian numbering system
  const formatter = new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    minimumFractionDigits: 0,
    maximumFractionDigits: 2,
  });

  return formatter.format(num);
};

/**
 * Format a number with commas (Indian system)
 */
export const formatNumber = (num) => {
  if (num === null || num === undefined) return '0';
  return new Intl.NumberFormat('en-IN').format(Number(num));
};

/**
 * Format large numbers with abbreviations
 */
export const formatCompactNumber = (num) => {
  if (num === null || num === undefined) return '0';
  const n = Number(num);
  if (n >= 10000000) return `₹${(n / 10000000).toFixed(2)} Cr`;
  if (n >= 100000) return `₹${(n / 100000).toFixed(2)} L`;
  if (n >= 1000) return `₹${(n / 1000).toFixed(1)} K`;
  return `₹${n}`;
};

/**
 * Helper to ensure naive ISO strings are parsed as UTC
 */
const ensureUTC = (dateString) => {
  if (typeof dateString === 'string' && dateString.includes('T') && !dateString.endsWith('Z') && !dateString.match(/[+-]\d{2}:?\d{2}$/)) {
    return dateString + 'Z';
  }
  return dateString;
};

/**
 * Format a date string
 */
export const formatDate = (dateString, options = {}) => {
  if (!dateString) return '—';
  
  const defaultOptions = {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    ...options,
  };

  try {
    return new Date(ensureUTC(dateString)).toLocaleDateString('en-IN', defaultOptions);
  } catch {
    return dateString;
  }
};

/**
 * Format date with time
 */
export const formatDateTime = (dateString) => {
  if (!dateString) return '—';
  try {
    return new Date(ensureUTC(dateString)).toLocaleString('en-IN', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  } catch {
    return dateString;
  }
};

/**
 * Format relative time (e.g., "2 hours ago")
 */
export const formatRelativeTime = (dateString) => {
  if (!dateString) return '—';
  
  const date = new Date(ensureUTC(dateString));
  const now = new Date();
  const diffMs = now - date;
  const diffSecs = Math.floor(diffMs / 1000);
  const diffMins = Math.floor(diffSecs / 60);
  const diffHours = Math.floor(diffMins / 60);
  const diffDays = Math.floor(diffHours / 24);

  if (diffSecs < 60) return 'Just now';
  if (diffMins < 60) return `${diffMins}m ago`;
  if (diffHours < 24) return `${diffHours}h ago`;
  if (diffDays < 7) return `${diffDays}d ago`;
  
  return formatDate(dateString);
};

/**
 * Truncate text with ellipsis
 */
export const truncateText = (text, maxLength = 50) => {
  if (!text) return '';
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '…';
};

/**
 * Get percentage change indicator
 */
export const getChangeIndicator = (current, previous) => {
  if (!previous || previous === 0) return { value: 0, isPositive: true };
  const change = ((current - previous) / previous) * 100;
  return {
    value: Math.abs(change).toFixed(1),
    isPositive: change >= 0,
  };
};
