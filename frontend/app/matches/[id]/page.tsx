'use client';
import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import { getMatch } from '../../../lib/api';
import { demoMatch } from '../../../lib/demo-data';
import { MatchData } from '../../../lib/types';
import { formatCurrencyFull, getConditionColor, getScoreColor } from '../../../lib/utils';

export default function MatchDetailPage() {
  const routerParams = useParams();
  const idStr = Array.isArray(routerParams?.id) ? routerParams.id[0] : (routerParams?.id as string);
  const [match, setMatch] = useState<MatchData | null>(null);

  useEffect(() => {
    if (!idStr) return;
    getMatch(parseInt(idStr)).then(data => {
      setMatch(data || null);
    });
  }, [idStr]);

  if (!match) return <div className="p-12 text-center">Loading match details...</div>;

  const mat = match.material;
  const req = match.requirement;
  const p = match.pricing;
  const l = match.logistics;
  const i = match.impact;

  return (
    <div className="max-w-6xl mx-auto px-4 py-8 animate-fadeIn">
      <Link href="/dashboard" className="text-emerald-500 hover:text-emerald-400 mb-6 inline-block">&larr; Back to Dashboard</Link>
      
      <div className="flex flex-col md:flex-row justify-between items-start gap-8 mb-12">
        <div>
          <h1 className="text-4xl font-bold mb-2">Match Recommended</h1>
          <p className="text-slate-400 text-lg">AI has found a highly compatible project for this material.</p>
        </div>
        <div className="bg-slate-900 border border-slate-700 rounded-2xl p-6 flex items-center gap-6 glass shadow-xl">
          <div className="text-center">
            <div className="text-5xl font-bold text-emerald-500">{match.match_score}</div>
            <div className="text-sm font-bold text-slate-400 mt-1 uppercase tracking-wider">Overall Match</div>
          </div>
          <div className="w-px h-16 bg-slate-700"></div>
          <div className="space-y-2 text-sm w-48">
            <div className="flex justify-between"><span>Quantity</span> <span className="font-bold text-emerald-400">{match.quantity_score}%</span></div>
            <div className="flex justify-between"><span>Quality</span> <span className="font-bold text-emerald-400">{match.quality_score}%</span></div>
            <div className="flex justify-between"><span>Distance</span> <span className="font-bold text-emerald-400">{match.distance_score}%</span></div>
            <div className="flex justify-between"><span>Price</span> <span className="font-bold text-emerald-400">{match.price_score}%</span></div>
            <div className="flex justify-between"><span>Carbon</span> <span className="font-bold text-emerald-400">{match.carbon_score}%</span></div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
        {/* Material Summary */}
        <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-6">
          <div className="text-xs font-bold text-emerald-500 uppercase tracking-wider mb-4">The Material</div>
          <h2 className="text-2xl font-bold capitalize mb-2">{mat?.material_type.replace('_', ' ')}</h2>
          <div className="text-slate-400 mb-4">{mat?.quantity} {mat?.unit} available in {mat?.location}</div>
          <div className="flex gap-4 mb-4">
            <div className="bg-slate-900 rounded p-3 flex-1 text-center border border-slate-700">
              <div className="text-xs text-slate-500 mb-1">Condition</div>
              <div className="font-bold capitalize" style={{ color: getConditionColor(mat?.condition || '') }}>{mat?.condition}</div>
            </div>
            <div className="bg-slate-900 rounded p-3 flex-1 text-center border border-slate-700">
              <div className="text-xs text-slate-500 mb-1">Reuse Score</div>
              <div className="font-bold text-emerald-400">{mat?.reuse_score}/100</div>
            </div>
          </div>
          <div className="text-sm text-slate-300 bg-slate-900/50 p-4 rounded border border-slate-800 italic">
            "{mat?.description}"
          </div>
        </div>

        {/* Requirement Summary */}
        <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-6">
          <div className="text-xs font-bold text-blue-400 uppercase tracking-wider mb-4">The Requirement</div>
          <h2 className="text-2xl font-bold mb-2">{req?.purpose}</h2>
          <div className="text-slate-400 mb-4">Needs {req?.quantity_needed} {req?.unit} of {req?.material_type.replace('_', ' ')} in {req?.location}</div>
          <div className="bg-slate-900/50 rounded-lg p-4 border border-slate-700 mb-4">
            <div className="flex justify-between items-center mb-2">
              <span className="text-slate-400">Buyer</span>
              <span className="font-semibold text-white">{match.buyer?.company}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-slate-400">Max Budget</span>
              <span className="font-semibold text-white">{formatCurrencyFull(req?.max_budget || 0)}</span>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-slate-900 border border-slate-700 rounded-xl p-8 mb-12 glass">
        <h3 className="text-xl font-bold mb-4 flex items-center gap-2"><span className="text-emerald-500">🤖</span> AI Match Reasoning</h3>
        <p className="text-lg text-slate-300 leading-relaxed">{match.ai_reasoning}</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
        {/* Pricing */}
        {p && (
          <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-6 col-span-1">
            <h3 className="text-lg font-bold mb-6 flex items-center gap-2"><span>💰</span> Pricing</h3>
            <div className="space-y-4">
              <div className="flex justify-between text-slate-400 line-through">
                <span>New equivalent:</span>
                <span>{formatCurrencyFull(p.new_material_total)}</span>
              </div>
              <div className="flex justify-between text-xl font-bold text-white">
                <span>Recommended:</span>
                <span className="text-emerald-400">{formatCurrencyFull(p.recommended_price)}</span>
              </div>
              <div className="bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 rounded p-3 text-center font-bold">
                Buyer saves {p.buyer_savings_percent}% ({formatCurrencyFull(p.buyer_savings)})
              </div>
              <ul className="text-sm text-slate-400 space-y-2 mt-4 pl-4 list-disc">
                {p.reasoning.slice(0, 3).map((r, i) => <li key={i}>{r}</li>)}
              </ul>
            </div>
          </div>
        )}

        {/* Impact */}
        {i && (
          <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-6 col-span-1">
            <h3 className="text-lg font-bold mb-6 flex items-center gap-2"><span>🌱</span> Environmental Impact</h3>
            <div className="grid grid-cols-2 gap-4 mb-4">
              <div className="bg-slate-900 p-4 rounded text-center border border-slate-700">
                <div className="text-2xl font-bold text-emerald-400">{i.waste_diverted_tonnes}t</div>
                <div className="text-xs text-slate-400 mt-1">Waste Diverted</div>
              </div>
              <div className="bg-slate-900 p-4 rounded text-center border border-slate-700">
                <div className="text-2xl font-bold text-emerald-400">{i.co2_avoided_tonnes}t</div>
                <div className="text-xs text-slate-400 mt-1">CO₂ Avoided</div>
              </div>
            </div>
            <div className="bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 rounded p-3 text-center text-sm font-medium">
              🌳 Equivalent to planting {i.trees_equivalent} trees
            </div>
          </div>
        )}

        {/* Logistics */}
        {l && (
          <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-6 col-span-1">
            <h3 className="text-lg font-bold mb-6 flex items-center gap-2"><span>🚚</span> Logistics</h3>
            <div className="flex justify-between items-center mb-6">
              <div className="text-center">
                <div className="text-xs text-slate-400">From</div>
                <div className="font-bold">{mat?.location}</div>
              </div>
              <div className="text-slate-500 text-xs px-2 border-b border-dashed border-slate-500 flex-1 text-center pb-1">
                {l.direct_distance_km} km
              </div>
              <div className="text-center">
                <div className="text-xs text-slate-400">To</div>
                <div className="font-bold">{req?.location}</div>
              </div>
            </div>
            
            <div className="space-y-3">
              {l.route_options.map((opt, idx) => (
                <div key={idx} className={`p-3 rounded border text-sm ${opt.recommended ? 'bg-emerald-500/10 border-emerald-500/50' : 'bg-slate-900 border-slate-700'}`}>
                  <div className="flex justify-between font-bold mb-1">
                    <span>{opt.route_name} {opt.recommended && <span className="text-emerald-500 text-xs ml-1">★ Rec</span>}</span>
                    <span>{formatCurrencyFull(opt.estimated_cost)}</span>
                  </div>
                  <div className="flex justify-between text-xs text-slate-400">
                    <span>{opt.vehicle_type}</span>
                    <span>{opt.co2_emissions_kg}kg CO₂</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
      
      <div className="text-center">
        <button className="bg-emerald-500 hover:bg-emerald-600 text-white px-12 py-5 rounded-xl font-bold text-xl transition-all shadow-[0_0_20px_rgba(16,185,129,0.4)] hover:shadow-[0_0_30px_rgba(16,185,129,0.6)]">
          Accept Match & Initiate Transaction
        </button>
      </div>
    </div>
  );
}
