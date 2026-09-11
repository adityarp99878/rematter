import Link from 'next/link';

export default function LandingPage() {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative pt-32 pb-24 px-4 overflow-hidden flex flex-col items-center justify-center min-h-[90vh]">
        <div className="max-w-6xl mx-auto text-center relative z-10 animate-slideUp">
          <div className="inline-block mb-6 px-4 py-1.5 rounded-full border border-emerald-500/30 bg-emerald-500/10 text-emerald-400 font-medium text-sm backdrop-blur-md">
            🚀 The Future of Circular Construction
          </div>
          
          <h1 className="text-6xl md:text-8xl font-[family-name:var(--font-outfit)] font-black mb-6 tracking-tight leading-tight">
            Give Materials <br/>
            <span className="gradient-text drop-shadow-[0_0_25px_rgba(16,185,129,0.4)]">Their Next Life</span>
          </h1>
          
          <p className="text-xl md:text-2xl text-slate-300 max-w-3xl mx-auto mb-12 font-light leading-relaxed">
            The intelligent marketplace connecting recovered construction materials with new projects. 
            Automated assessment, precise matching, and verifiable impact.
          </p>
          
          <div className="flex flex-col sm:flex-row justify-center gap-6 mb-20">
            <Link href="/scan" className="btn-primary px-10 py-4 text-lg shadow-[0_0_40px_rgba(16,185,129,0.3)]">
              Scan Materials Now
            </Link>
            <Link href="/marketplace" className="btn-secondary px-10 py-4 text-lg">
              Explore Marketplace
            </Link>
          </div>
          
          {/* Stats Row */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto glass-panel rounded-2xl p-8 border border-white/10 shadow-2xl">
            <div className="relative">
              <div className="absolute right-0 top-0 bottom-0 w-px bg-gradient-to-b from-transparent via-white/10 to-transparent hidden md:block"></div>
              <div className="text-5xl font-[family-name:var(--font-outfit)] font-bold text-white mb-2">12.8<span className="text-emerald-500 text-3xl">T</span></div>
              <div className="text-slate-400 font-medium uppercase tracking-wider text-sm">Materials Recovered</div>
            </div>
            <div className="relative">
              <div className="absolute right-0 top-0 bottom-0 w-px bg-gradient-to-b from-transparent via-white/10 to-transparent hidden md:block"></div>
              <div className="text-5xl font-[family-name:var(--font-outfit)] font-bold text-white mb-2">18.4<span className="text-emerald-500 text-3xl">T</span></div>
              <div className="text-slate-400 font-medium uppercase tracking-wider text-sm">CO₂ Avoided</div>
            </div>
            <div>
              <div className="text-5xl font-[family-name:var(--font-outfit)] font-bold text-white mb-2"><span className="text-emerald-500 text-3xl">₹</span>4.2<span className="text-3xl">L</span></div>
              <div className="text-slate-400 font-medium uppercase tracking-wider text-sm">Value Recovered</div>
            </div>
          </div>
        </div>
      </section>

      {/* Powered by AI */}
      <section className="py-32 px-4 relative">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-20">
            <h2 className="text-4xl md:text-5xl font-[family-name:var(--font-outfit)] font-bold mb-6">Powered by <span className="gradient-text">Agentic AI</span></h2>
            <p className="text-xl text-slate-400 max-w-2xl mx-auto">Our specialized AI agents work autonomously to handle the entire lifecycle of recovered materials.</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              { title: 'Vision Agent', desc: 'Detects material type, quantity, and condition from photos', icon: '👁️' },
              { title: 'Assessment Agent', desc: 'Evaluates structural integrity and calculates reuse scores', icon: '🧠' },
              { title: 'Pricing Agent', desc: 'Dynamically calculates fair market value and buyer savings', icon: '💰' },
              { title: 'Matching Agent', desc: 'Finds the perfect project based on location, quality, and budget', icon: '🎯' },
              { title: 'Logistics Agent', desc: 'Optimizes transport routes for minimal cost and carbon footprint', icon: '🚚' },
              { title: 'Impact Agent', desc: 'Generates verifiable LCAs and circularity metrics', icon: '🌱' }
            ].map((agent, i) => (
              <div key={i} className="glass-card rounded-2xl p-8 hover:-translate-y-2 transition-transform duration-300 group">
                <div className="w-16 h-16 rounded-2xl bg-slate-800/80 border border-white/5 flex items-center justify-center text-3xl mb-6 shadow-inner group-hover:bg-emerald-500/20 group-hover:border-emerald-500/50 transition-colors">
                  {agent.icon}
                </div>
                <h3 className="text-2xl font-[family-name:var(--font-outfit)] font-bold text-white mb-3">{agent.title}</h3>
                <p className="text-slate-400 leading-relaxed">{agent.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
