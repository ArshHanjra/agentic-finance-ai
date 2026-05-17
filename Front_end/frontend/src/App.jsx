import { useEffect, useState, useCallback } from "react";
import axios from "axios";
import {
  PieChart, Pie, Cell, Tooltip, ResponsiveContainer,
  AreaChart, Area, XAxis, YAxis, CartesianGrid,
  BarChart, Bar, Legend,
} from "recharts";

const API = "http://127.0.0.1:8000";

const PALETTE = ["#7c6af7", "#22d3ee", "#34d399", "#fbbf24", "#fb7185", "#a78bfa"];

const INR = (n) =>
  "\u20B9" + Number(n).toLocaleString("en-IN", { maximumFractionDigits: 0 });

const fmtDate = (iso) =>
  iso
    ? new Date(iso).toLocaleDateString("en-IN", { day: "numeric", month: "short" })
    : "—";

const catEmoji = (cat = "") => {
  const c = cat.toLowerCase();
  if (c.includes("food") || c.includes("grocery")) return "🍱";
  if (c.includes("transport") || c.includes("uber")) return "🚗";
  if (c.includes("entertain") || c.includes("netflix")) return "🎬";
  if (c.includes("shop") || c.includes("amazon")) return "🛍️";
  if (c.includes("bill") || c.includes("util")) return "💡";
  if (c.includes("health") || c.includes("gym")) return "🏥";
  return "💳";
};

/* ── Tooltip ── */
const ChartTip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <div style={{
      background: "#0d1b2a", border: "1px solid #1e3a52",
      borderRadius: 10, padding: "8px 13px", fontSize: "0.8rem",
    }}>
      {label && <div style={{ color: "#456780", marginBottom: 3 }}>{label}</div>}
      {payload.map((p, i) => (
        <div key={i} style={{ color: p.color ?? "#94c4e0", fontWeight: 700 }}>
          {INR(p.value)}
        </div>
      ))}
    </div>
  );
};

/* ── Stat card ── */
function StatCard({ label, value, emoji, accent, loading }) {
  return (
    <div style={{
      background: "linear-gradient(135deg, #0d1b2a 60%, #111f30)",
      border: `1px solid ${accent}28`,
      borderRadius: 16, padding: "18px 20px",
      position: "relative", overflow: "hidden",
    }}>
      <div style={{
        position: "absolute", top: -18, right: -18,
        width: 72, height: 72, borderRadius: "50%",
        background: accent, opacity: 0.08,
      }} />
      <div style={{ fontSize: 24, marginBottom: 10, lineHeight: 1 }}>{emoji}</div>
      {loading
        ? <div style={{ height: 30, width: "55%", borderRadius: 6, background: "#1e3a52" }} />
        : <div style={{
            fontSize: "1.6rem", fontWeight: 800, color: accent,
            fontFamily: "'DM Mono', monospace", letterSpacing: "-0.03em", lineHeight: 1,
          }}>{value}</div>
      }
      <div style={{
        color: "#2d5070", fontSize: "0.68rem", fontWeight: 700,
        textTransform: "uppercase", letterSpacing: "0.12em", marginTop: 8,
      }}>{label}</div>
    </div>
  );
}

/* ── Panel ── */
function Panel({ title, emoji, children, right, style = {} }) {
  return (
    <div style={{
      background: "#090f1a",
      border: "1px solid #162030",
      borderRadius: 18, overflow: "hidden",
      marginBottom: 16, ...style,
    }}>
      <div style={{
        display: "flex", alignItems: "center",
        justifyContent: "space-between",
        padding: "14px 20px",
        borderBottom: "1px solid #162030",
        background: "#0a1420",
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: 9 }}>
          <span style={{ fontSize: 16, lineHeight: 1 }}>{emoji}</span>
          <span style={{ fontWeight: 700, fontSize: "0.88rem", color: "#a0bfd4", letterSpacing: "0.01em" }}>{title}</span>
        </div>
        {right}
      </div>
      <div style={{ padding: "18px 20px" }}>{children}</div>
    </div>
  );
}

/* ── Badge ── */
function Badge({ text, color = "#7c6af7" }) {
  return (
    <span style={{
      background: color + "18",
      color,
      border: `1px solid ${color}44`,
      borderRadius: 999, padding: "3px 9px",
      fontSize: "0.68rem", fontWeight: 700,
      letterSpacing: "0.05em", whiteSpace: "nowrap",
    }}>{text}</span>
  );
}

