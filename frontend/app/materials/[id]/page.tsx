'use client';
import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import { getMaterial } from '../../../lib/api';
import { formatCurrencyFull, getConditionColor, getScoreColor, getScoreLabel } from '../../../lib/utils';
import AssessmentResult from '../../../components/materials/AssessmentResult';

export default function MaterialDetailPage() {
  const routerParams = useParams();
  const idStr = Array.isArray(routerParams?.id) ? routerParams.id[0] : (routerParams?.id as string);
  const [material, setMaterial] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!idStr) return;
    getMaterial(parseInt(idStr)).then(data => {
      setMaterial(data);
      setLoading(false);
    });
  }, [idStr]);

  if (loading) return <div className="p-12 text-center text-white"><div className="w-12 h-12 border-4 border-emerald-500 border-t-transparent rounded-full animate-spin mx-auto"></div></div>;
  if (!material) return <div className="p-12 text-center text-red-400">Material not found</div>;

  return (
    <div className="max-w-6xl mx-auto px-4 py-8 animate-fadeIn">
      <Link href="/marketplace" className="text-emerald-500 hover:text-emerald-400 mb-6 inline-block font-medium tracking-wide uppercase text-sm">&larr; Back to Marketplace</Link>
      
      <div className="flex flex-col md:flex-row gap-12 mb-12">
        <div className="flex-1">
          <div className="bg-slate-900/50 rounded-2xl aspect-video border border-white/5 flex items-center justify-center text-6xl shadow-inner mb-6 relative overflow-hidden">
            {material.images?.length > 0 ? (
              <img src={`http://localhost:8000${material.images[0].image_url}`} alt="Material" className="w-full h-full object-cover" />
            ) : (
              <span>📸</span>
            )}
            <div className="absolute top-4 right-4 bg-slate-900/80 backdrop-blur-md px-3 py-1 rounded-full border border-white/10 text-xs font-bold uppercase tracking-wider text-emerald-400">
              {material.status}
            </div>
          </div>
        </div>
        
        <div className="flex-1">
          <h1 className="text-4xl font-[family-name:var(--font-outfit)] font-bold mb-2 capitalize text-white">{material.material_type.replace('_', ' ')}</h1>
          <p className="text-slate-400 text-lg mb-6">{material.location}</p>
          
          <div className="glass-panel border border-white/10 rounded-2xl p-8 mb-8 shadow-xl">
            <div className="flex justify-between items-end mb-6">
              <div>
                <div className="text-sm font-bold text-slate-400 uppercase tracking-wider mb-1">Estimated Value</div>
                <div className="text-4xl font-bold text-emerald-400">{formatCurrencyFull(material.estimated_value || 0)}</div>
              </div>
              <div className="text-right">
                <div className="text-sm font-bold text-slate-400 uppercase tracking-wider mb-1">Available Quantity</div>
                <div className="text-2xl font-bold text-white">{material.quantity} {material.unit}</div>
              </div>
            </div>
            
            <Link href={`/materials/${material.id}/passport`} className="block w-full btn-secondary text-center py-4 text-lg">
              View Verified Material Passport
            </Link>
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-slate-900/50 border border-white/5 rounded-xl p-5">
              <div className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-1">Condition</div>
              <div className="font-bold text-lg capitalize" style={{ color: getConditionColor(material.condition) }}>{material.condition || 'Unknown'}</div>
            </div>
            <div className="bg-slate-900/50 border border-white/5 rounded-xl p-5">
              <div className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-1">Reuse Score</div>
              <div className="font-bold text-lg" style={{ color: getScoreColor(material.reuse_score) }}>{material.reuse_score}/100 - {getScoreLabel(material.reuse_score)}</div>
            </div>
            {material.carbon_estimate > 0 && (
              <div className="bg-slate-900/50 border border-white/5 rounded-xl p-5 col-span-2 flex items-center justify-between">
                <div className="text-sm font-bold text-slate-400 uppercase tracking-wider">Carbon Savings Potential</div>
                <div className="font-bold text-xl text-emerald-400">-{material.carbon_estimate}kg CO₂</div>
              </div>
            )}
          </div>
        </div>
      </div>
      
      {material.assessment && (
        <div className="mt-12">
          <AssessmentResult assessment={material.assessment} materialType={material.material_type} />
        </div>
      )}
    </div>
  );
}
