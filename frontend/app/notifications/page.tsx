'use client';
export default function NotificationsPage() {
  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Notifications</h1>
      <div className="space-y-4">
        {[
          {title: 'New Match Found', desc: 'AI found a 94% match for your Reclaimed Bricks', time: '10 mins ago', unread: true},
          {title: 'Passport Generated', desc: 'Material Passport for MR-1001-BRK is ready', time: '2 hours ago', unread: false},
        ].map((n, i) => (
          <div key={i} className={`p-4 rounded-xl border ${n.unread ? 'bg-slate-800 border-slate-600' : 'bg-slate-900 border-slate-800'}`}>
            <h3 className={`font-bold ${n.unread ? 'text-white' : 'text-slate-300'}`}>{n.title}</h3>
            <p className="text-sm text-slate-400 mt-1">{n.desc}</p>
            <div className="text-xs text-slate-500 mt-2">{n.time}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
