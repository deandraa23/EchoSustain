import streamlit as st
import requests
import pandas as pd
import json
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# ============================================================
# EchoSustain — Clean ESG Intelligence Frontend
# ============================================================

st.set_page_config(
    page_title="EchoSustain | ESG Intelligence",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

BACKEND_URL = "http://127.0.0.1:8001"

# ============================================================
# DESIGN SYSTEM (High-Trust Light Enterprise Theme)
# ============================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

/* Completely eliminate Streamlit top bar, deploy button, and 3 dots menu */
#MainMenu, header, [data-testid="stHeader"], .stDeployButton, footer {
    visibility: hidden !important;
    display: none !important;
    height: 0px !important;
    padding: 0px !important;
    margin: 0px !important;
}

:root {
    --bg: #f2f5f3;
    --surface: #ffffff;
    --surface-soft: #f7faf8;
    --border: #cbd6ce;
    --border-strong: #aebdb3;
    --text: #122018;
    --text-soft: #33433a;
    --muted: #526158;
    --green: #116b40;
    --green-dark: #084c2c;
    --green-soft: #e2f3e9;
    --amber: #9a6208;
    --amber-soft: #fff3d6;
    --red: #b4232c;
    --red-soft: #ffe8ea;
    --blue: #245f9e;
    --blue-soft: #e8f1fb;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: var(--bg);
    color: var(--text);
}

.block-container {
    max-width: 1540px;
    padding-top: 1.5rem !important;
    padding-bottom: 4rem;
}

[data-testid="stSidebar"] {
    background: #fbfdfb !important;
    border-right: 1.5px solid var(--border) !important;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.2rem;
}

h1, h2, h3 {
    font-family: 'Manrope', sans-serif !important;
    color: var(--text) !important;
    letter-spacing: -0.025em;
}

h1 { font-size: 2.25rem !important; font-weight: 800 !important; }
h2 { font-size: 1.45rem !important; font-weight: 800 !important; }
h3 { font-size: 1.05rem !important; font-weight: 700 !important; }

p, label, .stMarkdown {
    color: var(--text);
}

.brand {
    padding: 4px 4px 18px 4px;
}

.brand-row {
    display: flex;
    align-items: center;
    gap: 11px;
}

.brand-icon {
    width: 40px;
    height: 40px;
    border-radius: 11px;
    background: var(--green-soft);
    border: 1px solid #cde9d8;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
}

.brand-name {
    font-family: 'Manrope', sans-serif;
    font-weight: 800;
    font-size: 1.18rem;
    color: var(--text);
}

.brand-sub {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.09em;
    color: var(--green);
    margin-top: 2px;
}

.nav-label {
    color: #526158;
    font-size: 0.72rem;
    text-transform: uppercase;
    font-weight: 800;
    letter-spacing: 0.08em;
    margin: 15px 0 8px 3px;
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 20px;
    margin-bottom: 22px;
}

.header-title {
    font-family: 'Manrope', sans-serif;
    font-size: 2.1rem;
    font-weight: 800;
    color: var(--text);
    line-height: 1.15;
}

.header-subtitle {
    margin-top: 6px;
    color: var(--muted);
    font-size: 0.94rem;
}

.status {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 8px 14px;
    background: var(--green-soft);
    border: 1px solid #a9d1b8;
    border-radius: 999px;
    color: var(--green-dark);
    font-size: 0.78rem;
    font-weight: 700;
    white-space: nowrap;
}

.status-dot {
    width: 8px;
    height: 8px;
    background: #116b40;
    border-radius: 50%;
}

.card {
    background: var(--surface);
    border: 1px solid var(--border-strong);
    border-radius: 16px;
    padding: 22px;
    box-shadow: 0 4px 16px rgba(18, 32, 24, 0.04);
}

.card-title {
    font-family: 'Manrope', sans-serif;
    font-weight: 800;
    font-size: 1.02rem;
    color: var(--text);
}

.card-subtitle {
    color: var(--muted);
    font-size: 0.82rem;
    margin-top: 3px;
}

.metric-card {
    background: var(--surface);
    border: 1px solid var(--border-strong);
    border-radius: 16px;
    padding: 20px 22px;
    min-height: 130px;
    box-shadow: 0 4px 16px rgba(18, 32, 24, 0.04);
}

