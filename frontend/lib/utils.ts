import { clsx, type ClassValue } from 'clsx';

export function cn(...inputs: ClassValue[]) {
  return clsx(inputs);
}

export function formatCurrency(amount: number): string {
  if (amount >= 100000) return `₹${(amount / 100000).toFixed(1)}L`;
  if (amount >= 1000) return `₹${(amount / 1000).toFixed(1)}K`;
  return `₹${amount.toLocaleString('en-IN')}`;
}

export function formatCurrencyFull(amount: number): string {
  return `₹${amount.toLocaleString('en-IN', { maximumFractionDigits: 0 })}`;
}

export function formatWeight(kg: number): string {
  if (kg >= 1000) return `${(kg / 1000).toFixed(1)} t`;
  return `${kg.toFixed(0)} kg`;
}

export function formatDistance(km: number): string {
  return `${km.toFixed(0)} km`;
}

export function getScoreColor(score: number): string {
  if (score >= 80) return '#10b981';
  if (score >= 50) return '#f59e0b';
  return '#ef4444';
}

export function getScoreLabel(score: number): string {
  if (score >= 80) return 'High';
  if (score >= 50) return 'Moderate';
  return 'Low';
}

export function getConditionColor(condition: string): string {
  const map: Record<string, string> = {
    excellent: '#10b981', good: '#22d3ee', fair: '#f59e0b', poor: '#ef4444',
  };
  return map[condition] || '#94a3b8';
}

export function timeAgo(date: string): string {
  const seconds = Math.floor((Date.now() - new Date(date).getTime()) / 1000);
  if (seconds < 60) return 'just now';
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
  if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
  return `${Math.floor(seconds / 86400)}d ago`;
}

export function getMaterialIcon(type: string): string {
  const icons: Record<string, string> = {
    brick: '🧱', steel_beam: '🔩', steel: '🔩', wood: '🪵', 'wood/door': '🚪',
    door: '🚪', window: '🪟', glass: '🪟', tile: '🏗️', concrete: '🪨',
    pipe: '🔧', granite: '💎', bamboo: '🎋', roof_tile: '🏠',
  };
  return icons[type] || '📦';
}

export function getMaterialColor(type: string): string {
  const colors: Record<string, string> = {
    brick: '#dc2626', steel_beam: '#6b7280', steel: '#6b7280', wood: '#92400e',
    'wood/door': '#78350f', door: '#78350f', window: '#0891b2', glass: '#0891b2',
    tile: '#7c3aed', concrete: '#57534e', pipe: '#ea580c', granite: '#1e293b',
    bamboo: '#16a34a', roof_tile: '#b45309',
  };
  return colors[type] || '#64748b';
}
