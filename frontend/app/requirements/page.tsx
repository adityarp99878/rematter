'use client';
import Link from 'next/link';

export default function RequirementsPage() {
  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Material Requirements</h1>
        <Link href="/requirements/new" className="bg-emerald-500 hover:bg-emerald-600 text-white px-4 py-2 rounded-lg font-medium transition-colors">
          + Post Requirement
        </Link>
      </div>
      
      <div className="space-y-4">
        {[1,2,3].map(i => (
          <div key={i} className="bg-slate-800/50 border border-slate-700 rounded-xl p-6 flex justify-between items-center hover:bg-slate-800 transition-colors cursor-pointer">
            <div>
              <div className="flex items-center gap-3 mb-2">
                <span className="bg-slate-700 text-xs px-2 py-1 rounded text-slate-300">REQ-{1000+i}</span>
                <h3 className="font-bold text-lg">Reclaimed Bricks for Partition Wall</h3>
              </div>
              <div className="text-sm text-slate-400 flex gap-4">
                <span>Quantity: 450 units</span>
                <span>Budget: ₹15,000</span>
                <span>Location: Ernakulam</span>
              </div>
            </div>
            <div className="text-right">
              <div className="text-emerald-500 font-bold mb-1">3 Matches Found</div>
              <Link href="/matches/demo" className="text-sm text-blue-400 hover:underline">View Matches</Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
