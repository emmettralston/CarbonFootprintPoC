import { useEffect, useMemo, useState } from "react";
import { api } from "../lib/api";

export default function DashboardPage() {
  const [orgId, setOrgId] = useState(1);
  const [start, setStart] = useState("2025-01-01");
  const [end, setEnd] = useState("2025-01-31");
  const [byScope, setByScope] = useState<Record<string, number>>({});
  const [byCategory, setByCategory] = useState<Record<string, number>>({});
  const [total, setTotal] = useState<number>(0);
  const [loading, setLoading] = useState(false);

  const query = useMemo(() => `org_id=${orgId}&period_start=${start}&period_end=${end}`, [orgId, start, end]);

  const load = async () => {
    setLoading(true);
    try {
      const [scopeRes, catRes, calcRes] = await Promise.all([
        api.get(`/emissions/summary?${query}&group_by=scope`),
        api.get(`/emissions/summary?${query}&group_by=category`),
        api.get(`/calculate/run?${query}`), // you switched to GET above
      ]);
      setByScope(scopeRes.data || {});
      setByCategory(catRes.data || {});
      setTotal(calcRes.data?.total_kg ?? 0);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, [query]);

  return (
    <main className="max-w-4xl mx-auto p-6 space-y-8">
      <h1 className="text-2xl font-bold">Emissions Dashboard</h1>

      <section className="grid md:grid-cols-4 gap-4 items-end">
        <div>
          <label className="block text-sm font-medium">Org</label>
          <input type="number" className="border rounded p-2 w-full" value={orgId} onChange={e => setOrgId(Number(e.target.value))} />
        </div>
        <div>
          <label className="block text-sm font-medium">Start</label>
          <input type="date" className="border rounded p-2 w-full" value={start} onChange={e => setStart(e.target.value)} />
        </div>
        <div>
          <label className="block text-sm font-medium">End</label>
          <input type="date" className="border rounded p-2 w-full" value={end} onChange={e => setEnd(e.target.value)} />
        </div>
        <button onClick={load} className="bg-black text-white rounded px-4 py-2">{loading ? "Loading..." : "Refresh"}</button>
      </section>

      <section className="grid md:grid-cols-3 gap-4">
        <div className="border rounded p-4">
          <div className="text-sm text-gray-500">Total (kgCO₂e)</div>
          <div className="text-3xl font-bold">{total.toFixed(1)}</div>
        </div>
        <div className="border rounded p-4">
          <div className="text-sm text-gray-500 mb-2">By Scope (kg)</div>
          <ul className="space-y-1">
            {Object.entries(byScope).map(([k,v]) => (
              <li key={k} className="flex justify-between"><span>Scope {k}</span><span>{v.toFixed(1)}</span></li>
            ))}
          </ul>
        </div>
        <div className="border rounded p-4">
          <div className="text-sm text-gray-500 mb-2">By Category (kg)</div>
          <ul className="space-y-1">
            {Object.entries(byCategory).map(([k,v]) => (
              <li key={k} className="flex justify-between"><span>{k}</span><span>{v.toFixed(1)}</span></li>
            ))}
          </ul>
        </div>
      </section>
    </main>
  );
}
