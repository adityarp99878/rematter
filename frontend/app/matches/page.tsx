'use client';
import { useEffect, useState } from 'react';
import Link from 'next/link';
import { getMatches } from '../../lib/api';
import { formatCurrencyFull, getScoreColor } from '../../lib/utils';

export default function MatchesPage() {
  const [matches, setMatches] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getMatches().then(data => {
      if (data && data.matches) {
        setMatches(data.matches);
      } else {
        setMatches([]);
      }
      setLoading(false);
    });
  }, []);

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 animate-fadeIn">
      <div className="flex justify-between items-center mb-10">
        <div>
          <h1 className="text-4xl font-[family-name:var(--font-outfit)] font-bold mb-2 text-white">AI <span className="gradient-text">Matches</span></h1>
          <p className="text-slate-400">Discover optimal connections between recovered materials and active project requirements.</p>
        </div>
        <Link href="/requirements" className="btn-secondary px-6 py-3 font-medium">Post Requirement</Link>
      </div>

      {loading ? (
        <div className="py-20 text-center"><div className="w-12 h-12 border-4 border-emerald-500 border-t-transparent rounded-full animate-spin mx-auto"></div></div>
      ) : matches.length === 0 ? (
        <div className="glass-panel border border-white/5 rounded-3xl p-16 text-center shadow-xl">
          <div className="text-6xl mb-6 opacity-50">🤝</div>
          <h2 className="text-2xl font-[family-name:var(--font-outfit)] font-bold text-white mb-2">No Matches Found</h2>
          <p className="text-slate-400 mb-8 max-w-md mx-auto">There are currently no active matches between inventory and requirements. Check back later or post a new requirement.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {matches.map((match: any) => (
            <Link href={`/matches/${match.id}`} key={match.id} className="glass-card block border border-white/5 rounded-2xl overflow-hidden hover:border-emerald-500/50 hover:-translate-y-1 transition-all duration-300 shadow-xl group">
              <div className="p-6">
                <div className="flex justify-between items-start mb-6 border-b border-white/5 pb-4">
                  <div>
                    <div className="text-xs font-bold text-emerald-500 uppercase tracking-wider mb-1">Match Score</div>
                    <div className="text-4xl font-[family-name:var(--font-outfit)] font-bold text-white" style={{ color: getScoreColor(match.match_score) }}>
                      {match.match_score}<span className="text-xl text-slate-500">/100</span>
                    </div>
                  </div>
                  <div className="bg-slate-900/80 px-3 py-1 rounded-full border border-white/5 text-xs font-bold text-slate-400 uppercase tracking-wider">
                    {match.status}
                  </div>
                </div>

                <div className="space-y-4 mb-6">
                  <div>
                    <div className="text-xs text-slate-500 uppercase tracking-wider font-bold mb-1">Material</div>
                    <div className="text-white font-medium capitalize">{match.material?.material_type.replace('_', ' ')}</div>
                    <div className="text-sm text-slate-400">{match.material?.quantity} {match.material?.unit} • {match.material?.location}</div>
                  </div>
                  
                  <div>
                    <div className="text-xs text-slate-500 uppercase tracking-wider font-bold mb-1">Requirement</div>
                    <div className="text-white font-medium capitalize">{match.requirement?.material_type.replace('_', ' ')}</div>
                    <div className="text-sm text-slate-400">{match.requirement?.quantity_needed} units • {match.requirement?.location}</div>
                  </div>
                </div>

                <div className="bg-slate-900/50 rounded-xl p-4 border border-white/5">
                  <div className="text-xs text-emerald-400 font-bold uppercase tracking-wider mb-2">Impact & Logistics</div>
                  <div className="flex justify-between text-sm text-slate-300 mb-1">
                    <span>Carbon Savings</span>
                    <span className="font-medium text-white">{match.co2_avoided_kg} kg</span>
                  </div>
                  <div className="flex justify-between text-sm text-slate-300">
                    <span>Transport Est.</span>
                    <span className="font-medium text-white">{formatCurrencyFull(match.transport_cost || 0)}</span>
                  </div>
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
