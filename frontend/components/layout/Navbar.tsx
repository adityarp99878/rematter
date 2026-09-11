'use client';
import Link from 'next/link';

export default function Navbar() {
  return (
    <nav className="fixed top-0 w-full z-50 glass-panel border-b border-white/10 transition-all duration-300">
      <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
        
        <div className="flex items-center gap-12">
          <Link href="/" className="flex items-center gap-3 group">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-400 to-teal-600 flex items-center justify-center shadow-[0_0_15px_rgba(16,185,129,0.5)] group-hover:scale-105 transition-transform duration-300">
              <span className="text-xl">♻️</span>
            </div>
            <span className="font-[family-name:var(--font-outfit)] font-bold text-2xl tracking-tight text-white">
              Material<span className="text-emerald-400">Rebirth</span>
            </span>
          </Link>
          
          <div className="hidden md:flex items-center gap-8 font-medium">
            <Link href="/dashboard" className="text-sm text-slate-300 hover:text-white hover:text-shadow-glow transition-all">Dashboard</Link>
            <Link href="/marketplace" className="text-sm text-slate-300 hover:text-white hover:text-shadow-glow transition-all">Marketplace</Link>
            <Link href="/impact" className="text-sm text-slate-300 hover:text-white hover:text-shadow-glow transition-all">Impact</Link>
          </div>
        </div>

        <div className="flex items-center gap-6">
          <Link href="/scan" className="btn-primary px-6 py-2.5 text-sm hidden sm:block">
            + Scan Material
          </Link>
          
          <div className="flex items-center gap-4 border-l border-white/10 pl-6">
            <Link href="/notifications" className="relative p-2 text-slate-300 hover:text-white transition-colors hover:scale-110">
              <span className="text-xl">🔔</span>
              <span className="absolute top-1 right-1 w-2.5 h-2.5 bg-red-500 border-2 border-slate-900 rounded-full animate-pulse"></span>
            </Link>
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-slate-700 to-slate-800 border border-white/10 flex items-center justify-center text-sm font-bold shadow-inner cursor-pointer hover:border-emerald-500/50 transition-colors">
              AM
            </div>
          </div>
        </div>

      </div>
    </nav>
  );
}