/* ── Skeleton line ── */
const Skel = ({ w = "100%", h = 14, mb = 0 }) => (
  <div style={{
    height: h, width: w, borderRadius: 6,
    background: "#162030", marginBottom: mb,
    animation: "pulse 1.8s ease infinite",
  }} />
);

/* ── Progress bar ── */
function ProgressBar({ pct, color, over }) {
  return (
    <div style={{ background: "#162030", borderRadius: 999, height: 5, overflow: "hidden" }}>
      <div style={{
        width: `${Math.min(pct, 100)}%`, height: "100%",
        background: over ? "#fb7185" : color,
        borderRadius: 999,
        transition: "width .7s cubic-bezier(.34,1.56,.64,1)",
      }} />
    </div>
  );
}

/* ═══════════════════════════════════════════ */
export default function App() {
  const [analysis,     setAnalysis]     = useState(null);
  const [transactions, setTransactions] = useState([]);
  const [description,  setDescription]  = useState("");
  const [amount,       setAmount]       = useState("");
  const [question,     setQuestion]     = useState("");
  const [answer,       setAnswer]       = useState("");
  const [loading,      setLoading]      = useState(true);
  const [adding,       setAdding]       = useState(false);
  const [asking,       setAsking]       = useState(false);
  const [error,        setError]        = useState("");
  const [addErr,       setAddErr]       = useState("");

  const fetchAll = useCallback(async () => {
    setLoading(true); setError("");
    try {
      const [aRes, tRes] = await Promise.all([
        axios.get(`${API}/full-analysis`),
        axios.get(`${API}/transactions`),
      ]);
      setAnalysis(aRes.data);
      setTransactions(tRes.data);
    } catch {
      setError("Backend offline — start the FastAPI server and refresh.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchAll(); }, [fetchAll]);

  const addTransaction = async () => {
    if (!description.trim() || !amount || adding) return;
    setAdding(true); setAddErr("");
    try {
      await axios.post(`${API}/add-transaction`, {
        description: description.trim(),
        amount: parseFloat(amount),
      });
      setDescription(""); setAmount("");
      await fetchAll();
    } catch (e) {
      setAddErr(e.response?.data?.detail ?? "Failed to save.");
    } finally {
      setAdding(false);
    }
  };

  const askQuestion = async () => {
    if (!question.trim() || asking) return;
    setAsking(true); setAnswer("");
    try {
      const r = await axios.post(`${API}/ask`, { question: question.trim() });
      setAnswer(r.data.answer);
    } catch {
      setAnswer("AI offline — make sure Ollama is running.");
    } finally {
      setAsking(false);
    }
  };

  const budget   = analysis?.budget_plan?.budget_analysis  || analysis?.budget?.budget_analysis || [];
  const forecast = analysis?.forecast?.predicted_next_month_spending || 0;
  const total    = analysis?.budget_plan?.total_spending    || analysis?.budget?.total_spending
                   || transactions.reduce((s, t) => s + Number(t.amount || 0), 0);
  const savings  = analysis?.budget_plan?.savings_potential || analysis?.budget?.savings_potential || 0;
  const insight  = analysis?.insights || analysis?.insight  || "Add transactions to get AI-powered insights.";
  const warnings = analysis?.warnings || [];

  const sparkData = [...transactions].reverse().slice(-14).map((t, i) => ({ i, v: parseFloat(t.amount) }));

  const inp = {
    background: "#0d1b2a", border: "1px solid #1e3a52",
    borderRadius: 10, color: "#94c4e0",
    padding: "10px 14px", fontSize: "0.9rem",
    fontFamily: "inherit", outline: "none",
  };

  const btnPrimary = {
    background: "#7c6af7", color: "#fff",
    border: "none", borderRadius: 10,
    padding: "10px 22px", fontWeight: 700,
    fontSize: "0.88rem", cursor: "pointer",
    fontFamily: "inherit", letterSpacing: "0.02em",
    opacity: (adding || !description.trim() || !amount) ? 0.4 : 1,
    transition: "opacity .2s, transform .1s",
  };

  const btnAsk = {
    background: "#22d3ee", color: "#07131d",
    border: "none", borderRadius: 10,
    padding: "10px 22px", fontWeight: 700,
    fontSize: "0.88rem", cursor: "pointer",
    fontFamily: "inherit", letterSpacing: "0.02em",
    opacity: (asking || !question.trim()) ? 0.4 : 1,
    transition: "opacity .2s",
  };

  return (
    <>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Instrument+Serif&family=DM+Mono:wght@400;500&family=Manrope:wght@400;600;700;800&display=swap');
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        body { background: #060c16; }
        input { transition: border-color .2s, box-shadow .2s; }
        input:focus { border-color: #7c6af7 !important; box-shadow: 0 0 0 3px #7c6af720; }
        .tx-row:hover { background: #0d1b2a; border-radius: 10px; }
        .refresh-btn:hover { border-color: #2d5070 !important; color: #94c4e0 !important; }
        .chip-btn:hover { border-color: #7c6af7 !important; color: #a5b4fc !important; }
        @keyframes pulse { 0%,100%{opacity:.5} 50%{opacity:1} }
        @keyframes blink  { 0%,100%{opacity:1} 50%{opacity:.2} }
        @keyframes rise   { from{opacity:0;transform:translateY(12px)} to{opacity:1;transform:translateY(0)} }
        .page { animation: rise .4s ease; }
      `}</style>

      <div className="page" style={{
        background: "#060c16", minHeight: "100vh",
        color: "#94c4e0", fontFamily: "'Manrope', sans-serif",
        padding: "28px 22px", maxWidth: 1160, margin: "0 auto",
      }}>

        {/* ── Header ── */}
        <div style={{
          display: "flex", alignItems: "flex-start",
          justifyContent: "space-between", marginBottom: 28,
          paddingBottom: 24, borderBottom: "1px solid #162030",
        }}>
          <div>
            <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 6 }}>
              <div style={{
                width: 38, height: 38, borderRadius: 11,
                background: "linear-gradient(135deg, #7c6af7, #22d3ee)",
                display: "flex", alignItems: "center",
                justifyContent: "center", fontSize: 20,
              }}>📊</div>
              <h1 style={{
                fontFamily: "'Instrument Serif', serif",
                fontSize: "1.9rem", fontWeight: 400,
                color: "#d4eaf5", letterSpacing: "-0.02em",
              }}>FinanceAI</h1>
              <span style={{
                background: "#7c6af718", color: "#a5b4fc",
                border: "1px solid #7c6af740",
                borderRadius: 999, padding: "2px 9px",
                fontSize: "0.65rem", fontWeight: 700,
                letterSpacing: "0.1em", textTransform: "uppercase",
              }}>Beta</span>
            </div>
            <p style={{ color: "#2d5070", fontSize: "0.78rem", letterSpacing: "0.02em" }}>
              Multi-agent personal finance dashboard · FastAPI · PostgreSQL · Ollama
            </p>
          </div>
          <button
            className="refresh-btn"
            onClick={fetchAll}
            style={{
              background: "transparent", border: "1px solid #162030",
              borderRadius: 10, color: "#2d5070",
              padding: "8px 16px", cursor: "pointer",
              fontSize: "0.8rem", fontFamily: "inherit",
              fontWeight: 600, display: "flex",
              alignItems: "center", gap: 6, transition: "all .2s",
            }}
          >
            ↻ Refresh
          </button>
        </div>

        {/* ── Error banner ── */}
        {error && (
          <div style={{
            background: "#1a0a0e", border: "1px solid #7f1d1d",
            borderRadius: 12, padding: "12px 16px",
            marginBottom: 20, color: "#fca5a5", fontSize: "0.84rem",
            display: "flex", alignItems: "center", gap: 10,
          }}>
            <span>⚠️</span> {error}
          </div>
        )}

        {/* ── Stats grid ── */}
        <div style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
          gap: 13, marginBottom: 20,
        }}>
          <StatCard label="Total Spent"          value={loading ? "—" : INR(total)}    emoji="💸" accent="#7c6af7" loading={loading} />
          <StatCard label="Transactions"         value={loading ? "—" : transactions.length} emoji="📋" accent="#22d3ee" loading={loading} />
          <StatCard label="Next Month Forecast"  value={loading ? "—" : INR(forecast)} emoji="📈" accent="#fbbf24" loading={loading} />
          <StatCard label="Savings Potential"    value={loading ? "—" : INR(savings)}  emoji="🏦" accent="#34d399" loading={loading} />
        </div>

        {/* ── Add Transaction ── */}
        <Panel title="Add Transaction" emoji="➕">
          <div style={{ display: "flex", gap: 11, flexWrap: "wrap" }}>
            <input
              type="text"
              placeholder="Description (e.g. Uber ride to office)"
              value={description}
              onChange={e => setDescription(e.target.value)}
              onKeyDown={e => e.key === "Enter" && addTransaction()}
              style={{ ...inp, flex: "1 1 250px" }}
            />
            <input
              type="number"
              placeholder="Amount (₹)"
              value={amount}
              onChange={e => setAmount(e.target.value)}
              onKeyDown={e => e.key === "Enter" && addTransaction()}
              style={{ ...inp, width: 150 }}
            />
            <button
              style={btnPrimary}
              onClick={addTransaction}
              disabled={adding || !description.trim() || !amount}
            >
              {adding ? "Saving…" : "Add"}
            </button>
          </div>
          {addErr && (
            <p style={{ color: "#fb7185", marginTop: 9, fontSize: "0.82rem" }}>⚠️ {addErr}</p>
          )}
        </Panel>

        {/* ── Insights + Warnings ── */}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginBottom: 16 }}>
          <Panel title="AI Insights" emoji="🤖">
            {loading
              ? <><Skel w="90%" mb={8} /><Skel w="75%" mb={8} /><Skel w="60%" /></>
              : <p style={{ color: "#5a8ca8", lineHeight: 1.8, fontSize: "0.87rem" }}>
                  {insight}
                </p>
            }
          </Panel>

          <Panel title="Spending Warnings" emoji="⚠️">
            {loading
              ? <><Skel w="85%" mb={8} /><Skel w="70%" /></>
              : warnings.length === 0
                ? <p style={{ color: "#2d5070", fontSize: "0.84rem" }}>No warnings — all clear! ✅</p>
                : <ul style={{ listStyle: "none", display: "flex", flexDirection: "column", gap: 9 }}>
                    {warnings.map((w, i) => {
                      const ok = w.startsWith("✅") || w.startsWith("👍");
                      return (
                        <li key={i} style={{
                          color: "#5a8ca8", fontSize: "0.84rem", lineHeight: 1.7,
                          paddingLeft: 12,
                          borderLeft: `2px solid ${ok ? "#34d399" : "#fbbf24"}`,
                        }}>{w}</li>
                      );
                    })}
                  </ul>
            }
          </Panel>
        </div>

        {/* ── Charts ── */}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginBottom: 16 }}>
          <Panel title="Spending by Category" emoji="🪙">
            {!loading && budget.length > 0 ? (
              <>
                <ResponsiveContainer width="100%" height={210}>
                  <PieChart>
                    <Pie
                      data={budget} dataKey="spent" nameKey="category"
                      cx="50%" cy="50%" innerRadius={54} outerRadius={86} paddingAngle={3}
                    >
                      {budget.map((_, i) => (
                        <Cell key={i} fill={PALETTE[i % PALETTE.length]} stroke="transparent" />
                      ))}
                    </Pie>
                    <Tooltip content={<ChartTip />} />
                  </PieChart>
                </ResponsiveContainer>
                <div style={{ display: "flex", flexWrap: "wrap", gap: "5px 14px", justifyContent: "center", marginTop: 8 }}>
                  {budget.map((b, i) => (
                    <div key={i} style={{ display: "flex", alignItems: "center", gap: 6, fontSize: "0.72rem", color: "#456780" }}>
                      <div style={{ width: 7, height: 7, borderRadius: "50%", background: PALETTE[i % PALETTE.length] }} />
                      {b.category}
                    </div>
                  ))}
                </div>
              </>
            ) : (
              <div style={{ height: 230, display: "flex", alignItems: "center", justifyContent: "center", color: "#162030", fontSize: "0.83rem" }}>
                No data yet
              </div>
            )}
          </Panel>

          <Panel title="Recent Spending Trend" emoji="📉">
            {!loading && sparkData.length > 1 ? (
              <ResponsiveContainer width="100%" height={240}>
                <AreaChart data={sparkData} margin={{ top: 10, right: 0, left: -18, bottom: 0 }}>
                  <defs>
                    <linearGradient id="grad1" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%"  stopColor="#7c6af7" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="#7c6af7" stopOpacity={0}   />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#0d1b2a" />
                  <XAxis dataKey="i" tick={false} axisLine={false} tickLine={false} />
                  <YAxis
                    tick={{ fill: "#2d5070", fontSize: 11 }}
                    axisLine={false} tickLine={false}
                    tickFormatter={v => "₹" + v}
                  />
                  <Tooltip content={<ChartTip />} />
                  <Area
                    type="monotone" dataKey="v"
                    stroke="#7c6af7" strokeWidth={2.5}
                    fill="url(#grad1)" dot={false}
                  />
                </AreaChart>
              </ResponsiveContainer>
            ) : (
              <div style={{ height: 240, display: "flex", alignItems: "center", justifyContent: "center", color: "#162030", fontSize: "0.83rem" }}>
                No data yet
              </div>
            )}
          </Panel>
        </div>

        {/* ── Budget Plan ── */}
        <Panel
          title="Budget Plan"
          emoji="📋"
          right={!loading && savings > 0
            ? <Badge text={`Save up to ${INR(savings)}`} color="#34d399" />
            : null}
        >
          {loading ? (
            <><Skel mb={12} /><Skel w="80%" mb={12} /><Skel w="90%" /></>
          ) : budget.length === 0 ? (
            <p style={{ color: "#2d5070", fontSize: "0.84rem" }}>Add transactions to generate your budget plan.</p>
          ) : (
            <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
              {budget.map((item, i) => {
                const col  = PALETTE[i % PALETTE.length];
                const over = item.status === "over_budget";
                const pct  = Math.round((item.spent / (item.recommended_budget || 1)) * 100);
                return (
                  <div key={i} style={{
                    background: "#0d1b2a", borderRadius: 13,
                    padding: "14px 16px", border: "1px solid #162030",
                  }}>
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 10 }}>
                      <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                        <span style={{ fontSize: 20, lineHeight: 1 }}>{catEmoji(item.category)}</span>
                        <div>
                          <div style={{ fontWeight: 700, fontSize: "0.86rem", color: "#b0cfe6" }}>{item.category}</div>
                          {item.advice && (
                            <div style={{ color: "#2d5070", fontSize: "0.72rem", marginTop: 2 }}>{item.advice}</div>
                          )}
                        </div>
                      </div>
                      <div style={{ textAlign: "right" }}>
                        <div style={{ fontFamily: "'DM Mono', monospace", fontWeight: 700, color: col, fontSize: "0.95rem" }}>
                          {INR(item.spent)}
                        </div>
                        <div style={{ color: "#2d5070", fontSize: "0.7rem", marginTop: 2 }}>
                          of {INR(item.recommended_budget)}
                        </div>
                      </div>
                    </div>
                    <ProgressBar pct={pct} color={col} over={over} />
                    <div style={{ display: "flex", justifyContent: "space-between", marginTop: 7, alignItems: "center" }}>
                      <span style={{ fontSize: "0.69rem", color: "#2d5070" }}>{pct}% of budget used</span>
                      <Badge
                        text={over ? "Over budget" : "On track"}
                        color={over ? "#fb7185" : "#34d399"}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </Panel>

        {/* ── Bar Chart ── */}
        {!loading && budget.length > 0 && (
          <Panel title="Spent vs Recommended Budget" emoji="📊">
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={budget} margin={{ top: 5, right: 10, left: -12, bottom: 5 }} barGap={5}>
                <CartesianGrid strokeDasharray="3 3" stroke="#0d1b2a" />
                <XAxis dataKey="category" tick={{ fill: "#2d5070", fontSize: 11 }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fill: "#2d5070", fontSize: 11 }} axisLine={false} tickLine={false} tickFormatter={v => "₹" + v} />
                <Tooltip content={<ChartTip />} />
                <Bar dataKey="spent"              name="Spent"    fill="#7c6af7" radius={[5,5,0,0]} maxBarSize={32} />
                <Bar dataKey="recommended_budget" name="Budget"   fill="#1e3a52" radius={[5,5,0,0]} maxBarSize={32} />
                <Legend wrapperStyle={{ fontSize: "0.74rem", color: "#456780" }} />
              </BarChart>
            </ResponsiveContainer>
          </Panel>
        )}

        {/* ── RAG Q&A ── */}
        <Panel title="Ask Your Finance AI" emoji="💬">
          <p style={{ color: "#2d5070", fontSize: "0.78rem", marginBottom: 14 }}>
            RAG-powered — answers grounded in your actual transaction data.
          </p>
          <div style={{ display: "flex", gap: 11, flexWrap: "wrap" }}>
            <input
              type="text"
              placeholder='"How much did I spend on food?" or "Where can I save money?"'
              value={question}
              onChange={e => setQuestion(e.target.value)}
              onKeyDown={e => e.key === "Enter" && askQuestion()}
              style={{ ...inp, flex: "1 1 280px" }}
            />
            <button style={btnAsk} onClick={askQuestion} disabled={asking || !question.trim()}>
              {asking ? "Thinking…" : "Ask AI"}
            </button>
          </div>

          <div style={{ display: "flex", flexWrap: "wrap", gap: 7, marginTop: 12 }}>
            {["What's my biggest expense?", "Where can I save money?", "How's my spending this month?"].map(q => (
              <button key={q} className="chip-btn" onClick={() => setQuestion(q)} style={{
                background: "#0d1b2a", border: "1px solid #1e3a52",
                borderRadius: 999, color: "#456780",
                padding: "5px 12px", fontSize: "0.74rem",
                cursor: "pointer", fontFamily: "inherit",
                fontWeight: 600, transition: "all .2s",
              }}>{q}</button>
            ))}
          </div>

          {asking && (
            <div style={{ display: "flex", gap: 5, alignItems: "center", marginTop: 16 }}>
              {[0,1,2].map(i => (
                <div key={i} style={{
                  width: 6, height: 6, borderRadius: "50%", background: "#7c6af7",
                  animation: "blink 1.4s ease infinite",
                  animationDelay: `${i * 0.22}s`,
                }} />
              ))}
              <span style={{ color: "#2d5070", fontSize: "0.8rem", marginLeft: 6 }}>Thinking…</span>
            </div>
          )}

          {answer && !asking && (
            <div style={{
              marginTop: 15, background: "#0d1b2a",
              borderRadius: 12, padding: "15px 18px",
              borderLeft: "3px solid #7c6af7",
            }}>
              <p style={{ color: "#5a8ca8", lineHeight: 1.8, fontSize: "0.87rem" }}>{answer}</p>
            </div>
          )}
        </Panel>

        {/* ── Transaction History ── */}
        <Panel
          title="Transaction History"
          emoji="🧾"
          right={<span style={{ color: "#2d5070", fontSize: "0.75rem", fontWeight: 600 }}>{transactions.length} records</span>}
        >
          {loading ? (
            [1,2,3].map(i => <Skel key={i} mb={10} />)
          ) : transactions.length === 0 ? (
            <p style={{ color: "#2d5070", fontSize: "0.84rem" }}>No transactions yet.</p>
          ) : (
            <>
              <div style={{
                display: "grid",
                gridTemplateColumns: "1fr auto auto auto",
                gap: 14, padding: "0 8px 10px",
                color: "#1e3a52", fontSize: "0.67rem",
                fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.1em",
              }}>
                <span>Description</span>
                <span>Category</span>
                <span>Amount</span>
                <span>Date</span>
              </div>

              {transactions.map((t, i) => (
                <div key={t.id ?? i} className="tx-row" style={{
                  display: "grid",
                  gridTemplateColumns: "1fr auto auto auto",
                  gap: 14, padding: "9px 8px",
                  alignItems: "center",
                  borderTop: i > 0 ? "1px solid #0a1420" : "none",
                  transition: "background .15s",
                }}>
                  <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                    <span style={{ fontSize: 16, lineHeight: 1 }}>{catEmoji(t.category)}</span>
                    <span style={{ color: "#5a8ca8", fontSize: "0.84rem" }}>{t.description}</span>
                  </div>
                  <Badge text={t.category || "Other"} color="#7c6af7" />
                  <span style={{ fontFamily: "'DM Mono', monospace", color: "#22d3ee", fontWeight: 700, fontSize: "0.87rem" }}>
                    {INR(t.amount)}
                  </span>
                  <span style={{ color: "#2d5070", fontSize: "0.74rem" }}>{fmtDate(t.created_at)}</span>
                </div>
              ))}
            </>
          )}
        </Panel>

        <div style={{ textAlign: "center", padding: "16px 0 4px", color: "#162030", fontSize: "0.7rem" }}>
          FinanceAI · FastAPI · PostgreSQL · ChromaDB · Ollama / Mistral · scikit-learn
        </div>
      </div>
    </>
  );
}
