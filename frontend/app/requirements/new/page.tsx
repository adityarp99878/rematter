'use client';
export default function NewRequirementPage() {
  return (
    <div className="max-w-2xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Post New Requirement</h1>
      <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-8">
        <div className="space-y-6">
          <div>
            <label className="block text-sm text-slate-400 mb-2">Material Type</label>
            <select className="w-full bg-slate-900 border border-slate-700 rounded-lg p-3 text-white">
              <option>Brick</option><option>Steel</option><option>Wood</option>
            </select>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm text-slate-400 mb-2">Quantity Needed</label>
              <input type="number" className="w-full bg-slate-900 border border-slate-700 rounded-lg p-3 text-white" />
            </div>
            <div>
              <label className="block text-sm text-slate-400 mb-2">Unit</label>
              <select className="w-full bg-slate-900 border border-slate-700 rounded-lg p-3 text-white">
                <option>Units</option><option>kg</option><option>tonnes</option>
              </select>
            </div>
          </div>
          <div>
            <label className="block text-sm text-slate-400 mb-2">Max Budget (₹)</label>
            <input type="number" className="w-full bg-slate-900 border border-slate-700 rounded-lg p-3 text-white" />
          </div>
          <div>
            <label className="block text-sm text-slate-400 mb-2">Location</label>
            <select className="w-full bg-slate-900 border border-slate-700 rounded-lg p-3 text-white">
              <option>Ernakulam</option><option>Trivandrum</option>
            </select>
          </div>
          <button className="w-full bg-emerald-500 hover:bg-emerald-600 text-white py-3 rounded-lg font-bold transition-colors">
            Post Requirement
          </button>
        </div>
      </div>
    </div>
  );
}
