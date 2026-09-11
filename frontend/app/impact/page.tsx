"use client";

import { useEffect, useState } from 'react';
import { BarChart, Bar, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { Leaf, IndianRupee, Recycle, ArrowUpRight, Factory } from 'lucide-react';
import { getDashboardStats } from '@/lib/api';

const monthlyData = [
  { name: 'Jan', reused: 4000, co2: 2400 },
  { name: 'Feb', reused: 3000, co2: 1398 },
  { name: 'Mar', reused: 2000, co2: 9800 },
  { name: 'Apr', reused: 2780, co2: 3908 },
  { name: 'May', reused: 1890, co2: 4800 },
  { name: 'Jun', reused: 2390, co2: 3800 },
  { name: 'Jul', reused: 3490, co2: 4300 },
];

const categoryData = [
  { name: 'Wood', value: 400, color: '#f59e0b' },
  { name: 'Concrete', value: 300, color: '#94a3b8' },
  { name: 'Metal', value: 300, color: '#3b82f6' },
  { name: 'Glass', value: 200, color: '#06b6d4' },
];

export default function ImpactPage() {
  const [stats, setStats] = useState<any>(null);

  useEffect(() => {
    getDashboardStats().then(data => setStats(data));
  }, []);

  const co2AvoidedKg = stats?.impact?.co2_avoided_kg || 0;
  const wasteDivertedKg = stats?.impact?.waste_diverted_kg || 0;
  const valueRecovered = stats?.impact?.value_recovered || 0;

  return (
    <div className="max-w-7xl mx-auto space-y-8 animate-fade-in">
      <div>
        <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-emerald-400 to-teal-300">
          Environmental Impact
        </h1>
        <p className="text-slate-400 mt-2">
          Track the real-world impact of your circular construction decisions.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="glass p-6 rounded-xl border border-slate-700/50">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-green-500/10 rounded-lg">
              <Leaf className="h-5 w-5 text-green-400" />
            </div>
            <h3 className="text-slate-400 font-medium">CO2 Avoided</h3>
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-3xl font-bold">{co2AvoidedKg.toLocaleString()}</span>
            <span className="text-slate-500">kg</span>
          </div>
          <div className="text-xs text-emerald-400 flex items-center gap-1 mt-2">
            <ArrowUpRight className="h-3 w-3" /> 12% vs last month
          </div>
        </div>

        <div className="glass p-6 rounded-xl border border-slate-700/50">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-blue-500/10 rounded-lg">
              <Factory className="h-5 w-5 text-blue-400" />
            </div>
            <h3 className="text-slate-400 font-medium">Waste Diverted</h3>
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-3xl font-bold">{wasteDivertedKg.toLocaleString()}</span>
            <span className="text-slate-500">kg</span>
          </div>
          <div className="text-xs text-emerald-400 flex items-center gap-1 mt-2">
            <ArrowUpRight className="h-3 w-3" /> 8% vs last month
          </div>
        </div>

        <div className="glass p-6 rounded-xl border border-slate-700/50">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-amber-500/10 rounded-lg">
              <IndianRupee className="h-5 w-5 text-amber-400" />
            </div>
            <h3 className="text-slate-400 font-medium">Value Recovered</h3>
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-xl font-bold">₹{valueRecovered.toLocaleString()}</span>
          </div>
          <div className="text-xs text-emerald-400 flex items-center gap-1 mt-2">
            <ArrowUpRight className="h-3 w-3" /> 24% vs last month
          </div>
        </div>

        <div className="glass p-6 rounded-xl border border-emerald-500/30 relative overflow-hidden group">
          <div className="absolute inset-0 bg-emerald-500/5 group-hover:bg-emerald-500/10 transition-colors" />
          <div className="relative z-10">
            <div className="flex items-center gap-3 mb-2">
              <div className="p-2 bg-emerald-500/20 rounded-lg">
                <Recycle className="h-5 w-5 text-emerald-400" />
              </div>
              <h3 className="text-emerald-100 font-medium">Circularity Score</h3>
            </div>
            <div className="flex items-baseline gap-2">
              <span className="text-4xl font-bold text-emerald-400">84</span>
              <span className="text-emerald-500/50">/100</span>
            </div>
            <div className="text-xs text-emerald-300 mt-2">Top 15% of builders</div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="glass p-6 rounded-xl border border-slate-700/50">
          <h3 className="text-lg font-bold mb-6">CO2 Impact Over Time</h3>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={monthlyData}>
                <defs>
                  <linearGradient id="colorCo2" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10b981" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" vertical={false} />
                <XAxis dataKey="name" stroke="#94a3b8" tick={{fill: '#94a3b8'}} />
                <YAxis stroke="#94a3b8" tick={{fill: '#94a3b8'}} />
                <RechartsTooltip 
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px' }}
                  itemStyle={{ color: '#10b981' }}
                />
                <Area type="monotone" dataKey="co2" stroke="#10b981" fillOpacity={1} fill="url(#colorCo2)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="glass p-6 rounded-xl border border-slate-700/50">
          <h3 className="text-lg font-bold mb-6">Materials Reused by Category</h3>
          <div className="h-72 flex items-center justify-center">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={categoryData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {categoryData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <RechartsTooltip 
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px' }}
                />
              </PieChart>
            </ResponsiveContainer>
            <div className="flex flex-col justify-center space-y-3 pl-4">
              {categoryData.map((entry, idx) => (
                <div key={idx} className="flex items-center gap-2 text-sm">
                  <div className="w-3 h-3 rounded-full" style={{ backgroundColor: entry.color }}></div>
                  <span className="text-slate-300">{entry.name}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
