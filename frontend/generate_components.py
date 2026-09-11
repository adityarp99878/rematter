import os
base_dir = r"C:\Users\lenovo\.gemini\antigravity\scratch\material-rebirth-ai\frontend"

files = {
    "components/layout/Navbar.tsx": """'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function Navbar() {
  const pathname = usePathname();
  const isActive = (path: string) => pathname?.startsWith(path);
  
  return (
    <nav className="fixed top-0 w-full z-50 glass border-b border-slate-800">
      <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2">
          <div className="text-emerald-500 text-2xl">♻️</div>
          <span className="font-bold text-xl tracking-tight">Material Rebirth AI</span>
        </Link>
        <div className="hidden md:flex gap-6">
          <Link href="/dashboard" className={`hover:text-emerald-400 transition-colors ${isActive('/dashboard') ? 'text-emerald-500' : 'text-slate-300'}`}>Dashboard</Link>
          <Link href="/marketplace" className={`hover:text-emerald-400 transition-colors ${isActive('/marketplace') ? 'text-emerald-500' : 'text-slate-300'}`}>Marketplace</Link>
          <Link href="/impact" className={`hover:text-emerald-400 transition-colors ${isActive('/impact') ? 'text-emerald-500' : 'text-slate-300'}`}>Impact</Link>
        </div>
        <div className="flex items-center gap-4">
          <Link href="/notifications" className="relative p-2 text-slate-300 hover:text-white transition-colors">
            🔔
            <span className="absolute top-1 right-1 w-2 h-2 bg-emerald-500 rounded-full animate-pulse-glow"></span>
          </Link>
          <div className="w-8 h-8 rounded-full bg-slate-700 border border-slate-600 flex items-center justify-center text-sm font-semibold">
            AR
          </div>
        </div>
      </div>
    </nav>
  );
}
""",
    "components/layout/Footer.tsx": """export default function Footer() {
  return (
    <footer className="border-t border-slate-800 py-8 text-center text-slate-500 text-sm mt-auto">
      <p>© {new Date().getFullYear()} Material Rebirth AI. Kerala Hackathon Project.</p>
    </footer>
  );
}
""",
    "app/dashboard/page.tsx": """'use client';
import Link from 'next/link';

export default function DashboardPage() {
  return (
    <div className="max-w-7xl mx-auto px-4 py-8 animate-fadeIn">
      <h1 className="text-3xl font-bold mb-2">Welcome back, Arjun</h1>
      <p className="text-slate-400 mb-8">Here's what's happening with your materials.</p>
      
      <div className="flex gap-4 mb-8">
        <Link href="/scan" className="bg-emerald-500 hover:bg-emerald-600 text-white px-6 py-3 rounded-lg font-medium transition-all">+ List Material</Link>
        <Link href="/marketplace" className="bg-slate-800 hover:bg-slate-700 border border-slate-700 text-white px-6 py-3 rounded-lg font-medium transition-all">Find Materials</Link>
        <Link href="/requirements/new" className="bg-slate-800 hover:bg-slate-700 border border-slate-700 text-white px-6 py-3 rounded-lg font-medium transition-all">Post Requirement</Link>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        {[{l: 'Materials Listed', v: '12'}, {l: 'Active Requirements', v: '3'}, {l: 'Successful Matches', v: '8'}, {l: 'Materials Reused', v: '450 units'}, {l: 'CO₂ Avoided (t)', v: '2.4'}, {l: 'Value Recovered (₹)', v: '85,000'}].map(s => (
          <div key={s.l} className="bg-slate-800/50 border border-slate-700 rounded-xl p-6">
            <div className="text-slate-400 text-sm mb-2">{s.l}</div>
            <div className="text-3xl font-bold text-white">{s.v}</div>
          </div>
        ))}
      </div>
      
      <div className="bg-emerald-500/10 border border-emerald-500/30 rounded-xl p-6 mb-12 flex items-center gap-4">
        <div className="text-2xl">🤖</div>
        <div>
          <h3 className="font-semibold text-emerald-400">AI Recommendation</h3>
          <p className="text-slate-300">3 projects currently need your reclaimed bricks in Kochi.</p>
        </div>
        <Link href="/matches" className="ml-auto bg-emerald-500/20 text-emerald-400 px-4 py-2 rounded-lg hover:bg-emerald-500/30 transition-colors text-sm font-medium">View Matches</Link>
      </div>
    </div>
  );
}
""",
    "app/scan/page.tsx": """'use client';
import { useState } from 'react';
import Link from 'next/link';
import AgentActivity from '../../components/materials/AgentActivity';
import AssessmentResult from '../../components/materials/AssessmentResult';

export default function ScanPage() {
  const [step, setStep] = useState<'upload' | 'analyzing' | 'result'>('upload');
  
  const handleAnalyze = () => {
    setStep('analyzing');
    setTimeout(() => {
      setStep('result');
    }, 6000); // Wait for agents
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 animate-fadeIn">
      <h1 className="text-3xl font-bold mb-8">Scan & Analyze Material</h1>
      
      {step === 'upload' && (
        <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-8">
          <div className="border-2 border-dashed border-slate-600 rounded-xl p-12 text-center mb-6 hover:border-emerald-500 transition-colors cursor-pointer">
            <div className="text-4xl mb-4">📸</div>
            <h3 className="text-xl font-semibold mb-2">Upload Material Photos</h3>
            <p className="text-slate-400 mb-6">Drag and drop, or click to browse. Min 2 images.</p>
            <button className="bg-slate-700 hover:bg-slate-600 text-white px-6 py-2 rounded-lg transition-colors">Select Files</button>
          </div>
          
          <div className="grid grid-cols-2 gap-4 mb-8">
            <div>
              <label className="block text-sm text-slate-400 mb-2">Material Category</label>
              <select className="w-full bg-slate-900 border border-slate-700 rounded-lg p-3 text-white">
                <option>Select...</option>
                <option>Brick</option>
                <option>Steel</option>
                <option>Wood</option>
              </select>
            </div>
            <div>
              <label className="block text-sm text-slate-400 mb-2">Quantity</label>
              <input type="number" className="w-full bg-slate-900 border border-slate-700 rounded-lg p-3 text-white" placeholder="e.g. 500" />
            </div>
            <div className="col-span-2">
              <label className="block text-sm text-slate-400 mb-2">Location</label>
              <select className="w-full bg-slate-900 border border-slate-700 rounded-lg p-3 text-white">
                <option>Kochi</option>
                <option>Trivandrum</option>
                <option>Calicut</option>
              </select>
            </div>
          </div>
          
          <button onClick={handleAnalyze} className="w-full bg-emerald-500 hover:bg-emerald-600 text-white px-6 py-4 rounded-lg font-bold text-lg transition-all shadow-lg">
            Analyze Material with AI
          </button>
        </div>
      )}

      {step === 'analyzing' && <AgentActivity />}
      
      {step === 'result' && (
        <div className="animate-slideUp">
          <AssessmentResult />
          <div className="flex gap-4 mt-8">
            <Link href="/materials/demo-id/passport" className="flex-1 text-center bg-emerald-500 hover:bg-emerald-600 text-white px-6 py-3 rounded-lg font-medium transition-all">Generate Passport</Link>
            <button className="flex-1 bg-slate-800 hover:bg-slate-700 border border-slate-700 text-white px-6 py-3 rounded-lg font-medium transition-all">List on Marketplace</button>
          </div>
        </div>
      )}
    </div>
  );
}
""",
    "components/materials/AgentActivity.tsx": """'use client';
import { useState, useEffect } from 'react';

const steps = [
  { id: 1, agent: 'Upload Agent', msg: 'Received material photos' },
  { id: 2, agent: 'Vision Agent', msg: 'Analyzing images with computer vision' },
  { id: 3, agent: 'Vision Agent', msg: 'Detected material type and condition' },
  { id: 4, agent: 'Assessment Agent', msg: 'Calculating reuse score' },
  { id: 5, agent: 'Passport Agent', msg: 'Generating material passport' },
  { id: 6, agent: 'Orchestrator', msg: 'Finalizing assessment' }
];

export default function AgentActivity() {
  const [activeStep, setActiveStep] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setActiveStep(prev => {
        if (prev >= steps.length) {
          clearInterval(timer);
          return prev;
        }
        return prev + 1;
      });
    }, 800);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-8 animate-fadeIn">
      <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
        <span className="text-2xl animate-pulse">🤖</span> AI Agents Analyzing...
      </h3>
      <div className="space-y-4 relative before:absolute before:inset-0 before:ml-4 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-slate-700 before:to-transparent">
        {steps.map((step, index) => {
          const status = index < activeStep ? 'complete' : index === activeStep ? 'running' : 'waiting';
          return (
            <div key={step.id} className={`relative flex items-center gap-4 transition-all duration-500 ${status === 'waiting' ? 'opacity-30' : 'opacity-100'}`}>
              <div className={`w-8 h-8 rounded-full border-2 flex items-center justify-center shrink-0 z-10 
                ${status === 'complete' ? 'bg-emerald-500 border-emerald-500 text-white' : 
                  status === 'running' ? 'bg-slate-800 border-emerald-500 text-emerald-500 animate-pulse-glow' : 
                  'bg-slate-800 border-slate-600 text-slate-500'}`}>
                {status === 'complete' ? '✓' : index + 1}
              </div>
              <div className="bg-slate-900 border border-slate-700 rounded-lg p-3 w-full">
                <div className="text-xs font-semibold text-emerald-500 mb-1">{step.agent}</div>
                <div className="text-sm text-slate-300">{step.msg}</div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
""",
    "components/materials/AssessmentResult.tsx": """export default function AssessmentResult() {
  return (
    <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-8">
      <div className="flex items-start justify-between border-b border-slate-700 pb-6 mb-6">
        <div>
          <h2 className="text-2xl font-bold text-white mb-2">Reclaimed Red Bricks</h2>
          <p className="text-slate-400">Estimated Quantity: 500 units</p>
        </div>
        <div className="bg-emerald-500/20 text-emerald-400 px-4 py-2 rounded-full font-bold">
          Excellent Condition
        </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="flex flex-col items-center justify-center p-6 bg-slate-900 rounded-xl border border-slate-700">
          <div className="relative w-32 h-32 flex items-center justify-center rounded-full border-8 border-emerald-500 mb-4 text-4xl font-bold text-white shadow-[0_0_15px_rgba(16,185,129,0.3)]">
            92<span className="text-lg text-slate-400 ml-1">/100</span>
          </div>
          <div className="text-slate-300 font-semibold mb-1">Reuse Score</div>
          <div className="text-xs text-emerald-500">High Suitability</div>
        </div>
        
        <div className="space-y-4">
          <div className="bg-slate-900 rounded-lg p-4 border border-slate-700">
            <h4 className="font-semibold text-white mb-2 text-sm">AI Confidence</h4>
            <div className="w-full bg-slate-800 rounded-full h-2">
              <div className="bg-blue-500 h-2 rounded-full w-[95%]"></div>
            </div>
            <div className="text-right text-xs text-slate-400 mt-1">95%</div>
          </div>
          <div className="bg-slate-900 rounded-lg p-4 border border-slate-700">
            <h4 className="font-semibold text-white mb-2 text-sm">Visible Defects</h4>
            <ul className="text-sm text-slate-400 list-disc list-inside">
              <li>Minor mortar residue (15%)</li>
              <li>Chipped corners (< 5%)</li>
            </ul>
          </div>
          <div className="bg-emerald-500/10 border border-emerald-500/30 rounded-lg p-4">
            <h4 className="font-semibold text-emerald-400 mb-1 text-sm">Recommendation</h4>
            <p className="text-sm text-emerald-300">Safe for direct reuse in non-load bearing walls or landscaping.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
"""
}

for rel_path, content in files.items():
    full_path = os.path.join(base_dir, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print("Generated dashboard and scan components.")
