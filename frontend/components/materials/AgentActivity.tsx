'use client';
import { useEffect, useState } from 'react';
import { AgentActivityStep } from '../../lib/types';

export default function AgentActivity({ steps, animate = true }: { steps: AgentActivityStep[], animate?: boolean }) {
  const [visibleCount, setVisibleCount] = useState(animate ? 0 : steps.length);

  useEffect(() => {
    if (!animate) return;
    if (visibleCount < steps.length) {
      const timer = setTimeout(() => {
        setVisibleCount(v => v + 1);
      }, steps[visibleCount].duration_ms || 400);
      return () => clearTimeout(timer);
    }
  }, [visibleCount, animate, steps]);

  return (
    <div className="glass-card rounded-3xl p-10 max-w-3xl mx-auto shadow-2xl relative overflow-hidden border border-emerald-500/20">
      <div className="absolute top-0 right-0 w-full h-1 bg-gradient-to-r from-transparent via-emerald-500 to-transparent"></div>
      
      <h2 className="text-2xl font-[family-name:var(--font-outfit)] font-bold mb-10 flex items-center gap-4 text-white">
        <div className="w-12 h-12 bg-emerald-500/20 rounded-xl flex items-center justify-center border border-emerald-500/30 text-2xl animate-pulse">🤖</div> 
        Agentic AI Analysis Pipeline
      </h2>
      
      <div className="space-y-8 relative">
        <div className="absolute left-3.5 top-2 bottom-2 w-0.5 bg-slate-800"></div>
        {steps.map((step, i) => {
          const isVisible = i < visibleCount;
          const isCurrent = i === visibleCount - (visibleCount === steps.length ? 1 : 0) && animate && visibleCount < steps.length;
          const isPast = i < visibleCount - 1 || (visibleCount === steps.length && animate);

          return (
            <div key={i} className={`flex items-start gap-6 relative transition-all duration-700 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}>
              <div className={`mt-0.5 flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center relative z-10 transition-colors duration-500 ${isPast ? 'bg-emerald-500 shadow-[0_0_15px_rgba(16,185,129,0.5)]' : isCurrent ? 'bg-slate-900 border-2 border-emerald-500 shadow-[0_0_20px_rgba(16,185,129,0.8)]' : 'bg-slate-800 border border-slate-700'}`}>
                {isPast && <span className="text-white text-sm">✓</span>}
                {isCurrent && <span className="w-3 h-3 bg-emerald-500 rounded-full animate-ping"></span>}
              </div>
              <div className="flex-1 bg-slate-900/50 p-4 rounded-xl border border-white/5">
                <div className="font-bold text-white mb-1 flex items-center gap-2">
                  {step.agent}
                  {isCurrent && <span className="text-xs font-normal text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-full">Processing</span>}
                </div>
                <div className="text-slate-400">{step.message}</div>
              </div>
            </div>
          );
        })}
      </div>
      
      {visibleCount === steps.length && (
        <div className="mt-10 p-4 bg-emerald-500/10 border border-emerald-500/30 rounded-xl text-center animate-fadeIn">
          <div className="text-emerald-400 font-bold text-xl flex items-center justify-center gap-2">
            <span>✨</span> Analysis Complete
          </div>
        </div>
      )}
    </div>
  );
}
