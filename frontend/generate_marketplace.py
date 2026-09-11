import os
base_dir = r"C:\Users\lenovo\.gemini\antigravity\scratch\material-rebirth-ai\frontend"

files = {
    "app/marketplace/page.tsx": """'use client';
import Link from 'next/link';

export default function MarketplacePage() {
  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Material Marketplace</h1>
        <div className="flex gap-4">
          <input type="text" placeholder="Search materials..." className="bg-slate-900 border border-slate-700 rounded-lg p-2 text-white w-64" />
          <button className="bg-slate-800 border border-slate-700 px-4 py-2 rounded-lg">Filter</button>
        </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {[1,2,3,4,5,6,7,8].map(i => (
          <Link href={`/materials/demo-id/passport`} key={i} className="bg-slate-800/50 border border-slate-700 rounded-xl overflow-hidden hover:border-emerald-500/50 hover:bg-slate-800 transition-all group">
            <div className="h-48 bg-gradient-to-br from-slate-700 to-slate-900 relative">
              <div className="absolute top-2 right-2 bg-emerald-500 text-white text-xs font-bold px-2 py-1 rounded-full">Score: 9{i}</div>
            </div>
            <div className="p-4">
              <h3 className="font-bold text-lg mb-1 group-hover:text-emerald-400 transition-colors">Reclaimed Red Bricks</h3>
              <div className="text-sm text-slate-400 mb-2">500 units • Kochi, Kerala</div>
              <div className="flex justify-between items-center mt-4 pt-4 border-t border-slate-700">
                <span className="font-bold text-white">₹12,500</span>
                <span className="text-xs text-emerald-500 bg-emerald-500/10 px-2 py-1 rounded">-45kg CO₂</span>
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
""",
    "app/materials/[id]/passport/page.tsx": """'use client';
import Link from 'next/link';

export default function MaterialPassportPage() {
  return (
    <div className="max-w-4xl mx-auto px-4 py-8 animate-fadeIn">
      <div className="bg-slate-800/50 border border-slate-700 rounded-xl overflow-hidden shadow-2xl">
        <div className="bg-gradient-to-r from-emerald-900/50 to-slate-900 p-8 border-b border-slate-700 flex justify-between items-start">
          <div>
            <div className="text-emerald-500 font-bold mb-2 tracking-widest text-sm">MATERIAL PASSPORT</div>
            <h1 className="text-3xl font-bold text-white mb-2">Reclaimed Red Bricks</h1>
            <p className="text-slate-400">ID: MR-1001-BRK</p>
          </div>
          <div className="w-24 h-24 bg-white p-2 rounded-lg flex justify-center items-center">
            {/* Fake QR */}
            <div className="w-full h-full bg-[url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMDAgMTAwIj48cGF0aCBkPSJNMTAgMTBoMzB2MzBIMTB6TTIwIDIwaDEwdjEwaC0xMHpNNjAgMTBoMzB2MzBINjB6TTcwIDIwaDEwdjEwaC0xMHpNMTAgNjBoMzB2MzBIMTB6TTIwIDcwaDEwdjEwaC0xMHpNNDAgMTBoMTB2MTBoLTEwek01MCAyMGgxMHYxMGgtMTB6TTQwIDQwaDEwdjEwaC0xMHpNNTAgNTBoMTB2MTBoLTEwek02MCA0MGgxMHYxMGgtMTB6TTcwIDUwaDEwdjEwaC0xMHpNNDAgNjBoMTB2MTBoLTEwek01MCA3MGgxMHYxMGgtMTB6TTYwIDYwaDEwdjEwaC0xMHpNNzAgNzBoMTB2MTBoLTEwek04MCA4MGgxMHYxMGgtMTB6IiBmaWxsPSIjMDAwIi8+PC9zdmc+')] bg-cover"></div>
          </div>
        </div>
        
        <div className="p-8 grid grid-cols-1 md:grid-cols-2 gap-12">
          <div className="space-y-6">
            <div>
              <h3 className="text-slate-500 text-sm font-semibold mb-1">Specifications</h3>
              <div className="grid grid-cols-2 gap-4 bg-slate-900 rounded-lg p-4 border border-slate-700">
                <div>
                  <div className="text-slate-500 text-xs">Quantity</div>
                  <div className="text-white font-medium">500 units</div>
                </div>
                <div>
                  <div className="text-slate-500 text-xs">Age</div>
                  <div className="text-white font-medium">~15 years</div>
                </div>
                <div>
                  <div className="text-slate-500 text-xs">Previous Use</div>
                  <div className="text-white font-medium">Residential Wall</div>
                </div>
                <div>
                  <div className="text-slate-500 text-xs">Source</div>
                  <div className="text-white font-medium">Kochi, Kerala</div>
                </div>
              </div>
            </div>
            
            <div>
              <h3 className="text-slate-500 text-sm font-semibold mb-1">AI Assessment</h3>
              <div className="bg-slate-900 rounded-lg p-4 border border-slate-700 space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-slate-400 text-sm">Condition</span>
                  <span className="text-emerald-400 font-medium">Excellent</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-slate-400 text-sm">Reuse Score</span>
                  <span className="text-white font-bold bg-emerald-500/20 px-2 py-1 rounded">92/100</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-slate-400 text-sm">AI Confidence</span>
                  <span className="text-blue-400 font-medium">95%</span>
                </div>
              </div>
            </div>
          </div>
          
          <div className="space-y-6">
            <div>
              <h3 className="text-slate-500 text-sm font-semibold mb-1">Impact & Value</h3>
              <div className="bg-slate-900 rounded-lg p-4 border border-slate-700 space-y-4">
                <div>
                  <div className="text-slate-400 text-sm mb-1">Estimated Value</div>
                  <div className="text-2xl font-bold text-white">₹12,500</div>
                </div>
                <div>
                  <div className="text-slate-400 text-sm mb-1">Carbon Avoided</div>
                  <div className="text-xl font-bold text-emerald-400 flex items-center gap-2">
                    <span className="text-2xl">🌱</span> 145 kg CO₂
                  </div>
                </div>
              </div>
            </div>
            
            <div>
              <h3 className="text-slate-500 text-sm font-semibold mb-1">Lifecycle Tracking</h3>
              <div className="bg-slate-900 rounded-lg p-4 border border-slate-700">
                <div className="flex items-center gap-3 text-sm text-emerald-400 font-medium">
                  <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></div>
                  Recovered & Assessed
                </div>
                <div className="flex items-center gap-3 text-sm text-slate-500 font-medium mt-3 pl-1 border-l-2 border-slate-800 ml-1 h-6">
                  <div className="w-2 h-2 rounded-full bg-slate-700 -ml-[5px]"></div>
                  Listed on Marketplace
                </div>
                <div className="flex items-center gap-3 text-sm text-slate-500 font-medium mt-3 pl-1 border-l-2 border-slate-800 ml-1 h-6">
                  <div className="w-2 h-2 rounded-full bg-slate-700 -ml-[5px]"></div>
                  Matched & Reused
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div className="p-8 bg-slate-900 border-t border-slate-700 flex gap-4">
          <button className="flex-1 bg-emerald-500 hover:bg-emerald-600 text-white py-3 rounded-lg font-medium transition-colors shadow-lg">List on Marketplace</button>
          <button className="flex-1 bg-slate-800 hover:bg-slate-700 border border-slate-700 text-white py-3 rounded-lg font-medium transition-colors">Find Buyers</button>
        </div>
      </div>
    </div>
  );
}
""",
    "app/matches/[id]/page.tsx": """'use client';

export default function MatchDetailPage() {
  return (
    <div className="max-w-5xl mx-auto px-4 py-8 animate-fadeIn">
      <div className="text-center mb-10">
        <div className="inline-block bg-emerald-500/20 text-emerald-400 px-4 py-1 rounded-full font-bold text-sm mb-4">
          AI MATCH RECOMMENDATION
        </div>
        <h1 className="text-4xl font-bold mb-4">94% Optimal Match</h1>
        <p className="text-slate-400">Found perfect fit between available materials and project requirements.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
        <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-6">
          <h3 className="text-slate-400 text-sm font-semibold mb-4 uppercase tracking-wider">Available Material</h3>
          <div className="text-2xl font-bold mb-1">Reclaimed Red Bricks</div>
          <div className="text-emerald-400 font-medium mb-4">500 units • Excellent Condition</div>
          <div className="text-slate-400 text-sm">Location: Kochi</div>
          <div className="text-slate-400 text-sm">Listed Price: ₹12,500</div>
        </div>
        
        <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-6">
          <h3 className="text-slate-400 text-sm font-semibold mb-4 uppercase tracking-wider">Project Requirement</h3>
          <div className="text-2xl font-bold mb-1">Interior Partition Wall</div>
          <div className="text-blue-400 font-medium mb-4">Needs: ~450 bricks</div>
          <div className="text-slate-400 text-sm">Location: Ernakulam</div>
          <div className="text-slate-400 text-sm">Budget: ₹15,000</div>
        </div>
      </div>

      <div className="bg-slate-900 border border-slate-700 rounded-xl p-8 mb-12">
        <h3 className="text-xl font-bold mb-6">Score Breakdown</h3>
        <div className="space-y-4">
          {[
            { l: 'Quantity Fit', v: 95 },
            { l: 'Quality Match', v: 90 },
            { l: 'Distance/Logistics', v: 98 },
            { l: 'Price Match', v: 100 },
          ].map(score => (
            <div key={score.l}>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-slate-300">{score.l}</span>
                <span className="text-emerald-400 font-bold">{score.v}/100</span>
              </div>
              <div className="w-full bg-slate-800 rounded-full h-2">
                <div className="bg-gradient-to-r from-emerald-600 to-emerald-400 h-2 rounded-full" style={{ width: `${score.v}%` }}></div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        <div className="col-span-1 md:col-span-2 bg-slate-800/50 border border-slate-700 rounded-xl p-6">
          <h3 className="font-bold mb-4">AI Explanation</h3>
          <p className="text-slate-300 text-sm leading-relaxed">
            This is an exceptional match. The required quantity (450) fits well within the available 500 units, leaving a small 10% buffer. 
            The material condition is 'Excellent', which perfectly suits the requirement for an interior partition wall. 
            Logistics are highly optimized as both locations are within 15km of each other in the Ernakulam district, minimizing transport emissions.
          </p>
        </div>
        <div className="bg-gradient-to-br from-emerald-900/40 to-slate-900 border border-emerald-500/30 rounded-xl p-6 flex flex-col justify-center items-center text-center">
          <div className="text-3xl mb-2">♻️</div>
          <div className="text-emerald-400 font-bold mb-1">MATERIAL REBORN</div>
          <div className="text-white text-xl font-bold mb-2">₹2,500 Saved</div>
          <div className="text-slate-400 text-sm">145 kg CO₂e avoided</div>
        </div>
      </div>

      <button className="w-full bg-emerald-500 hover:bg-emerald-600 text-white py-4 rounded-xl font-bold text-lg shadow-[0_0_20px_rgba(16,185,129,0.3)] hover:shadow-[0_0_30px_rgba(16,185,129,0.5)] transition-all">
        Accept Match & Initiate Transfer
      </button>
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

print("Generated marketplace and matches pages.")
