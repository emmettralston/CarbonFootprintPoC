import { useEffect, useState } from "react";
import axios from "axios";


const API = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";


export default function Home() {
    const [items, setItems] = useState<any[]>([]);
    const [form, setForm] = useState({
        org_id: 1,
        scope: "2",
        category: "electricity",
        unit: "kWh",
        quantity: 1000,
        period_start: "2025-01-01",
        period_end: "2025-01-31",
        notes: "demo row"
    });


    async function load() {
        const res = await axios.get(`${API}/activities`, { headers: { "X-Org-Id": 1 } });
        setItems(res.data);
    }


    async function add() {
        await axios.post(`${API}/activities`, form, { headers: { "X-Org-Id": 1 } });
        await load();
    }


    useEffect(() => { load(); }, []);


    return (
        <main style={{ maxWidth: 720, margin: "40px auto", fontFamily: "ui-sans-serif" }}>
            <h1>Carbon Footprint PoC</h1>
            <p>Minimal demo: create an activity row (electricity kWh).</p>


            <button onClick={add} style={{ padding: 8, border: "1px solid #ddd" }}>
                Add Sample Activity
            </button>


            <h2 style={{ marginTop: 24 }}>Activities</h2>
            <pre>{JSON.stringify(items, null, 2)}</pre>
        </main>
    );
}