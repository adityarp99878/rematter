import os

base_dir = r"C:\Users\lenovo\.gemini\antigravity\scratch\material-rebirth-ai\frontend"

files = {
    "app/globals.css": """@tailwind base;
@tailwind components;
@tailwind utilities;

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
  --background: #0a0f1a;
  --surface: #111827;
  --surface-hover: #1a2332;
  --border: #1e293b;
  --primary: #10b981;
  --primary-hover: #059669;
  --primary-light: #d1fae5;
  --accent: #f59e0b;
  --text-primary: #f1f5f9;
  --text-secondary: #94a3b8;
  --text-muted: #64748b;
  --success: #10b981;
  --warning: #f59e0b;
  --danger: #ef4444;
  --info: #3b82f6;
}

body {
  background-color: var(--background);
  color: var(--text-primary);
  font-family: 'Inter', sans-serif;
}

/* Animations */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes slideIn {
  from { opacity: 0; transform: translateX(-20px); }
  to { opacity: 1; transform: translateX(0); }
}

@keyframes pulse-glow {
  0%, 100% { box-shadow: 0 0 15px rgba(16, 185, 129, 0.2); }
  50% { box-shadow: 0 0 25px rgba(16, 185, 129, 0.5); }
}

.animate-fadeIn { animation: fadeIn 0.5s ease-out forwards; }
.animate-slideUp { animation: slideUp 0.5s ease-out forwards; }
.animate-slideIn { animation: slideIn 0.5s ease-out forwards; }
.animate-pulse-glow { animation: pulse-glow 2s infinite; }

/* Scrollbar */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}
::-webkit-scrollbar-track {
  background: var(--background);
}
::-webkit-scrollbar-thumb {
  background: var(--border);
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
  background: var(--surface-hover);
}

.glass {
  background: rgba(17, 24, 39, 0.7);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid var(--border);
}

.gradient-text {
  background: linear-gradient(to right, #10b981, #0d9488);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
""",
    "app/layout.tsx": """import type { Metadata } from 'next';
import './globals.css';
import Navbar from '../components/layout/Navbar';
import Footer from '../components/layout/Footer';

export const metadata: Metadata = {
  title: 'Material Rebirth AI',
  description: 'Agentic AI marketplace for construction material circularity.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen flex flex-col bg-[#0a0f1a] text-slate-100 font-sans">
        <Navbar />
        <main className="flex-grow pt-16">
          {children}
        </main>
        <Footer />
      </body>
    </html>
  );
}
""",
    "app/page.tsx": """import Link from 'next/link';

export default function LandingPage() {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative pt-32 pb-20 px-4 overflow-hidden">
        <div className="absolute inset-0 bg-[url('/grid-pattern.svg')] bg-center opacity-10"></div>
        <div className="max-w-6xl mx-auto text-center relative z-10 animate-slideUp">
          <h1 className="text-5xl md:text-7xl font-bold mb-6 tracking-tight">
            Give Construction Materials <br/>
            <span className="gradient-text">Their Next Life</span>
          </h1>
          <p className="text-xl text-slate-400 max-w-3xl mx-auto mb-10">
            The agentic AI marketplace that connects recovered materials with new projects. 
            Automated assessment, precise matching, and verified sustainability impact.
          </p>
          <div className="flex flex-col sm:flex-row justify-center gap-4 mb-16">
            <Link href="/scan" className="bg-emerald-500 hover:bg-emerald-600 text-white px-8 py-4 rounded-lg font-semibold text-lg transition-all shadow-[0_0_20px_rgba(16,185,129,0.3)] hover:shadow-[0_0_30px_rgba(16,185,129,0.5)]">
              Scan Materials
            </Link>
            <Link href="/marketplace" className="bg-slate-800 hover:bg-slate-700 border border-slate-700 text-white px-8 py-4 rounded-lg font-semibold text-lg transition-all">
              Explore Marketplace
            </Link>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto border-t border-slate-800 pt-10">
            <div>
              <div className="text-4xl font-bold text-white mb-2">12.8T</div>
              <div className="text-slate-400">Materials Recovered</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-white mb-2">18.4T</div>
              <div className="text-slate-400">CO₂ Avoided</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-white mb-2">₹4.2L</div>
              <div className="text-slate-400">Value Recovered</div>
            </div>
          </div>
        </div>
      </section>

      {/* How it Works */}
      <section className="py-20 bg-slate-900/50">
        <div className="max-w-6xl mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-16">How It Works</h2>
          <div className="flex flex-wrap justify-center gap-8">
            {['Scan', 'Assess', 'Passport', 'Match', 'Reuse', 'Measure Impact'].map((step, i) => (
              <div key={i} className="flex flex-col items-center max-w-[150px] text-center">
                <div className="w-16 h-16 rounded-full bg-slate-800 flex items-center justify-center text-emerald-500 font-bold text-xl mb-4 border border-slate-700">
                  {i + 1}
                </div>
                <h3 className="font-semibold mb-2">{step}</h3>
              </div>
            ))}
          </div>
        </div>
      </section>
      
      {/* Agentic AI */}
      <section className="py-20 px-4">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-4">Powered by Agentic AI</h2>
          <p className="text-slate-400 text-center max-w-2xl mx-auto mb-12">Our specialized AI agents work autonomously to handle the entire lifecycle of recovered materials.</p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {['Vision Agent', 'Assessment Agent', 'Matching Agent', 'Pricing Agent', 'Logistics Agent', 'Impact Agent'].map((agent, i) => (
              <div key={i} className="bg-slate-800/50 border border-slate-700 rounded-xl p-6 hover:bg-slate-800 transition-colors">
                <div className="w-12 h-12 rounded-lg bg-emerald-500/10 text-emerald-500 flex items-center justify-center mb-4">
                  🤖
                </div>
                <h3 className="text-xl font-semibold mb-2">{agent}</h3>
                <p className="text-slate-400 text-sm">Specialized in autonomous analysis and decision-making for optimal circularity.</p>
              </div>
            ))}
          </div>
        </div>
      </section>
      
      {/* CTA */}
      <section className="py-24 px-4 text-center">
        <div className="max-w-3xl mx-auto glass rounded-2xl p-12 relative overflow-hidden">
          <div className="absolute top-0 right-0 w-64 h-64 bg-emerald-500/20 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2"></div>
          <h2 className="text-4xl font-bold mb-6 relative z-10">Ready to build sustainably?</h2>
          <p className="text-xl text-slate-300 mb-8 relative z-10">Join the movement to decarbonize construction in Kerala.</p>
          <Link href="/scan" className="relative z-10 bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-400 hover:to-teal-500 text-white px-8 py-4 rounded-lg font-semibold text-lg transition-all inline-block shadow-lg">
            Give a Material a Second Life
          </Link>
        </div>
      </section>
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

print("Generated initial files successfully.")