.metric-label {
    color: var(--muted);
    font-size: 0.78rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.07em;
}

.metric-number {
    color: var(--text);
    font-family: 'Manrope', sans-serif;
    font-size: 2.2rem;
    line-height: 1.05;
    font-weight: 800;
    margin-top: 8px;
}

.metric-note {
    color: var(--muted);
    font-size: 0.8rem;
    margin-top: 4px;
}

.green-number { color: var(--green); }
.red-number { color: var(--red); }
.amber-number { color: var(--amber); }

.section-gap { height: 20px; }

.audit-row {
    background: #fff;
    border: 1px solid var(--border-strong);
    border-radius: 14px;
    padding: 16px 18px;
    margin-bottom: 10px;
    box-shadow: 0 2px 8px rgba(18, 32, 24, 0.03);
}

.score-pill {
    display: inline-block;
    padding: 5px 11px;
    border-radius: 999px;
    font-size: 0.76rem;
    font-weight: 800;
    border: 1px solid currentColor;
}

.score-good { color: var(--green-dark); background: var(--green-soft); }
.score-mid { color: #8b5e13; background: var(--amber-soft); }
.score-low { color: #a52f2f; background: var(--red-soft); }

.risk-badge {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.03em;
    border: 1px solid currentColor;
}

.risk-greenwashing { color: #a52f2f; background: var(--red-soft); }
.risk-unverified { color: #8b5e13; background: var(--amber-soft); }
.risk-verified { color: var(--green-dark); background: var(--green-soft); }

.claim-card {
    background: #fff;
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px 22px;
    margin-bottom: 14px;
    box-shadow: 0 2px 8px rgba(18, 32, 24, 0.03);
}

.claim-card-danger { border-left: 5px solid var(--red); }
.claim-card-warning { border-left: 5px solid #d69a28; }
.claim-card-success { border-left: 5px solid #2d9961; }

.claim-text {
    font-size: 1.02rem;
    font-weight: 700;
    color: var(--text);
    line-height: 1.5;
    margin: 10px 0 12px;
}

.reasoning {
    background: #f8faf9;
    border: 1px solid #e1e9e3;
    border-radius: 10px;
    padding: 12px 16px;
    color: #405247;
    font-size: 0.88rem;
    line-height: 1.6;
}

.info-strip {
    background: var(--green-soft);
    border: 1px solid #d1eadb;
    border-radius: 12px;
    padding: 14px 18px;
    color: var(--green-dark);
    font-size: 0.88rem;
}

.context-box {
    background: #f1f7f3;
    border: 1px solid #cde5d4;
    border-radius: 12px;
    padding: 14px 18px;
}

/* Fix dark background in select boxes */
[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    border: 1px solid var(--border-strong) !important;
    border-radius: 10px !important;
    color: #122018 !important;
}

[data-baseweb="select"] * {
    color: #122018 !important;
    background-color: transparent !important;
}

/* Inputs & Buttons */
.stTextInput input, [data-testid="stFileUploaderDropzone"] {
    background: #ffffff !important;
    border: 1px solid var(--border-strong) !important;
    border-radius: 10px !important;
    color: #122018 !important;
}

.stButton > button, .stDownloadButton > button {
    border-radius: 10px !important;
    font-weight: 750 !important;
    border: 1px solid var(--border-strong) !important;
    background: #ffffff !important;
    color: #173025 !important;
}

button[kind="primary"] {
    background: var(--green) !important;
    border-color: var(--green) !important;
    color: #ffffff !important;
}
button[kind="primary"]:hover {
    background: var(--green-dark) !important;
    border-color: var(--green-dark) !important;
}

div[data-testid="stPlotlyChart"] {
    background: #ffffff;
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 8px 12px 2px 12px;
    box-shadow: 0 3px 12px rgba(18, 32, 24, 0.035);
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# HELPERS
# ============================================================

def sync_registry():
    try:
        response = requests.get(f"{BACKEND_URL}/audits", timeout=3)
        if response.status_code == 200:
            return response.json().get("audits", [])
    except Exception:
        pass
    return []

def score_class(score):
    if score >= 70:
        return "score-good"
    if score >= 45:
        return "score-mid"
    return "score-low"

def score_label(score):
    if score >= 70:
        return "Good"
    if score >= 45:
        return "Needs Review"
    return "High Risk"

def risk_badge(verdict):
    verdict = (verdict or "").lower()
    if verdict == "greenwashing":
        return '<span class="risk-badge risk-greenwashing">HIGH RISK · GREENWASHING</span>'
    if verdict == "unverified":
        return '<span class="risk-badge risk-unverified">REVIEW · UNVERIFIED</span>'
    return '<span class="risk-badge risk-verified">VERIFIED</span>'

def chart_layout(fig, height=300):
    fig.update_layout(
        height=height,
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font=dict(family="DM Sans", color="#24372c", size=13),
        margin=dict(l=18, r=24, t=28, b=18),
        showlegend=True,
        legend=dict(font=dict(size=12, color="#24372c"), bgcolor="rgba(255,255,255,0.9)"),
    )
    fig.update_xaxes(tickfont=dict(color="#526158", size=12), gridcolor="#dfe6e1")
    fig.update_yaxes(tickfont=dict(color="#526158", size=12), gridcolor="#dfe6e1")
    return fig

def selected_audit():
    audit_id = st.session_state.get("selected_audit_id")
    if not audit_id:
        return None
    return next((a for a in st.session_state.audits if a.get("audit_id") == audit_id), None)

# ============================================================
# SESSION STATE
# ============================================================

if "audits" not in st.session_state:
    st.session_state.audits = sync_registry()

if "selected_audit_id" not in st.session_state:
    st.session_state.selected_audit_id = (
        st.session_state.audits[0]["audit_id"] if st.session_state.audits else None
    )

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("""
    <div class="brand">
        <div class="brand-row">
            <div class="brand-icon">🌱</div>
            <div>
                <div class="brand-name">EchoSustain</div>
                <div class="brand-sub">ESG INTELLIGENCE</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="nav-label">Workspace</div>', unsafe_allow_html=True)

    menu = st.radio(
        "Navigation",
        ["Overview", "Audits", "Upload & Analyze", "Claims", "AI Copilot"],
        label_visibility="collapsed",
    )

    st.divider()

    st.markdown('<div class="nav-label">Active audit</div>', unsafe_allow_html=True)

    if st.session_state.audits:
        options = {a["audit_id"]: a["filename"] for a in st.session_state.audits}
        curr_idx = (
            list(options.keys()).index(st.session_state.selected_audit_id)
            if st.session_state.selected_audit_id in options
            else 0
        )

        selected = st.selectbox(
            "Select audit",
            list(options.keys()),
            index=curr_idx,
            format_func=lambda x: options[x],
            label_visibility="collapsed",
        )
        st.session_state.selected_audit_id = selected

        current = selected_audit()
        if current:
            score = current.get("audit_results", {}).get("transparency_score", 0)
            st.markdown(
                f"""
                <div style="margin-top:10px;">
                    <span class="score-pill {score_class(score)}">
                        {score}/100 · {score_label(score)}
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.caption("No audits in the registry.")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    if st.button("↻ Refresh audits", use_container_width=True):
        st.session_state.audits = sync_registry()
        st.rerun()

    st.divider()

    st.markdown(
        """
        <div style="font-size:0.75rem;color:#526158;line-height:1.6;">
        <b>Architecture</b><br>
        FastAPI · Gemini 3.6 Flash · AWS S3 · SQLite<br><br>
        Audit context retrieved dynamically per document.
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# GLOBAL TELEMETRY
# ============================================================

total_docs = len(st.session_state.audits)
all_claims = [
    c for a in st.session_state.audits for c in a.get("audit_results", {}).get("claims_analyzed", [])
]
total_claims = len(all_claims)
greenwashing_count = sum(1 for c in all_claims if c.get("verdict") == "greenwashing")
unverified_count = sum(1 for c in all_claims if c.get("verdict") == "unverified")
verified_count = sum(1 for c in all_claims if c.get("verdict") == "verified")
avg_transparency = (
    round(sum(a.get("audit_results", {}).get("transparency_score", 0) for a in st.session_state.audits) / total_docs, 1)
    if total_docs else 0
)

# Header
st.markdown("""
<div class="header">
    <div>
        <div style="font-size:.74rem;font-weight:800;letter-spacing:.12em;color:#116b40;text-transform:uppercase;margin-bottom:6px;">
            EchoSustain · ESG Risk Workspace
        </div>
        <div class="header-title">ESG Compliance Intelligence</div>
        <div class="header-subtitle">
            Detect unsupported sustainability claims, assess disclosure quality, and investigate audit findings.
        </div>
    </div>
    <div class="status">
        <span class="status-dot"></span>
        Audit engine operational
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# 1. OVERVIEW
# ============================================================

if menu == "Overview":
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Reports Audited</div><div class="metric-number">{total_docs}</div><div class="metric-note">Stored audit records</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Claims Evaluated</div><div class="metric-number">{total_claims}</div><div class="metric-note">Across all reports</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Greenwashing Flags</div><div class="metric-number red-number">{greenwashing_count}</div><div class="metric-note">Claims requiring attention</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Avg. Transparency</div><div class="metric-number green-number">{avg_transparency}%</div><div class="metric-note">Portfolio-level index</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)

    left, right = st.columns([1.05, 1.45])
    with left:
        st.markdown('<div class="card"><div class="card-title">Claim disposition</div><div class="card-subtitle">Distribution of AI-evaluated sustainability claims</div></div>', unsafe_allow_html=True)
        fig = go.Figure(data=[go.Pie(
            labels=["Verified", "Unverified", "Greenwashing"],
            values=[verified_count, unverified_count, greenwashing_count],
            hole=0.68,
            textinfo="percent",
            textfont=dict(size=13, color="#122018"),
            marker=dict(colors=["#2d9961", "#d69a28", "#c53b3b"], line=dict(color="#ffffff", width=2))
        )])
        fig.update_layout(showlegend=True, legend=dict(orientation="h", y=-0.08), height=300, paper_bgcolor="#ffffff", margin=dict(l=8, r=8, t=15, b=20))
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.markdown('<div class="card"><div class="card-title">Audit performance</div><div class="card-subtitle">Transparency score by analyzed report</div></div>', unsafe_allow_html=True)
        if st.session_state.audits:
            chart_df = pd.DataFrame([{
                "Report": a["filename"][:28],
                "Transparency": a.get("audit_results", {}).get("transparency_score", 0)
            } for a in reversed(st.session_state.audits)])
            bar_fig = px.bar(chart_df, x="Transparency", y="Report", orientation="h", range_x=[0, 100], text="Transparency")
            bar_fig.update_traces(marker_color="#116b40", textposition="outside", textfont=dict(size=12, color="#122018"))
            st.plotly_chart(chart_layout(bar_fig, 300), use_container_width=True)
        else:
            st.info("Upload reports to view benchmark analytics.")

# ============================================================
# 2. AUDITS REGISTRY
# ============================================================

elif menu == "Audits":
    st.markdown("## Audit Registry")
    st.caption("Browse and search every sustainability report archived in EchoSustain.")

    if not st.session_state.audits:
        st.info("No reports have been audited yet. Navigate to Upload & Analyze to start.")
    else:
        search = st.text_input("Search reports", placeholder="Search by filename...", label_visibility="collapsed")
        filtered = [a for a in st.session_state.audits if search.lower() in a.get("filename", "").lower()] if search else st.session_state.audits

        for audit in filtered:
            res = audit.get("audit_results", {})
            sc = res.get("transparency_score", 0)
            claims = res.get("claims_analyzed", [])
            gw = sum(1 for c in claims if c.get("verdict") == "greenwashing")
            uv = sum(1 for c in claims if c.get("verdict") == "unverified")

            with st.container():
                col1, col2, col3, col4 = st.columns([3, 1, 1.3, 1])
                with col1:
                    st.markdown(f'<div class="audit-row"><div style="font-weight:700;">{audit["filename"]}</div><div style="font-size:.8rem;color:#526158;margin-top:3px;">{audit.get("timestamp","")} · {len(claims)} claims</div></div>', unsafe_allow_html=True)
                with col2:
                    st.markdown(f'<div style="padding-top:14px;"><span class="score-pill {score_class(sc)}">{sc}/100</span></div>', unsafe_allow_html=True)
                with col3:
                    st.markdown(f'<div style="padding-top:14px;font-size:.82rem;color:#526158;"><span style="color:#b4232c;font-weight:700;">{gw}</span> high risk · <span style="color:#9a6208;font-weight:700;">{uv}</span> unverified</div>', unsafe_allow_html=True)
                with col4:
                    if st.button("Open audit", key=f"btn_{audit['audit_id']}", use_container_width=True):
                        st.session_state.selected_audit_id = audit["audit_id"]
                        st.rerun()

# ============================================================
# 3. UPLOAD & ANALYZE
# ============================================================

elif menu == "Upload & Analyze":
    st.markdown("## Upload & Analyze")
    st.caption("Upload a corporate sustainability report and trigger the compliance pipeline.")

    st.markdown("""
    <div class="info-strip">
        <b>Audit Flow:</b> The PDF binary is uploaded and stored under <code>s3://echosustain-reports</code>, extracted in-memory, evaluated using zero-temperature Gemini inference, and indexed in SQLite.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)

    uploaded = st.file_uploader("Select PDF Report", type=["pdf"], label_visibility="collapsed")
    if uploaded:
        size_kb = uploaded.size / 1024
        st.markdown(f'<div class="card"><div class="card-title">{uploaded.name}</div><div class="card-subtitle">PDF · {size_kb:.1f} KB · Verified & Ready</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)

        if st.button("🌱 Run ESG Audit", type="primary", use_container_width=True):
            with st.status("Executing Multi-Stage Audit...", expanded=True) as status:
                st.write("1. Archiving binary to Amazon S3...")
                payload = {"file": (uploaded.name, uploaded.getvalue(), "application/pdf")}
                try:
                    st.write("2. Extracting textual tokens & PDF AST...")
                    st.write("3. Dispatching to Gemini 3.6 Flash...")
                    res = requests.post(f"{BACKEND_URL}/upload", files=payload, timeout=120)
                    if res.status_code == 200:
                        data = res.json()
                        st.session_state.audits = sync_registry()
                        st.session_state.selected_audit_id = data.get("audit_id")
                        status.update(label="Audit Succeeded & Persisted!", state="complete", expanded=False)
                        st.success(f"Audit completed for **{uploaded.name}**!")
                    else:
                        status.update(label="Audit Failed", state="error")
                        st.error(res.text)
                except Exception as e:
                    status.update(label="Connection Error", state="error")
                    st.error(f"Backend offline: {e}")

# ============================================================
# 4. CLAIMS INVESTIGATION
# ============================================================

elif menu == "Claims":
    current = selected_audit()
    if not current:
        st.info("Select an audit from the sidebar or upload a new filing to begin.")
    else:
        results = current.get("audit_results", {})
        claims = results.get("claims_analyzed", [])
        score = results.get("transparency_score", 0)

        st.markdown("## Claim Investigation")
        st.caption(f"Detailed disclosure findings for **{current.get('filename')}**")

        top1, top2, top3, top4 = st.columns(4)
        with top1:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Transparency</div><div class="metric-number green-number">{score}</div><div class="metric-note">out of 100</div></div>', unsafe_allow_html=True)
        with top2:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Total Claims</div><div class="metric-number">{len(claims)}</div><div class="metric-note">evaluated statements</div></div>', unsafe_allow_html=True)
        with top3:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Greenwashing</div><div class="metric-number red-number">{sum(1 for c in claims if c.get("verdict") == "greenwashing")}</div><div class="metric-note">high-risk violations</div></div>', unsafe_allow_html=True)
        with top4:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Unverified</div><div class="metric-number amber-number">{sum(1 for c in claims if c.get("verdict") == "unverified")}</div><div class="metric-note">needs evidence</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)

        left, right = st.columns([2.5, 1])
        with left:
            st.markdown('<div class="card"><div class="card-title">Auditor Executive Synthesis</div>', unsafe_allow_html=True)
            st.write(results.get("summary", "No assessment provided."))
            st.caption(f"Archived URI: `{current.get('s3_path')}`")
            st.markdown('</div>', unsafe_allow_html=True)

        with right:
            st.markdown('<div class="card"><div class="card-title">Exports</div><div class="card-subtitle">Download verified audit data</div>', unsafe_allow_html=True)
            if claims:
                csv_bytes = pd.DataFrame(claims).to_csv(index=False).encode("utf-8")
                st.download_button("📥 Download CSV", csv_bytes, file_name=f"audit_{current['audit_id'][:8]}.csv", mime="text/csv", use_container_width=True)
                json_bytes = json.dumps(current, indent=2).encode("utf-8")
                st.download_button("📥 Download JSON", json_bytes, file_name=f"audit_{current['audit_id'][:8]}.json", mime="application/json", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)

        f_choice = st.selectbox(
            "Filter Findings",
            ["All claims", "Greenwashing only", "Unverified only", "Verified only"]
        )

        filtered_claims = claims
        if f_choice == "Greenwashing only":
            filtered_claims = [c for c in claims if c.get("verdict") == "greenwashing"]
        elif f_choice == "Unverified only":
            filtered_claims = [c for c in claims if c.get("verdict") == "unverified"]
        elif f_choice == "Verified only":
            filtered_claims = [c for c in claims if c.get("verdict") == "verified"]

        st.markdown(f"### Findings ({len(filtered_claims)})")

        for idx, claim in enumerate(filtered_claims, 1):
            v = claim.get("verdict", "").lower()
            css = "claim-card-danger" if v == "greenwashing" else "claim-card-warning" if v == "unverified" else "claim-card-success"
            st.markdown(f"""
            <div class="claim-card {css}">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-size:0.75rem; color:#526158; font-weight:800;">CLAIM #{idx:02d}</span>
                    {risk_badge(v)}
                </div>
                <div class="claim-text">"{claim.get('claim')}"</div>
                <div class="reasoning">
                    <b>Auditor Assessment:</b> {claim.get('reasoning')}
                </div>
            </div>
            """, unsafe_allow_html=True)

# ============================================================
# 5. AI COPILOT
# ============================================================

elif menu == "AI Copilot":
    current = selected_audit()
    if not current:
        st.info("Select an audit from the sidebar to initialize the Copilot.")
    else:
        results = current.get("audit_results", {})
        score = results.get("transparency_score", 0)
        claims = results.get("claims_analyzed", [])

        st.markdown(f"""
        <div class="context-box">
            <div style="font-weight:800; color:#122018;">Context locked to {current.get("filename")}</div>
            <div style="font-size:0.8rem; color:#526158; margin-top:3px;">
                Transparency {score}/100 · {len(claims)} claims · {sum(1 for c in claims if c.get("verdict") == "greenwashing")} high-risk findings
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)

        # Quick query buttons
        q_cols = st.columns(2)
        suggestions = [
            "Why were the highest-risk claims flagged?",
            "Summarize the main ESG risks in this report.",
            "Which claims are unverified?",
            "What evidence would strengthen the flagged claims?"
        ]
        for i, s in enumerate(suggestions):
            with q_cols[i % 2]:
                if st.button(s, key=f"sug_{i}", use_container_width=True):
                    st.session_state.pending_question = s

        for role, msg in st.session_state.chat_history:
            with st.chat_message(role):
                st.write(msg)

        q = st.chat_input("Ask about this audit...")
        if "pending_question" in st.session_state:
            q = st.session_state.pop("pending_question")

        if q:
            st.session_state.chat_history.append(("user", q))
            with st.chat_message("user"):
                st.write(q)

            with st.chat_message("assistant"):
                with st.spinner("Reviewing audit context..."):
                    try:
                        res = requests.post(
                            f"{BACKEND_URL}/chat",
                            json={"audit_id": current["audit_id"], "question": q},
                            timeout=90
                        )
                        if res.status_code == 200:
                            ans = res.json().get("answer", "No answer returned.")
                            st.write(ans)
                            st.session_state.chat_history.append(("assistant", ans))
                        else:
                            st.error(res.text)
                    except Exception as e:
                        st.error(f"Cannot reach backend: {e}")