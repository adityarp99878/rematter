import os
base_dir = r"C:\Users\lenovo\.gemini\antigravity\scratch\material-rebirth-ai\frontend"

files = {
    "app/requirements/page.tsx": """'use client';
import Link from 'next/link';

export default function RequirementsPage() {
  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Material Requirements</h1>
        <Link href="/requirements/new" className="bg-emerald-500 hover:bg-emerald-600 text-white px-4 py-2 rounded-lg font-medium transition-colors">
          + Post Requirement
        </Link>
      </div>
      
      <div className="space-y-4">
        {[1,2,3].map(i => (
          <div key={i} className="bg-slate-800/50 border border-slate-700 rounded-xl p-6 flex justify-between items-center hover:bg-slate-800 transition-colors cursor-pointer">
            <div>
              <div className="flex items-center gap-3 mb-2">
                <span className="bg-slate-700 text-xs px-2 py-1 rounded text-slate-300">REQ-{1000+i}</span>
                <h3 className="font-bold text-lg">Reclaimed Bricks for Partition Wall</h3>
              </div>
              <div className="text-sm text-slate-400 flex gap-4">
                <span>Quantity: 450 units</span>
                <span>Budget: ₹15,000</span>
                <span>Location: Ernakulam</span>
              </div>
            </div>
            <div className="text-right">
              <div className="text-emerald-500 font-bold mb-1">3 Matches Found</div>
              <Link href="/matches/demo" className="text-sm text-blue-400 hover:underline">View Matches</Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
""",
    "app/requirements/new/page.tsx": """'use client';
export default function NewRequirementPage() {
  return (
    <div className="max-w-2xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Post New Requirement</h1>
      <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-8">
        <div className="space-y-6">
          <div>
            <label className="block text-sm text-slate-400 mb-2">Material Type</label>
            <select className="w-full bg-slate-900 border border-slate-700 rounded-lg p-3 text-white">
              <option>Brick</option><option>Steel</option><option>Wood</option>
            </select>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm text-slate-400 mb-2">Quantity Needed</label>
              <input type="number" className="w-full bg-slate-900 border border-slate-700 rounded-lg p-3 text-white" />
            </div>
            <div>
              <label className="block text-sm text-slate-400 mb-2">Unit</label>
              <select className="w-full bg-slate-900 border border-slate-700 rounded-lg p-3 text-white">
                <option>Units</option><option>kg</option><option>tonnes</option>
              </select>
            </div>
          </div>
          <div>
            <label className="block text-sm text-slate-400 mb-2">Max Budget (₹)</label>
            <input type="number" className="w-full bg-slate-900 border border-slate-700 rounded-lg p-3 text-white" />
          </div>
          <div>
            <label className="block text-sm text-slate-400 mb-2">Location</label>
            <select className="w-full bg-slate-900 border border-slate-700 rounded-lg p-3 text-white">
              <option>Ernakulam</option><option>Trivandrum</option>
            </select>
          </div>
          <button className="w-full bg-emerald-500 hover:bg-emerald-600 text-white py-3 rounded-lg font-bold transition-colors">
            Post Requirement
          </button>
        </div>
      </div>
    </div>
  );
}
""",
    "app/impact/page.tsx": """'use client';
export default function ImpactPage() {
  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Sustainability Impact Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        {[
          {l: 'Total Materials Reused', v: '12,450 units', c: 'text-white'},
          {l: 'Waste Diverted', v: '18.4 tonnes', c: 'text-amber-400'},
          {l: 'CO₂ Avoided', v: '4.2 tonnes', c: 'text-emerald-400'},
          {l: 'Value Recovered', v: '₹4.2L', c: 'text-blue-400'}
        ].map((s,i) => (
          <div key={i} className="bg-slate-800/50 border border-slate-700 rounded-xl p-6">
            <div className="text-slate-400 text-sm mb-2">{s.l}</div>
            <div className={`text-3xl font-bold ${s.c}`}>{s.v}</div>
          </div>
        ))}
      </div>
      <div className="h-96 bg-slate-800/50 border border-slate-700 rounded-xl flex items-center justify-center text-slate-500">
        Chart Placeholder (Use Recharts here for actual impl)
      </div>
    </div>
  );
}
""",
    "app/notifications/page.tsx": """'use client';
export default function NotificationsPage() {
  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Notifications</h1>
      <div className="space-y-4">
        {[
          {title: 'New Match Found', desc: 'AI found a 94% match for your Reclaimed Bricks', time: '10 mins ago', unread: true},
          {title: 'Passport Generated', desc: 'Material Passport for MR-1001-BRK is ready', time: '2 hours ago', unread: false},
        ].map((n, i) => (
          <div key={i} className={`p-4 rounded-xl border ${n.unread ? 'bg-slate-800 border-slate-600' : 'bg-slate-900 border-slate-800'}`}>
            <h3 className={`font-bold ${n.unread ? 'text-white' : 'text-slate-300'}`}>{n.title}</h3>
            <p className="text-sm text-slate-400 mt-1">{n.desc}</p>
            <div className="text-xs text-slate-500 mt-2">{n.time}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
""",
    "lib/api.ts": """export const API_URL = 'http://localhost:8000';
// Add fetch wrappers here
""",
    "lib/types.ts": """export interface Material {
  id: string;
  name: string;
  type: string;
  quantity: number;
}
""",
    "lib/utils.ts": """import { clsx, type ClassValue } from 'clsx';
export function cn(...inputs: ClassValue[]) {
  return clsx(inputs);
}
""",
    "lib/demo-data.ts": """export const demoMaterials = [];
""",
    "lib/constants.ts": """export const CATEGORIES = ['Brick', 'Steel', 'Wood'];
""",
    "hooks/useApi.ts": """import { useState } from 'react';
export function useApi() {
  const [loading, setLoading] = useState(false);
  return { loading };
}
"""
}

for rel_path, content in files.items():
    full_path = os.path.join(base_dir, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print("Generated remaining pages and libs.")
