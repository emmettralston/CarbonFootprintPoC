import { useEffect, useMemo, useState } from "react";
import { api } from "../lib/api";
import type { Activity } from "../types";

const scopes = [
  { value: "1", label: "Scope 1" },
  { value: "2", label: "Scope 2" },
  { value: "3", label: "Scope 3" },
];

const categories = [
  "electricity",
  "diesel",
  "gasoline",
  "natural_gas",
  "distance",
  "refrigerant",
  "spend",
];

export default function ActivitiesPage() {
  const [form, setForm] = useState({
    org_id: 1,
    scope: "2",
    category: "electricity",
    unit: "kWh",
    quantity: 100,
    period_start: "2025-01-01",
    period_end: "2025-01-31",
    notes: "",
  });

  const [filters, setFilters] = useState({
    org_id: 1,
    scope: "",
    category: "",
    period_start: "2025-01-01",
    period_end: "2025-12-31",
  });

  const [rows, setRows] = useState<Activity[]>([]);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const query = useMemo(() => {
    const p = new URLSearchParams();
    if (filters.org_id) p.set("org_id", String(filters.org_id));
    if (filters.scope) p.set("scope", filters.scope);
    if (filters.category) p.set("category", filters.category);
    if (filters.period_start) p.set("period_start", filters.period_start);
    if (filters.period_end) p.set("period_end", filters.period_end);
    return p.toString();
  }, [filters]);

  const load = async () => {
    setLoading(true);
    setError(null);
    try {
      const { data } = await api.get<Activity[]>(`/activities?${query}`);
      setRows(data);
    } catch (e: any) {
      setError(e?.response?.data?.detail || "Failed to load activities");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, [query]);

  const create = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      await api.post<Activity>("/activities", form);
      await load();
    } catch (e: any) {
      setError(e?.response?.data?.detail || "Create failed");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <main className="max-w-5xl mx-auto p-6 space-y-8">
      <h1 className="text-2xl font-bold">Activities</h1>

      {/* Create Form */}
      <form onSubmit={create} className="grid md:grid-cols-4 gap-4 items-end">
        <div>
          <label className="block text-sm font-medium">Org</label>
          <input
            type="number"
            className="border rounded p-2 w-full"
            value={form.org_id}
            onChange={(e) => setForm({ ...form, org_id: Number(e.target.value) })}
          />
        </div>

        <div>
          <label className="block text-sm font-medium">Scope</label>
          <select
            className="border rounded p-2 w-full"
            value={form.scope}
            onChange={(e) => setForm({ ...form, scope: e.target.value })}
          >
            {scopes.map(s => <option key={s.value} value={s.value}>{s.label}</option>)}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium">Category</label>
          <select
            className="border rounded p-2 w-full"
            value={form.category}
            onChange={(e) => setForm({ ...form, category: e.target.value })}
          >
            {categories.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium">Unit</label>
          <input
            className="border rounded p-2 w-full"
            value={form.unit}
            onChange={(e) => setForm({ ...form, unit: e.target.value })}
          />
        </div>

        <div>
          <label className="block text-sm font-medium">Quantity</label>
          <input
            type="number" step="any"
            className="border rounded p-2 w-full"
            value={form.quantity}
            onChange={(e) => setForm({ ...form, quantity: Number(e.target.value) })}
          />
        </div>

        <div>
          <label className="block text-sm font-medium">Start</label>
          <input
            type="date"
            className="border rounded p-2 w-full"
            value={form.period_start}
            onChange={(e) => setForm({ ...form, period_start: e.target.value })}
          />
        </div>

        <div>
          <label className="block text-sm font-medium">End</label>
          <input
            type="date"
            className="border rounded p-2 w-full"
            value={form.period_end}
            onChange={(e) => setForm({ ...form, period_end: e.target.value })}
          />
        </div>

        <div className="md:col-span-3">
          <label className="block text-sm font-medium">Notes</label>
          <input
            className="border rounded p-2 w-full"
            value={form.notes}
            onChange={(e) => setForm({ ...form, notes: e.target.value })}
          />
        </div>

        <button
          disabled={submitting}
          className="bg-black text-white rounded px-4 py-2"
        >
          {submitting ? "Saving..." : "Add Activity"}
        </button>
      </form>

      {/* Filters */}
      <section className="grid md:grid-cols-6 gap-4 items-end">
        <div>
          <label className="block text-sm font-medium">Scope</label>
          <select
            className="border rounded p-2 w-full"
            value={filters.scope}
            onChange={(e) => setFilters({ ...filters, scope: e.target.value })}
          >
            <option value="">Any</option>
            {scopes.map(s => <option key={s.value} value={s.value}>{s.label}</option>)}
          </select>
        </div>
        <div className="md:col-span-2">
          <label className="block text-sm font-medium">Category</label>
          <input
            className="border rounded p-2 w-full"
            value={filters.category}
            onChange={(e) => setFilters({ ...filters, category: e.target.value })}
            placeholder="electricity / diesel ..."
          />
        </div>
        <div>
          <label className="block text-sm font-medium">Start</label>
          <input
            type="date"
            className="border rounded p-2 w-full"
            value={filters.period_start}
            onChange={(e) => setFilters({ ...filters, period_start: e.target.value })}
          />
        </div>
        <div>
          <label className="block text-sm font-medium">End</label>
          <input
            type="date"
            className="border rounded p-2 w-full"
            value={filters.period_end}
            onChange={(e) => setFilters({ ...filters, period_end: e.target.value })}
          />
        </div>
        <button onClick={load} className="bg-gray-800 text-white rounded px-4 py-2">Refresh</button>
      </section>

      {error && <p className="text-red-600">{error}</p>}

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full border rounded">
          <thead className="bg-gray-50">
            <tr>
              <th className="text-left p-2">ID</th>
              <th className="text-left p-2">Scope</th>
              <th className="text-left p-2">Category</th>
              <th className="text-left p-2">Unit</th>
              <th className="text-left p-2">Qty</th>
              <th className="text-left p-2">Start</th>
              <th className="text-left p-2">End</th>
            </tr>
          </thead>
          <tbody>
            {rows.map(r => (
              <tr key={r.id} className="border-t">
                <td className="p-2">{r.id}</td>
                <td className="p-2">{r.scope}</td>
                <td className="p-2">{r.category}</td>
                <td className="p-2">{r.unit}</td>
                <td className="p-2">{r.quantity}</td>
                <td className="p-2">{r.period_start}</td>
                <td className="p-2">{r.period_end}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </main>
  );
}
