'use client';
import { useState, useRef } from 'react';
import Link from 'next/link';
import AgentActivity from '../../components/materials/AgentActivity';
import AssessmentResult from '../../components/materials/AssessmentResult';
import { analyzeMaterial } from '../../lib/api';
import { MATERIAL_CATEGORIES, KERALA_CITIES } from '../../lib/constants';
import { AssessmentResult as AssessmentType, AgentActivityStep } from '../../lib/types';

export default function ScanPage() {
  const [step, setStep] = useState<'upload' | 'analyzing' | 'result'>('upload');
  const [files, setFiles] = useState<File[]>([]);
  const [formData, setFormData] = useState({
    material_type: '',
    location: '',
    quantity: '',
    unit: 'units',
    age: ''
  });
  const [analysisResult, setAnalysisResult] = useState<any>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  
  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFiles(Array.from(e.target.files));
    }
  };

  const handleAnalyze = async () => {
    if (files.length === 0) {
      alert("Please select at least one photo.");
      return;
    }
    
    setStep('analyzing');
    
    const data = new FormData();
    files.forEach(file => data.append('files', file));
    if (formData.material_type) data.append('material_type', formData.material_type);
    if (formData.location) data.append('location', formData.location);
    if (formData.quantity) data.append('quantity', formData.quantity);
    if (formData.unit) data.append('unit', formData.unit);
    if (formData.age) data.append('age', formData.age);
    
    const result = await analyzeMaterial(data);
    
    if (result) {
      setAnalysisResult(result);
      // Wait for agent activity animation before showing result
      const duration = result.agent_activity.reduce((acc: number, step: AgentActivityStep) => acc + (step.duration_ms || 400), 0) + 1000;
      setTimeout(() => {
        setStep('result');
      }, duration);
    } else {
      alert("Analysis failed. Please check the backend connection or API key.");
      setStep('upload');
    }
  };

  return (
    <div className="max-w-5xl mx-auto px-4 py-12 animate-fadeIn">
      <div className="text-center mb-12">
        <h1 className="text-4xl md:text-5xl font-[family-name:var(--font-outfit)] font-bold mb-4 text-white">Scan & Analyze <span className="gradient-text">Material</span></h1>
        <p className="text-lg text-slate-400 max-w-2xl mx-auto">Upload photos of recovered materials for instant AI assessment, structural grading, and market pricing.</p>
      </div>
      
      {step === 'upload' && (
        <div className="glass-panel border border-white/10 rounded-3xl p-10 shadow-2xl relative overflow-hidden">
          <div className="absolute top-0 right-0 w-64 h-64 bg-emerald-500/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2"></div>
          
          <input 
            type="file" 
            multiple 
            accept="image/*" 
            ref={fileInputRef} 
            onChange={handleFileSelect} 
            className="hidden" 
          />
          
          <div onClick={() => fileInputRef.current?.click()} className="relative border-2 border-dashed border-emerald-500/30 rounded-2xl p-16 text-center mb-10 hover:border-emerald-500 hover:bg-emerald-500/5 transition-all duration-300 cursor-pointer group bg-slate-900/50">
            <div className="w-24 h-24 bg-slate-800 rounded-full flex items-center justify-center text-5xl mx-auto mb-6 shadow-inner group-hover:scale-110 group-hover:shadow-[0_0_20px_rgba(16,185,129,0.3)] transition-all">📸</div>
            <h3 className="text-2xl font-[family-name:var(--font-outfit)] font-bold mb-3 text-white">
              {files.length > 0 ? `${files.length} Photo(s) Selected` : 'Drop Photos Here or Click to Browse'}
            </h3>
            {files.length > 0 ? (
              <div className="text-emerald-400 font-medium">{files.map(f => f.name).join(', ')}</div>
            ) : (
              <p className="text-slate-400 mb-8 max-w-md mx-auto">Upload at least 2 clear photos. For structural elements, include close-ups of connections and any visible damage.</p>
            )}
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-10 relative">
            <div>
              <label className="block text-sm font-bold text-slate-300 mb-2 uppercase tracking-wide">Material Category</label>
              <select 
                value={formData.material_type}
                onChange={e => setFormData({...formData, material_type: e.target.value})}
                className="w-full bg-slate-900/80 border border-white/10 rounded-xl p-4 text-white focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 transition-colors shadow-inner appearance-none">
                <option value="">✨ Auto-detect with AI...</option>
                {MATERIAL_CATEGORIES.map(c => <option key={c.value} value={c.value}>{c.icon} {c.label}</option>)}
              </select>
            </div>
            <div>
              <label className="block text-sm font-bold text-slate-300 mb-2 uppercase tracking-wide">Location</label>
              <select 
                value={formData.location}
                onChange={e => setFormData({...formData, location: e.target.value})}
                className="w-full bg-slate-900/80 border border-white/10 rounded-xl p-4 text-white focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 transition-colors shadow-inner appearance-none">
                <option value="">Select location...</option>
                {KERALA_CITIES.map(c => <option key={c} value={c}>{c}, Kerala</option>)}
              </select>
            </div>
            <div>
              <label className="block text-sm font-bold text-slate-300 mb-2 uppercase tracking-wide">Quantity (Optional)</label>
              <div className="flex shadow-inner rounded-xl overflow-hidden border border-white/10 focus-within:border-emerald-500 focus-within:ring-1 focus-within:ring-emerald-500 transition-colors">
                <input 
                  type="number" 
                  value={formData.quantity}
                  onChange={e => setFormData({...formData, quantity: e.target.value})}
                  className="w-2/3 bg-slate-900/80 p-4 text-white outline-none" 
                  placeholder="e.g. 500" 
                />
                <select 
                  value={formData.unit}
                  onChange={e => setFormData({...formData, unit: e.target.value})}
                  className="w-1/3 bg-slate-800 border-l border-white/10 p-4 text-white outline-none">
                  <option>units</option>
                  <option>sqft</option>
                  <option>kg</option>
                </select>
              </div>
            </div>
            <div>
              <label className="block text-sm font-bold text-slate-300 mb-2 uppercase tracking-wide">Age (Optional)</label>
              <input 
                type="text" 
                value={formData.age}
                onChange={e => setFormData({...formData, age: e.target.value})}
                className="w-full bg-slate-900/80 border border-white/10 rounded-xl p-4 text-white focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none transition-colors shadow-inner" 
                placeholder="e.g. 15 years" 
              />
            </div>
          </div>
          
          <button onClick={handleAnalyze} className="w-full btn-primary py-5 text-xl tracking-wide shadow-[0_0_30px_rgba(16,185,129,0.2)]">
            Analyze Material with AI
          </button>
        </div>
      )}

      {step === 'analyzing' && (
        <div className="py-20 animate-fadeIn text-center">
          {!analysisResult ? (
            <div className="flex flex-col items-center justify-center">
              <div className="w-16 h-16 border-4 border-emerald-500 border-t-transparent rounded-full animate-spin mb-6"></div>
              <h2 className="text-2xl font-bold text-white">AI Agents Initializing...</h2>
              <p className="text-slate-400 mt-2">Uploading photos and extracting data</p>
            </div>
          ) : (
            <AgentActivity steps={analysisResult.agent_activity} animate={true} />
          )}
        </div>
      )}
      
      {step === 'result' && analysisResult && (
        <div className="animate-slideUp space-y-8">
          <AssessmentResult assessment={analysisResult.assessment} materialType={analysisResult.material.material_type} />
          
          <div className="flex flex-col sm:flex-row gap-6 max-w-4xl mx-auto pt-4">
            {analysisResult.assessment.recommendation === 'rejected' ? (
              <>
                <Link href={`/materials/${analysisResult.material_id}/passport`} className="flex-1 btn-secondary text-center py-5 text-lg shadow-lg">
                  View Audit Record
                </Link>
                <button onClick={() => { setStep('upload'); setFiles([]); setAnalysisResult(null); }} className="flex-1 btn-primary text-center py-5 text-lg">
                  Scan Another Material
                </button>
              </>
            ) : (
              <>
                <Link href={`/materials/${analysisResult.material_id}/passport`} className="flex-1 btn-secondary text-center py-5 text-lg shadow-lg">
                  View Material Passport
                </Link>
                <Link href="/dashboard" className="flex-1 btn-primary text-center py-5 text-lg">
                  List on Marketplace
                </Link>
              </>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
