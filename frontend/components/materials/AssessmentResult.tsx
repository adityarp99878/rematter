import { AssessmentResult as AssessmentType } from '../../lib/types';
import { getConditionColor, getScoreColor, getScoreLabel } from '../../lib/utils';

export default function AssessmentResult({ assessment, materialType }: { assessment: AssessmentType, materialType: string }) {
  if (!assessment) return null;
  
  const scoreColor = getScoreColor(assessment.reuse_score);
  
  return (
    <div className="glass-card border border-white/10 rounded-3xl p-10 max-w-4xl mx-auto shadow-2xl relative overflow-hidden">
      {/* Decorative gradient blur based on score */}
      <div className="absolute top-0 right-0 w-96 h-96 rounded-full blur-[100px] opacity-10 pointer-events-none -translate-y-1/2 translate-x-1/2" style={{ backgroundColor: scoreColor }}></div>
      
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-10 pb-10 border-b border-slate-700/50">
        <div>
          <div className="inline-block px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-sm font-bold tracking-wide uppercase mb-4">
            AI Assessment Complete
          </div>
          <h2 className="text-4xl font-[family-name:var(--font-outfit)] font-bold text-white capitalize mb-2">
            {materialType.replace('_', ' ')}
          </h2>
          <p className="text-slate-400 text-lg">Detected with {Math.round(assessment.confidence * 100)}% confidence</p>
        </div>
        
        <div className="mt-8 md:mt-0 bg-slate-900/80 p-6 rounded-2xl border border-white/5 flex items-center gap-6 shadow-inner relative overflow-hidden">
          <div className="absolute top-0 left-0 w-1 h-full" style={{ backgroundColor: scoreColor }}></div>
          <div>
            <div className="text-sm font-bold text-slate-400 uppercase tracking-wider mb-1">Reuse Score</div>
            <div className="text-sm font-bold" style={{ color: scoreColor }}>
              {getScoreLabel(assessment.reuse_score)} Potential
            </div>
          </div>
          <div className="text-6xl font-[family-name:var(--font-outfit)] font-black" style={{ color: scoreColor }}>
            {assessment.reuse_score}<span className="text-2xl text-slate-500">/100</span>
          </div>
        </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-10">
        <div className="space-y-6">
          <div>
            <h3 className="text-xl font-[family-name:var(--font-outfit)] font-bold mb-4 text-white flex items-center gap-2">🔍 Condition Details</h3>
            <div className="bg-slate-900/50 rounded-xl p-5 border border-white/5 shadow-inner">
              <div className="flex justify-between items-center mb-2">
                <div className="text-slate-400 font-medium">Assessed Condition</div>
                <div className="px-3 py-1 rounded-md text-sm font-bold capitalize" style={{ backgroundColor: `${getConditionColor(assessment.condition)}20`, color: getConditionColor(assessment.condition), border: `1px solid ${getConditionColor(assessment.condition)}40` }}>
                  {assessment.condition}
                </div>
              </div>
            </div>
          </div>
          
          <div>
            <h3 className="text-slate-400 font-medium mb-3">Visible Defects</h3>
            <div className="bg-slate-900/50 rounded-xl p-5 border border-white/5 shadow-inner min-h-[100px]">
              {assessment.visible_defects.length > 0 ? (
                <ul className="space-y-2">
                  {assessment.visible_defects.map((d, i) => (
                    <li key={i} className="flex gap-3 text-slate-300">
                      <span className="text-amber-500/70">●</span> {d}
                    </li>
                  ))}
                </ul>
              ) : (
                <div className="flex items-center gap-2 text-emerald-400 h-full">
                  <span>✨</span> No major defects detected.
                </div>
              )}
            </div>
          </div>
        </div>
        
        <div>
          <h3 className="text-xl font-[family-name:var(--font-outfit)] font-bold mb-4 text-white flex items-center gap-2">🧠 AI Reasoning</h3>
          <div className="bg-slate-900/50 rounded-xl p-6 border border-white/5 shadow-inner h-full">
            <ul className="space-y-5">
              {assessment.reasoning.map((r, i) => (
                <li key={i} className="flex gap-4 items-start group">
                  <span className="text-emerald-500 mt-0.5 bg-emerald-500/10 w-6 h-6 rounded flex items-center justify-center shrink-0 group-hover:bg-emerald-500 group-hover:text-slate-900 transition-colors">↳</span>
                  <span className="text-slate-300 leading-relaxed">{r}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
      
      {assessment.verification_required && (
        <div className="bg-amber-500/10 border border-amber-500/30 rounded-xl p-5 flex gap-4 animate-pulse">
          <div className="text-3xl">⚠️</div>
          <div>
            <h4 className="font-bold text-amber-500 text-lg mb-1">Professional Verification Recommended</h4>
            <p className="text-amber-500/80 text-sm leading-relaxed">{assessment.safety_disclaimer || 'This is a structural material and requires human verification before reuse.'}</p>
          </div>
        </div>
      )}
    </div>
  );
}
