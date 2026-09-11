'use client';
import { useEffect, useState } from 'react';
import Link from 'next/link';
import { getMaterials } from '../../lib/api';
import { demoMaterials } from '../../lib/demo-data';
import { Material } from '../../lib/types';
import { formatCurrencyFull, getMaterialIcon, getScoreColor } from '../../lib/utils';
import { MATERIAL_CATEGORIES } from '../../lib/constants';

export default function MarketplacePage() {
  const [materials, setMaterials] = useState<Material[]>([]);
  const [filter, setFilter] = useState('');

  useEffect(() => {
    getMaterials().then(data => {
      if (data && data.materials) {
        setMaterials(data.materials);
      } else {
        setMaterials([]);
      }
    });
  }, []);

  const filtered = filter ? materials.filter(m => m.material_type === filter) : materials;

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 animate-fadeIn">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Material Marketplace</h1>
        <input type="text" placeholder="Search materials..." className="bg-slate-900 border border-slate-700 rounded-lg p-2 text-white w-64" />
      </div>
      
      <div className="flex gap-2 overflow-x-auto pb-4 mb-6 no-scrollbar">
        <button onClick={() => setFilter('')} className={`px-4 py-2 rounded-full whitespace-nowrap border ${!filter ? 'bg-emerald-500 text-white border-emerald-500' : 'bg-slate-800 border-slate-700 text-slate-300'}`}>
          All Materials
        </button>
        {MATERIAL_CATEGORIES.map(c => (
          <button key={c.value} onClick={() => setFilter(c.value)} className={`px-4 py-2 rounded-full whitespace-nowrap border flex items-center gap-2 ${filter === c.value ? 'bg-emerald-500 text-white border-emerald-500' : 'bg-slate-800 border-slate-700 text-slate-300 hover:bg-slate-700'}`}>
            <span>{c.icon}</span> {c.label}
          </button>
        ))}
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {filtered.map(m => (
          <Link href={`/materials/${m.id}`} key={m.id} className="bg-slate-800/40 border border-slate-700 rounded-xl overflow-hidden hover:border-emerald-500/50 hover:bg-slate-800 transition-all group glass">
            <div className="h-40 bg-slate-900 relative flex items-center justify-center border-b border-slate-700/50">
              <div className="text-7xl group-hover:scale-110 transition-transform">{getMaterialIcon(m.material_type)}</div>
              <div className="absolute top-2 right-2 bg-slate-900/80 border border-slate-700 text-xs font-bold px-2 py-1 rounded-full flex items-center gap-1" style={{ color: getScoreColor(m.reuse_score || 0) }}>
                Score: {m.reuse_score}
              </div>
            </div>
            <div className="p-4">
              <h3 className="font-bold text-lg mb-1 group-hover:text-emerald-400 transition-colors capitalize">{m.material_type.replace('_', ' ')}</h3>
              <div className="text-sm text-slate-400 mb-2">{m.quantity} {m.unit} • {m.location}</div>
              <div className="flex justify-between items-center mt-4 pt-4 border-t border-slate-700/50">
                <span className="font-bold text-white text-lg">{formatCurrencyFull(m.estimated_value || 0)}</span>
                <span className="text-xs text-emerald-400 bg-emerald-500/10 px-2 py-1 rounded font-medium">-{m.carbon_estimate || 0}kg CO₂</span>
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
