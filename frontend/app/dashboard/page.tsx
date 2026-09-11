'use client';
import { useEffect, useState } from 'react';
import Link from 'next/link';
import { getDashboardStats } from '../../lib/api';
import { demoStats } from '../../lib/demo-data';
import { DashboardStats } from '../../lib/types';
import { formatCurrencyFull, getMaterialIcon } from '../../lib/utils';

export default function DashboardPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null);

  useEffect(() => {
    getDashboardStats().then(data => {
      setStats(data || null);
    });
  }, []);

  if (!stats) return <div className="min-h-[80vh] flex items-center justify-center"><div className="w-12 h-12 border-4 border-emerald-500 border-t-transparent rounded-full animate-spin"></div></div>;

  return (
    <div className="max-w-7xl mx-auto px-4 py-12 animate-slideUp">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-end mb-12">
        <div>
          <h1 className="text-4xl font-[family-name:var(--font-outfit)] font-bold mb-2 text-white">Welcome back, <span className="gradient-text">Arjun</span></h1>
          <p className="text-lg text-slate-400">Here's the latest on your circular construction journey.</p>
        </div>
        <div className="flex gap-4 mt-6 md:mt-0">
          <Link href="/scan" className="btn-primary px-6 py-3 shadow-[0_0_20px_rgba(16,185,129,0.2)] flex items-center gap-2">
            <span className="text-xl">+</span> List Material
          </Link>
          <Link href="/marketplace" className="btn-secondary px-6 py-3">Find Materials</Link>
        </div>
      </div>

      <div className="grid grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
        {[
          { l: 'Materials Listed', v: stats.materials_listed, icon: '📦' },
          { l: 'Active Requirements', v: stats.active_requirements, icon: '📋' },
          { l: 'Successful Matches', v: stats.successful_matches, icon: '🤝' },
          { l: 'Materials Reused', v: `${stats.materials_reused} units`, icon: '♻️' },
          { l: 'CO₂ Avoided', v: `${stats.co2_avoided} t`, icon: '🌱' },
          { l: 'Value Recovered', v: formatCurrencyFull(stats.value_recovered), icon: '💰' }
        ].map((s, i) => (
          <div key={s.l} className="glass-card rounded-2xl p-6 relative overflow-hidden group">
            <div className="absolute top-0 right-0 p-6 opacity-20 text-4xl group-hover:scale-110 group-hover:opacity-40 transition-all duration-500">{s.icon}</div>
            <div className="relative z-10">
              <div className="text-slate-400 font-medium uppercase tracking-wider text-xs mb-3">{s.l}</div>
              <div className="text-4xl font-[family-name:var(--font-outfit)] font-bold text-white">{s.v}</div>
            </div>
            <div className="absolute bottom-0 left-0 h-1 bg-gradient-to-r from-emerald-500 to-teal-500 w-0 group-hover:w-full transition-all duration-500"></div>
          </div>
        ))}
      </div>
      
      {stats.ai_recommendations.map((rec, i) => (
        <div key={i} className="bg-gradient-to-r from-emerald-900/40 to-slate-900 border border-emerald-500/30 rounded-2xl p-6 mb-8 flex flex-col sm:flex-row items-center gap-6 shadow-lg shadow-emerald-900/20 animate-slideInRight" style={{ animationDelay: `${i * 150}ms` }}>
          <div className="w-16 h-16 rounded-full bg-emerald-500/20 border border-emerald-500/50 flex items-center justify-center text-3xl shadow-[0_0_15px_rgba(16,185,129,0.3)] shrink-0">
            🤖
          </div>
          <div className="flex-1 text-center sm:text-left">
            <h3 className="text-lg font-bold text-emerald-400 mb-1">AI Recommendation</h3>
            <p className="text-slate-200 text-lg">{rec.message}</p>
          </div>
          <Link href="/matches" className="btn-primary px-8 py-3 whitespace-nowrap">View Action &rarr;</Link>
        </div>
      ))}
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mt-12">
        <div className="glass-panel rounded-2xl p-8">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-[family-name:var(--font-outfit)] font-bold text-white">Recent Materials</h2>
            <Link href="/materials" className="text-sm text-emerald-400 hover:text-emerald-300">View All</Link>
          </div>
          <div className="space-y-4">
            {stats.recent_materials.slice(0, 4).map(m => (
              <Link href={`/materials/${m.id}`} key={m.id} className="flex items-center p-4 bg-slate-800/40 border border-white/5 rounded-xl hover:bg-slate-700/50 hover:border-white/10 transition-all group">
                <div className="w-12 h-12 rounded-lg bg-slate-900 flex items-center justify-center text-2xl mr-4 group-hover:scale-110 transition-transform">
                  {getMaterialIcon(m.material_type)}
                </div>
                <div className="flex-1">
                  <div className="font-bold text-white capitalize">{m.quantity} {m.unit} {m.material_type.replace('_', ' ')}</div>
                  <div className="text-sm text-slate-400">{m.location} • Score: {m.reuse_score}</div>
                </div>
                <div className="text-right">
                  <div className="font-bold text-emerald-400">{formatCurrencyFull(m.estimated_value || 0)}</div>
                  <div className="text-xs text-slate-500 mt-1 uppercase tracking-wide">{m.status}</div>
                </div>
              </Link>
            ))}
          </div>
        </div>
        
        <div className="glass-panel rounded-2xl p-8">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-[family-name:var(--font-outfit)] font-bold text-white">Recent Matches</h2>
            <Link href="/matches" className="text-sm text-emerald-400 hover:text-emerald-300">View All</Link>
          </div>
          <div className="space-y-4">
            {stats.recent_matches.map(m => (
              <Link href={`/matches/${m.id}`} key={m.id} className="flex items-center p-5 bg-gradient-to-r from-slate-800/40 to-emerald-900/10 border border-white/5 rounded-xl hover:border-emerald-500/30 transition-all group relative overflow-hidden">
                <div className="absolute left-0 top-0 bottom-0 w-1 bg-emerald-500"></div>
                <div className="w-14 h-14 rounded-full bg-slate-900 border-2 border-emerald-500/50 flex items-center justify-center mr-5 shadow-[0_0_15px_rgba(16,185,129,0.2)] group-hover:shadow-[0_0_20px_rgba(16,185,129,0.4)] transition-shadow">
                  <span className="font-bold text-emerald-400 text-lg">{m.match_score}</span>
                </div>
                <div className="flex-1">
                  <div className="font-bold text-white text-lg">High-Value Match Found!</div>
                  <div className="text-sm text-slate-400 mt-1">For Requirement #{m.requirement_id}</div>
                </div>
                <div className="btn-secondary px-4 py-2 text-sm group-hover:border-emerald-500/50 group-hover:text-emerald-400">Review</div>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
