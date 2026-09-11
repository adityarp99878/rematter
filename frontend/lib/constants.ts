export const MATERIAL_CATEGORIES = [
  { value: 'brick', label: 'Brick', icon: '🧱', color: '#dc2626' },
  { value: 'steel_beam', label: 'Steel I-Beam', icon: '🔩', color: '#6b7280' },
  { value: 'wood/door', label: 'Wooden Door', icon: '🚪', color: '#78350f' },
  { value: 'wood', label: 'Wood / Timber', icon: '🪵', color: '#92400e' },
  { value: 'window', label: 'Window', icon: '🪟', color: '#0891b2' },
  { value: 'glass', label: 'Glass', icon: '🪟', color: '#0891b2' },
  { value: 'tile', label: 'Tile', icon: '🏗️', color: '#7c3aed' },
  { value: 'concrete', label: 'Concrete', icon: '🪨', color: '#57534e' },
  { value: 'pipe', label: 'Pipe', icon: '🔧', color: '#ea580c' },
  { value: 'granite', label: 'Granite', icon: '💎', color: '#1e293b' },
  { value: 'bamboo', label: 'Bamboo', icon: '🎋', color: '#16a34a' },
  { value: 'roof_tile', label: 'Roof Tile', icon: '🏠', color: '#b45309' },
];

export const KERALA_CITIES = [
  'Thrissur', 'Kochi', 'Palakkad', 'Kozhikode', 'Thiruvananthapuram',
  'Kannur', 'Kollam', 'Alappuzha', 'Malappuram', 'Kottayam',
];

export const CONDITION_OPTIONS = [
  { value: 'excellent', label: 'Excellent', color: '#10b981' },
  { value: 'good', label: 'Good', color: '#22d3ee' },
  { value: 'fair', label: 'Fair', color: '#f59e0b' },
  { value: 'poor', label: 'Poor', color: '#ef4444' },
];

export const STATUS_COLORS: Record<string, string> = {
  available: '#10b981', draft: '#64748b', assessed: '#3b82f6',
  matched: '#8b5cf6', sold: '#f59e0b', delivered: '#06b6d4',
  recommended: '#10b981', accepted: '#3b82f6', pending: '#f59e0b',
  completed: '#10b981', active: '#10b981',
};

export const LIFECYCLE_STAGES = [
  'recovered', 'assessed', 'passport_created', 'listed', 'matched', 'sold', 'delivered', 'reused',
];
