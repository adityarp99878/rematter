'use client';
import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import { getMaterialPassport } from '../../../../lib/api';
import { formatCurrencyFull, getConditionColor, getScoreColor } from '../../../../lib/utils';

export default function MaterialPassportPage() {
  const routerParams = useParams();
  const idStr = Array.isArray(routerParams?.id) ? routerParams.id[0] : (routerParams?.id as string);
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!idStr) return;
    getMaterialPassport(parseInt(idStr)).then(res => {
      setData(res);
      setLoading(false);
    });
  }, [idStr]);

  if (loading) return <div className="p-12 text-center"><div className="w-12 h-12 border-4 border-emerald-500 border-t-transparent rounded-full animate-spin mx-auto"></div></div>;
  if (!data) return <div className="p-12 text-center text-red-400">Passport not found</div>;

  const mat = data.material;

  return (
    <div className="max-w-4xl mx-auto px-4 py-12 animate-fadeIn">
      <Link href={`/materials/${idStr}`} className="text-emerald-500 hover:text-emerald-400 mb-6 inline-block font-medium tracking-wide uppercase text-sm">&larr; Back to Material</Link>
      
      <div className="glass-card border border-white/10 rounded-3xl overflow-hidden shadow-2xl relative">
        <div className="absolute top-0 right-0 w-64 h-64 bg-emerald-500/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2"></div>
        
        <div className="bg-gradient-to-r from-slate-800/80 to-emerald-900/40 p-10 border-b border-white/10 flex justify-between items-start relative z-10">
          <div>
            <div className="text-emerald-400 font-bold mb-3 tracking-[0.2em] text-sm uppercase flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
              VERIFIED MATERIAL PASSPORT
            </div>
            <h1 className="text-4xl font-[family-name:var(--font-outfit)] font-bold text-white mb-2 capitalize">{mat?.material_type.replace('_', ' ')}</h1>
            <p className="text-slate-400 font-mono tracking-wider">ID: {data.passport_id}</p>
          </div>
          <div className="w-28 h-28 bg-white p-3 rounded-xl flex justify-center items-center shadow-[0_0_20px_rgba(16,185,129,0.3)] rotate-3">
            {/* Fake QR */}
            <div className="w-full h-full bg-[url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMDAgMTAwIj48cGF0aCBkPSJNMTAgMTBoMzB2MzBIMTB6TTIwIDIwaDEwdjEwaC0xMHpNNjAgMTBoMzB2MzBINjB6TTcwIDIwaDEwdjEwaC0xMHpNMTAgNjBoMzB2MzBIMTB6TTIwIDcwaDEwdjEwaC0xMHpNNDAgMTBoMTB2MTBoLTEwek01MCAyMGgxMHYxMGgtMTB6TTQwIDQwaDEwdjEwaC0xMHpNNTAgNTBoMTB2MTBoLTEwek02MCA0MGgxMHYxMGgtMTB6TTcwIDUwaDEwdjEwaC0xMHpNNDAgNjBoMTB2MTBoLTEwek01MCA3MGgxMHYxMGgtMTB6TTYwIDYwaDEwdjEwaC0xMHpNNzAgNzBoMTB2MTBoLTEwek04MCA4MGgxMHYxMGgtMTB6IiBmaWxsPSIjMDAwIi8+PC9zdmc+')] bg-cover opacity-80"></div>
          </div>
        </div>
        
        <div className="p-10 grid grid-cols-1 md:grid-cols-2 gap-12 relative z-10">
          <div className="space-y-8">
            <div>
              <h3 className="text-slate-400 text-sm font-bold uppercase tracking-wider mb-3">Specifications</h3>
              <div className="grid grid-cols-2 gap-4 bg-slate-900/50 rounded-xl p-5 border border-white/5 shadow-inner">
                <div>
                  <div className="text-slate-500 text-xs uppercase mb-1">Quantity</div>
                  <div className="text-white font-bold">{mat?.quantity} {mat?.unit}</div>
                </div>
                <div>
                  <div className="text-slate-500 text-xs uppercase mb-1">Age</div>
                  <div className="text-white font-bold">{mat?.age || 'Unknown'}</div>
                </div>
                <div>
                  <div className="text-slate-500 text-xs uppercase mb-1">Previous Use</div>
                  <div className="text-white font-bold">{data.previous_use || 'Unknown'}</div>
                </div>
                <div>
                  <div className="text-slate-500 text-xs uppercase mb-1">Source Location</div>
                  <div className="text-white font-bold">{mat?.location}</div>
                </div>
              </div>
            </div>
            
            <div>
              <h3 className="text-slate-400 text-sm font-bold uppercase tracking-wider mb-3">AI Assessment</h3>
              <div className="bg-slate-900/50 rounded-xl p-5 border border-white/5 space-y-4 shadow-inner">
                <div className="flex justify-between items-center">
                  <span className="text-slate-400 font-medium">Condition</span>
                  <span className="font-bold capitalize" style={{ color: getConditionColor(data.ai_condition) }}>{data.ai_condition}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-slate-400 font-medium">Reuse Score</span>
                  <span className="font-bold px-3 py-1 rounded-md text-slate-900" style={{ backgroundColor: getScoreColor(data.ai_reuse_score) }}>{data.ai_reuse_score}/100</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-slate-400 font-medium">Grade</span>
                  <span className="text-white font-bold">{data.material_grade}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-slate-400 font-medium">Verification</span>
                  <span className={`font-bold capitalize ${data.verification_status === 'verified' ? 'text-emerald-400' : 'text-amber-400'}`}>
                    {data.verification_status.replace('_', ' ')}
                  </span>
                </div>
              </div>
            </div>
          </div>
          
          <div className="space-y-8">
            <div>
              <h3 className="text-slate-400 text-sm font-bold uppercase tracking-wider mb-3">Impact & Value</h3>
              <div className="bg-slate-900/50 rounded-xl p-5 border border-white/5 space-y-5 shadow-inner">
                <div>
                  <div className="text-slate-500 text-xs uppercase mb-1">Estimated Market Value</div>
                  <div className="text-3xl font-[family-name:var(--font-outfit)] font-bold text-emerald-400">{formatCurrencyFull(mat?.estimated_value || 0)}</div>
                </div>
                <div className="h-px bg-white/5 w-full"></div>
                <div>
                  <div className="text-slate-500 text-xs uppercase mb-1">Carbon Avoided (CO₂e)</div>
                  <div className="text-2xl font-[family-name:var(--font-outfit)] font-bold text-white flex items-center gap-3">
                    <span className="text-3xl">🌱</span> {data.carbon_estimate} kg
                  </div>
                </div>
              </div>
            </div>
            
            <div>
              <h3 className="text-slate-400 text-sm font-bold uppercase tracking-wider mb-3">Lifecycle Tracking</h3>
              <div className="bg-slate-900/50 rounded-xl p-6 border border-white/5 shadow-inner relative">
                <div className="absolute left-8 top-10 bottom-8 w-0.5 bg-slate-700"></div>
                
                <div className="flex items-start gap-4 mb-6 relative">
                  <div className="w-4 h-4 rounded-full bg-emerald-500 shadow-[0_0_10px_rgba(16,185,129,0.5)] z-10 mt-1"></div>
                  <div>
                    <div className="text-white font-bold">Recovered & Assessed</div>
                    <div className="text-sm text-emerald-400">AI Passport Generated</div>
                  </div>
                </div>
                
                <div className={`flex items-start gap-4 mb-6 relative ${data.lifecycle_stage !== 'passport_created' ? 'opacity-100' : 'opacity-50'}`}>
                  <div className={`w-4 h-4 rounded-full z-10 mt-1 ${data.lifecycle_stage !== 'passport_created' ? 'bg-emerald-500 shadow-[0_0_10px_rgba(16,185,129,0.5)]' : 'bg-slate-700'}`}></div>
                  <div>
                    <div className="text-white font-bold">Listed on Marketplace</div>
                    <div className="text-sm text-slate-400">Available for buyers</div>
                  </div>
                </div>
                
                <div className={`flex items-start gap-4 relative ${data.lifecycle_stage === 'reused' ? 'opacity-100' : 'opacity-50'}`}>
                  <div className={`w-4 h-4 rounded-full z-10 mt-1 ${data.lifecycle_stage === 'reused' ? 'bg-emerald-500 shadow-[0_0_10px_rgba(16,185,129,0.5)]' : 'bg-slate-700'}`}></div>
                  <div>
                    <div className="text-white font-bold">Matched & Reused</div>
                    <div className="text-sm text-slate-400">Installed in new project</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div className="p-8 bg-slate-900/80 border-t border-white/10 flex flex-col sm:flex-row gap-4 relative z-10">
          <Link href="/dashboard" className="flex-1 btn-primary text-center py-4 text-lg">List on Marketplace</Link>
          <Link href="/matches" className="flex-1 btn-secondary text-center py-4 text-lg">Find Buyers</Link>
        </div>
      </div>
    </div>
  );
}
