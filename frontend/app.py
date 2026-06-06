from __future__ import annotations

import os
from typing import Any

import pandas as pd
import requests
import streamlit as st

API_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Sales Memory Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap');

    :root {
        --bg:          #f8f9fc;
        --white:       #ffffff;
        --surface:     #f1f3f8;
        --border:      #e2e6ef;
        --border-light:#edf0f7;
        --accent:      #2563eb;
        --accent-light:#eff4ff;
        --accent-dark: #1d4ed8;
        --green:       #16a34a;
        --green-light: #f0fdf4;
        --amber:       #d97706;
        --amber-light: #fffbeb;
        --red:         #dc2626;
        --red-light:   #fef2f2;
        --text:        #111827;
        --text-muted:  #6b7280;
        --text-light:  #9ca3af;
        --shadow-sm:   0 1px 3px rgba(0,0,0,.07), 0 1px 2px rgba(0,0,0,.05);
        --shadow:      0 4px 12px rgba(0,0,0,.08), 0 1px 3px rgba(0,0,0,.05);
        --shadow-md:   0 8px 24px rgba(0,0,0,.10), 0 2px 6px rgba(0,0,0,.05);
        --radius:      10px;
        --radius-sm:   7px;
        --radius-lg:   14px;
    }

    /* ── Base ── */
    html, body, .stApp {
        background: var(--bg) !important;
        font-family: 'Inter', sans-serif !important;
        color: var(--text) !important;
        font-size: 15px !important;
    }
    #MainMenu, footer, header { visibility: hidden; }
    .block-container {
        padding: 2rem 2.5rem 4rem !important;
        max-width: 1300px;
    }

    /* ── Global text — force dark on white bg everywhere ── */
    p, li, span, div, td, th, label {
        color: var(--text) !important;
    }

    /* ── Sidebar shell ── */
    section[data-testid="stSidebar"] {
        background: #ffffff !important;
        border-right: 1px solid var(--border) !important;
    }
    section[data-testid="stSidebar"] * {
        font-family: 'Inter', sans-serif !important;
    }
    section[data-testid="stSidebar"] .stRadio {
        display: none !important;
    }

    /* ── Sidebar nav buttons — all ── */
    section[data-testid="stSidebar"] .stButton > button {
        display: flex !important;
        align-items: center !important;
        gap: 10px !important;
        width: 100% !important;
        text-align: left !important;
        padding: 9px 12px !important;
        border-radius: 8px !important;
        font-size: .9rem !important;
        font-weight: 500 !important;
        background: transparent !important;
        color: #4b5563 !important;
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
        transition: background .15s, color .15s !important;
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: #f3f4f6 !important;
        color: #111827 !important;
        border: none !important;
        box-shadow: none !important;
        transform: none !important;
    }
    section[data-testid="stSidebar"] .stButton > button:focus,
    section[data-testid="stSidebar"] .stButton > button:focus-visible,
    section[data-testid="stSidebar"] .stButton > button:active {
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
        transform: none !important;
    }
    section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background: #eff6ff !important;
        color: #1d4ed8 !important;
        font-weight: 600 !important;
        border: none !important;
        box-shadow: none !important;
    }
    section[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover,
    section[data-testid="stSidebar"] .stButton > button[kind="primary"]:focus,
    section[data-testid="stSidebar"] .stButton > button[kind="primary"]:focus-visible {
        background: #dbeafe !important;
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
        transform: none !important;
    }
    section[data-testid="stSidebar"] .stButton > button[kind="secondary"] {
        background: transparent !important;
        color: #6b7280 !important;
        border: none !important;
        font-size: .82rem !important;
        padding: 7px 12px !important;
    }
    section[data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover {
        background: #f3f4f6 !important;
        color: #374151 !important;
        border: none !important;
        box-shadow: none !important;
        transform: none !important;
    }

    /* ── Headings ── */
    h1, h2, h3, h4 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: var(--text) !important;
        letter-spacing: -.3px !important;
    }
    h1 { font-size: 1.75rem !important; font-weight: 700 !important; }
    h2 { font-size: 1.25rem !important; font-weight: 700 !important; }
    h3 { font-size: 1.05rem !important; font-weight: 600 !important; }

    /* ── Section heading (replaces tiny uppercase label) ── */
    .section-label {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 1rem;
        font-weight: 700;
        color: #111827;
        border-bottom: 2px solid var(--border);
        padding-bottom: .5rem;
        margin: 1.8rem 0 1rem;
        letter-spacing: -.1px;
    }

    /* ── Metric cards ── */
    [data-testid="stMetric"] {
        background: var(--white) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-lg) !important;
        padding: 1.25rem 1.5rem !important;
        box-shadow: var(--shadow-sm) !important;
        transition: box-shadow .2s !important;
    }
    [data-testid="stMetric"]:hover { box-shadow: var(--shadow-md) !important; }
    [data-testid="stMetricLabel"] {
        color: var(--text-muted) !important;
        font-size: .78rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: .08em !important;
    }
    [data-testid="stMetricValue"] {
        color: var(--accent) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 2rem !important;
        font-weight: 800 !important;
    }

    /* ── Main buttons ── */
    .stButton > button {
        background: var(--accent) !important;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
        font-size: .9rem !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: var(--radius-sm) !important;
        padding: .55rem 1.4rem !important;
        box-shadow: 0 1px 3px rgba(37,99,235,.25) !important;
        transition: background .15s, box-shadow .15s, transform .1s !important;
        cursor: pointer !important;
    }
    .stButton > button:hover {
        background: var(--accent-dark) !important;
        box-shadow: 0 4px 12px rgba(37,99,235,.3) !important;
        transform: translateY(-1px) !important;
    }
    .stButton > button:active { transform: translateY(0) !important; }

    /* ── Form fields ── */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: var(--white) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
        color: #111827 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: .9rem !important;
        box-shadow: var(--shadow-sm) !important;
        transition: border-color .15s, box-shadow .15s !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px rgba(37,99,235,.12) !important;
        outline: none !important;
    }
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: #9ca3af !important;
    }

    /* ── Selectbox trigger ── */
    .stSelectbox > div > div {
        background: var(--white) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
        color: #111827 !important;
        font-size: .9rem !important;
        box-shadow: var(--shadow-sm) !important;
    }
    /* Selected value text */
    .stSelectbox [data-baseweb="select"] div,
    .stSelectbox [data-baseweb="select"] span,
    .stSelectbox [data-baseweb="select"] input {
        color: #111827 !important;
        background: transparent !important;
    }
    /* Arrow icon — black */
    .stSelectbox svg {
        fill: #111827 !important;
        color: #111827 !important;
        stroke: #111827 !important;
    }
    /* Dropdown popup */
    [data-baseweb="popover"] > div,
    [data-baseweb="menu"],
    ul[role="listbox"] {
        background: #ffffff !important;
        border: 1px solid #d1d5db !important;
        border-radius: var(--radius-sm) !important;
        box-shadow: var(--shadow-md) !important;
    }
    /* Option rows */
    [role="option"],
    li[role="option"],
    [data-baseweb="menu"] li {
        background: #ffffff !important;
        color: #111827 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: .9rem !important;
        padding: 9px 14px !important;
    }
    [role="option"]:hover,
    li[role="option"]:hover,
    [data-baseweb="menu"] li:hover {
        background: #eff6ff !important;
        color: #1d4ed8 !important;
    }
    [aria-selected="true"],
    [role="option"][aria-selected="true"] {
        background: #eff6ff !important;
        color: #1d4ed8 !important;
        font-weight: 600 !important;
    }

    /* ── Labels ── */
    label, .stSelectbox label, .stTextInput label, .stTextArea label {
        color: #374151 !important;
        font-size: .85rem !important;
        font-weight: 600 !important;
        letter-spacing: .01em !important;
    }

    /* ── Expanders ── */
    .streamlit-expanderHeader {
        background: #ffffff !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
        color: #111827 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: .9rem !important;
        font-weight: 600 !important;
        padding: .75rem 1rem !important;
        box-shadow: var(--shadow-sm) !important;
    }
    .streamlit-expanderHeader:hover {
        background: #f9fafb !important;
    }
    /* expander header text and svg always dark */
    .streamlit-expanderHeader p,
    .streamlit-expanderHeader span,
    .streamlit-expanderHeader div {
        color: #111827 !important;
    }
    .streamlit-expanderHeader svg {
        fill: #111827 !important;
        stroke: #111827 !important;
        color: #111827 !important;
    }
    .streamlit-expanderContent {
        background: #ffffff !important;
        border: 1px solid var(--border) !important;
        border-top: none !important;
        border-radius: 0 0 var(--radius-sm) var(--radius-sm) !important;
        padding: 1.1rem !important;
    }
    /* ALL text inside expander content — force dark */
    .streamlit-expanderContent *,
    .streamlit-expanderContent p,
    .streamlit-expanderContent span,
    .streamlit-expanderContent div,
    .streamlit-expanderContent li,
    .streamlit-expanderContent td,
    .streamlit-expanderContent th,
    .streamlit-expanderContent strong,
    .streamlit-expanderContent label {
        color: #111827 !important;
    }

    /* ── Alerts ── */
    .stSuccess { background: var(--green-light) !important; border: 1px solid #bbf7d0 !important; border-radius: var(--radius-sm) !important; color: #166534 !important; }
    .stSuccess * { color: #166534 !important; }
    .stWarning { background: var(--amber-light) !important; border: 1px solid #fde68a !important; border-radius: var(--radius-sm) !important; color: #92400e !important; }
    .stWarning * { color: #92400e !important; }
    .stError   { background: var(--red-light) !important; border: 1px solid #fecaca !important; border-radius: var(--radius-sm) !important; color: #991b1b !important; }
    .stError   * { color: #991b1b !important; }
    .stInfo    { background: var(--accent-light) !important; border: 1px solid #bfdbfe !important; border-radius: var(--radius-sm) !important; color: #1e40af !important; }
    .stInfo    * { color: #1e40af !important; }

    /* ── Dataframe — full white bg, dark text ── */
    .stDataFrame {
        border-radius: var(--radius) !important;
        border: 1px solid var(--border) !important;
        box-shadow: var(--shadow-sm) !important;
        overflow: hidden !important;
    }
    /* dataframe header */
    [data-testid="stDataFrame"] thead th,
    [data-testid="stDataFrame"] th {
        background: #f8fafc !important;
        color: #111827 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: .875rem !important;
        font-weight: 700 !important;
        border-bottom: 2px solid var(--border) !important;
        padding: 10px 14px !important;
    }
    /* dataframe cells */
    [data-testid="stDataFrame"] tbody td,
    [data-testid="stDataFrame"] td {
        background: #ffffff !important;
        color: #111827 !important;
        font-size: .875rem !important;
        padding: 9px 14px !important;
        border-bottom: 1px solid #f3f4f6 !important;
    }
    [data-testid="stDataFrame"] tbody tr:hover td {
        background: #f8fafc !important;
    }
    /* glide table (newer streamlit) */
    [data-testid="glideDataEditor"] *,
    .glide-data-grid *,
    canvas { color: #111827 !important; }

    /* ── Code blocks ── */
    .stCode, pre, code {
        background: #f8fafc !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
        color: #1e3a8a !important;
        font-size: .85rem !important;
    }
    pre *, code * { color: #1e3a8a !important; }

    /* ── Divider ── */
    hr { border-color: var(--border) !important; margin: 1.2rem 0 !important; }

    /* ── Captions ── */
    .stCaption, small { color: var(--text-muted) !important; font-size: .82rem !important; }

    /* ── Spinner ── */
    .stSpinner > div { border-top-color: var(--accent) !important; }

    /* ─── Custom components ─── */

    /* Page header */
    .page-header {
        display: flex;
        align-items: flex-start;
        gap: 1rem;
        padding: 1.5rem 1.75rem;
        background: var(--white);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        box-shadow: var(--shadow-sm);
        margin-bottom: 1.75rem;
    }
    .page-header-icon {
        font-size: 1.5rem;
        width: 46px;
        height: 46px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: var(--accent-light);
        border-radius: 11px;
        flex-shrink: 0;
    }
    .page-header-text h1 {
        margin: 0 0 .25rem !important;
        font-size: 1.4rem !important;
        color: #111827 !important;
    }
    .page-header-text p {
        margin: 0;
        color: #6b7280 !important;
        font-size: .9rem;
    }

    /* Tags / pills */
    .tag {
        display: inline-block;
        background: #eff6ff;
        color: #1d4ed8 !important;
        border: 1px solid #bfdbfe;
        font-size: .75rem;
        font-weight: 600;
        padding: .2rem .65rem;
        border-radius: 20px;
        margin: .1rem .1rem;
        letter-spacing: .01em;
    }

    /* Status dot */
    .status-dot {
        display: inline-block;
        width: 8px; height: 8px;
        border-radius: 50%;
        flex-shrink: 0;
    }
    .dot-green { background: #16a34a; }
    .dot-amber { background: #d97706; }
    .dot-blue  { background: #2563eb; }
    .dot-red   { background: #dc2626; }

    /* Activity card */
    .activity-card {
        background: #ffffff;
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: .9rem 1.1rem;
        margin-bottom: .5rem;
        box-shadow: var(--shadow-sm);
        transition: box-shadow .15s;
    }
    .activity-card:hover { box-shadow: var(--shadow); }
    .activity-card strong, .activity-card span, .activity-card small {
        color: #111827 !important;
    }
    .op-badge {
        font-size: .7rem;
        font-weight: 700;
        letter-spacing: .06em;
        text-transform: uppercase;
        padding: .2rem .6rem;
        border-radius: 5px;
    }
    .op-retain { background: #eff6ff; color: #1d4ed8 !important; border: 1px solid #bfdbfe; }
    .op-recall { background: #f0fdf4; color: #16a34a !important; border: 1px solid #bbf7d0; }
    .op-reflect{ background: #fffbeb; color: #b45309 !important; border: 1px solid #fde68a; }
    .op-other  { background: #f3f4f6; color: #4b5563 !important; border: 1px solid #e5e7eb; }

    /* Compare columns */
    .compare-header {
        font-size: .78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: .08em;
        padding: .32rem .75rem;
        border-radius: 6px;
        display: inline-block;
        margin-bottom: .7rem;
    }
    .compare-bad  { background: #fef2f2; color: #991b1b !important; border: 1px solid #fecaca; }
    .compare-good { background: #f0fdf4; color: #166534 !important; border: 1px solid #bbf7d0; }

    /* Health chips — bigger, clearer */
    .health-row {
        display: flex;
        gap: .75rem;
        flex-wrap: wrap;
        margin: .75rem 0 1.4rem;
    }
    .health-chip {
        display: flex;
        align-items: center;
        gap: 10px;
        background: #ffffff;
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: .7rem 1.2rem;
        font-size: .95rem;
        font-weight: 500;
        color: #374151 !important;
        box-shadow: var(--shadow-sm);
        min-width: 148px;
    }
    .health-chip span { color: #374151 !important; }
    .health-chip strong { font-weight: 700; color: #111827 !important; }

    /* Nav custom items (legacy, unused now but keep for safety) */
    .nav-item {
        display: flex; align-items: center; gap: 10px;
        padding: 9px 12px; border-radius: 8px;
        font-size: .9rem; font-weight: 500; color: #4b5563;
        margin-bottom: 2px; transition: background .15s, color .15s;
        border: none;
    }
    .nav-item:hover { background: #f3f4f6; color: #111827; }
    .nav-item.active { background: #eff6ff; color: #1d4ed8; font-weight: 600; }
    .nav-icon { width: 30px; height: 30px; display: flex; align-items: center;
        justify-content: center; border-radius: 7px; font-size: 14px;
        flex-shrink: 0; background: #f3f4f6; }
    .nav-item.active .nav-icon { background: #dbeafe; }
    .nav-label { flex: 1; letter-spacing: -.01em; }
    .nav-group-label {
        font-size: .68rem; font-weight: 700; text-transform: uppercase;
        letter-spacing: .1em; color: #9ca3af; padding: 0 12px; margin: 14px 0 5px;
    }
    .nav-divider { height: 1px; background: #f3f4f6; margin: 10px 0; }
    .backend-badge {
        display: inline-flex; align-items: center; gap: 5px;
        font-size: .68rem; background: #f3f4f6; border: 1px solid #e5e7eb;
        color: #6b7280 !important; padding: 2px 8px; border-radius: 4px;
        font-family: 'Courier New', monospace; margin-top: 4px;
    }
    .status-live { display: inline-block; width: 6px; height: 6px;
        border-radius: 50%; background: #22c55e; flex-shrink: 0; }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #c4cad6; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ── Helpers ───────────────────────────────────────────────────────────────────

def api_get(path: str) -> Any:
    r = requests.get(f"{API_URL}{path}", timeout=45)
    r.raise_for_status()
    return r.json()


def api_post(path: str, payload: dict[str, Any] | None = None) -> Any:
    r = requests.post(f"{API_URL}{path}", json=payload or {}, timeout=60)
    r.raise_for_status()
    return r.json()


def page_header(icon: str, title: str, subtitle: str = "") -> None:
    st.markdown(
        f"""
        <div class="page-header">
          <div class="page-header-icon">{icon}</div>
          <div class="page-header-text">
            <h1>{title}</h1>
            <p>{subtitle}</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section(label: str) -> None:
    st.markdown(f'<div class="section-label">{label}</div>', unsafe_allow_html=True)


def tags_html(tags: list[str]) -> str:
    return "".join(f'<span class="tag">{t}</span>' for t in tags)


def memory_badge(mode: str | None = None, fallback: bool | None = None) -> None:
    if fallback is True or (mode and "fallback" in mode.lower()):
        st.warning("Memory mode: Local fallback — configure HINDSIGHT_API_KEY to enable cloud memory.")
    else:
        st.success(f"Memory mode: {mode or 'Hindsight Cloud'}")


def source_badge(source: str | None, warning: str | None = None) -> None:
    if source == "hindsight":
        st.success("Memory source: Hindsight Cloud")
    elif source == "fallback":
        st.warning("Memory source: local fallback")
    else:
        st.info(f"Memory source: {source or 'unknown'}")
    if warning:
        st.warning(warning)


def load_prospects() -> list[dict[str, Any]]:
    try:
        return api_get("/prospects")
    except requests.RequestException:
        return []


def prospect_picker(label: str = "Select prospect") -> dict[str, Any] | None:
    prospects = load_prospects()
    if not prospects:
        st.info("No prospects yet. Seed demo data or log an interaction first.")
        return None
    labels = [f"{p['company']}  —  {p['name']}  ({p['role_title']})" for p in prospects]
    idx = st.selectbox(label, range(len(prospects)), format_func=lambda i: labels[i])
    return prospects[idx]


def show_memory_items(memories: list[dict[str, Any]]) -> None:
    if not memories:
        st.info("No recalled memories returned yet.")
        return
    for i, item in enumerate(memories, 1):
        mem_type = item.get("type", "memory")
        with st.expander(f"Memory {i}  ·  {mem_type}"):
            st.write(item.get("text", item))
            row = st.columns(3)
            if item.get("tags"):
                row[0].markdown(tags_html(item["tags"]), unsafe_allow_html=True)
            if item.get("score") is not None:
                row[1].caption(f"Relevance score: **{item['score']}**")
            if item.get("created_at"):
                row[2].caption(item["created_at"])
            if item.get("metadata"):
                st.json(item["metadata"])


# ── Pages ─────────────────────────────────────────────────────────────────────

def dashboard_page() -> None:
    page_header("🧠", "Sales Memory Agent", "Deal-aware sales intelligence · retain · recall · reflect")

    try:
        stats = api_get("/dashboard")
    except requests.RequestException as exc:
        st.error(f"Backend not reachable at `{API_URL}`. Start FastAPI first.\n\n{exc}")
        return

    memory_badge(fallback=stats["fallback_mode"])
    health = stats.get("memory_health", {})

    section("Hindsight Memory Status")
    chips = [
        ("Enabled",    health.get("hindsight_enabled"), "dot-blue"),
        ("Configured", health.get("configured"),        "dot-blue"),
        ("Reachable",  health.get("reachable"),         "dot-green"),
        ("Fallback",   health.get("fallback_enabled"),  "dot-amber"),
    ]
    html = '<div class="health-row">'
    for label, val, dot_cls in chips:
        yes = bool(val)
        dot = dot_cls if yes else "dot-amber"
        text = "Yes" if yes else "No"
        html += (
            f'<div class="health-chip">'
            f'<span class="status-dot {dot}"></span>'
            f'<span>{label}: <strong>{text}</strong></span>'
            f'</div>'
        )
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

    if health.get("bank_id"):
        st.caption(f"Bank ID: `{health['bank_id']}`")
    if health.get("last_error"):
        st.warning(health["last_error"])

    section("Overview")
    c1, c2, c3 = st.columns(3)
    c1.metric("Prospects",          stats["prospects"])
    c2.metric("Interactions",        stats["interactions"])
    c3.metric("Retained Memories",   stats["retained_memories"])

    left, right = st.columns([1, 2], gap="large")

    with left:
        section("Top Objections")
        if stats["top_objections"]:
            st.dataframe(pd.DataFrame(stats["top_objections"]), hide_index=True, use_container_width=True)
        else:
            st.info("No objections captured yet.")

    with right:
        section("Recent Memory Activity")
        for item in stats["recent_activity"]:
            op = item["operation"].lower()
            op_cls = {"retain": "op-retain", "recall": "op-recall", "reflect": "op-reflect"}.get(op, "op-other")
            t_html = tags_html(item.get("tags", []))
            st.markdown(
                f"""
                <div class="activity-card">
                  <span class="op-badge {op_cls}">{item['operation'].upper()}</span>&nbsp;
                  <strong>{item['company']}</strong> / {item['prospect_name']}
                  <br>
                  <span style="font-size:.78rem;color:#9ca3af;">{item['created_at']}</span>
                  &nbsp;&nbsp;{t_html}
                </div>
                """,
                unsafe_allow_html=True,
            )


def log_interaction_page() -> None:
    page_header("📝", "Log Interaction", "Record a meeting and retain memory for future deal intelligence.")

    with st.form("interaction_form"):
        section("Prospect Details")
        c1, c2, c3 = st.columns(3)
        prospect_name       = c1.text_input("Prospect name")
        company             = c2.text_input("Company")
        role_title          = c3.text_input("Role / Title")

        section("Interaction Details")
        interaction_type = st.selectbox(
            "Interaction type",
            ["Discovery call", "Demo", "Security review", "Pricing call", "Procurement update", "Sales interaction"],
        )
        meeting_notes = st.text_area("Meeting notes", height=130, placeholder="Summarise what happened in this meeting…")

        section("Deal Intelligence")
        c4, c5 = st.columns(2)
        objections           = c4.text_input("Objections raised")
        competitor_mentioned = c5.text_input("Competitor mentioned")

        c6, c7 = st.columns(2)
        budget   = c6.text_input("Budget")
        timeline = c7.text_input("Timeline")

        decision_makers = st.text_input("Decision makers")
        next_steps      = st.text_input("Next steps")
        deal_id         = st.text_input("Deal ID (optional)")

        submitted = st.form_submit_button("Save & Retain Memory", type="primary", use_container_width=True)

    if submitted:
        payload = {
            "prospect_name": prospect_name, "company": company, "role_title": role_title,
            "interaction_type": interaction_type, "meeting_notes": meeting_notes,
            "objections": objections, "competitor_mentioned": competitor_mentioned,
            "budget": budget, "timeline": timeline,
            "decision_makers": decision_makers, "next_steps": next_steps,
            "deal_id": deal_id or None,
        }
        try:
            result = api_post("/interactions", payload)
            if result["memory_status"] == "retained":
                st.success("Interaction saved. Memory retained in Hindsight.")
            elif result["memory_status"] == "fallback":
                st.warning("Interaction saved. Memory retained in local fallback.")
            else:
                st.error("Interaction saved, but memory retain failed.")
            if result.get("memory_warning"):
                st.warning(result["memory_warning"])
            if result.get("memory_error"):
                st.error(result["memory_error"])
            section("Retained Payload Preview")
            st.code(result.get("retained_payload", {}).get("preview", ""), language="text")
            with st.expander("Full JSON response"):
                st.json(result)
        except requests.RequestException as exc:
            st.error(f"Could not save interaction: {exc}")


def sales_brief_page() -> None:
    page_header("📊", "Sales Brief", "Generate a deal-aware briefing document using recalled memory.")
    prospect = prospect_picker()
    if prospect and st.button("Generate Brief", type="primary"):
        with st.spinner("Recalling memories and generating brief…"):
            result = api_get(f"/prospects/{prospect['id']}/brief")
        memory_badge(result["memory_mode"])
        source_badge(result.get("memory_source"), result.get("memory_warning"))
        section("Recalled Memories")
        show_memory_items(result["recalled_memories"])
        section("Generated Brief")
        st.markdown(result["content"])


def followup_page() -> None:
    page_header("✉️", "Follow-up Email", "See how memory transforms a generic template into a personalised message.")
    prospect = prospect_picker()
    if prospect and st.button("Generate Follow-up", type="primary"):
        with st.spinner("Personalising from recalled history…"):
            result = api_get(f"/prospects/{prospect['id']}/followup")
        memory_badge(result["memory_mode"])
        source_badge(result.get("memory_source"), result.get("memory_warning"))

        generic = _generic_email(result["prospect"]["company"])
        left, right = st.columns(2, gap="large")
        with left:
            st.markdown('<span class="compare-header compare-bad">Without Memory</span>', unsafe_allow_html=True)
            st.code(generic, language="markdown")
        with right:
            st.markdown('<span class="compare-header compare-good">With Hindsight Memory</span>', unsafe_allow_html=True)
            st.code(result["content"], language="markdown")

        section("Memory Used")
        show_memory_items(result["recalled_memories"])


def before_after_page() -> None:
    page_header("🔬", "Before vs After Demo", "Side-by-side contrast — generic assistant vs memory-aware agent.")
    prospect = prospect_picker()
    if prospect and st.button("Run Comparison", type="primary"):
        result = api_get(f"/demo/before-after/{prospect['id']}")
        memory_badge(result["memory_mode"])
        source_badge(result.get("memory_source"), result.get("memory_warning"))

        left, right = st.columns(2, gap="large")
        with left:
            st.markdown('<span class="compare-header compare-bad">Without Memory</span>', unsafe_allow_html=True)
            st.code(result["without_memory"], language="markdown")
        with right:
            st.markdown('<span class="compare-header compare-good">With Hindsight Memory</span>', unsafe_allow_html=True)
            st.code(result["with_hindsight_memory"], language="markdown")

        section("Recall Activity")
        show_memory_items(result["recalled_memories"])


def inspector_page() -> None:
    page_header("🔍", "Memory Inspector", "Browse retained and recalled memory items by prospect or globally.")
    prospect = prospect_picker("Filter by prospect")
    if prospect:
        result = api_get(f"/prospects/{prospect['id']}/memory")
        source_badge(result.get("memory_source"), result.get("memory_warning"))
        section("Recalled Memories")
        show_memory_items(result.get("recalled_memories", []))
        activities = result.get("activity", [])
    else:
        activities = api_get("/memory")

    if not activities:
        st.info("No memory activity yet.")
        return

    section("Activity Log")
    for item in activities:
        op = item["operation"].lower()
        op_cls = {"retain": "op-retain", "recall": "op-recall", "reflect": "op-reflect"}.get(op, "op-other")
        with st.expander(f"{item['operation'].upper()}  ·  {item['company']}  ·  {item['created_at']}"):
            c1, c2 = st.columns(2)
            c1.write(f"**Prospect:** {item['prospect_name']}")
            c1.write(f"**Company:** {item['company']}")
            c1.write(f"**Deal ID:** {item['deal_id']}")
            c2.write(f"**Provider:** {item['provider']}")
            c2.write(f"**Fallback mode:** {item['fallback_mode']}")
            st.markdown(tags_html(item.get("tags", [])), unsafe_allow_html=True)
            st.write("**Content sent / query**")
            st.text(item["content"])
            st.write("**Provider result**")
            st.text(item["result"])


# ── Utilities ─────────────────────────────────────────────────────────────────

def _generic_email(company: str) -> str:
    return (
        f"Subject: Following up on our conversation\n\n"
        f"Hi there,\n\n"
        f"Thanks for taking the time to speak with us about {company}. "
        f"I wanted to follow up and see whether you had any questions about our solution. "
        f"We would be happy to schedule a demo and discuss next steps at your convenience.\n\n"
        f"Best regards,\nSales Team"
    )


def seed_button() -> None:
    if st.sidebar.button("🌱  Seed Demo Data", use_container_width=True, key="seed_btn"):
        try:
            result = api_post("/seed")
            st.sidebar.success(f"✓ Seeded {result['created_interactions']} interactions.")
        except requests.RequestException as exc:
            st.sidebar.error(f"Seed failed: {exc}")


# ── Navigation ────────────────────────────────────────────────────────────────

PAGES = {
    "Dashboard":          dashboard_page,
    "Log Interaction":    log_interaction_page,
    "Sales Brief":        sales_brief_page,
    "Follow-up Email":    followup_page,
    "Before vs After":    before_after_page,
    "Memory Inspector":   inspector_page,
}

NAV_ITEMS = [
    ("Dashboard",        "📊"),
    ("Log Interaction",  "📝"),
    ("Sales Brief",      "📄"),
    ("Follow-up Email",  "✉️"),
    ("Before vs After",  "⚡"),
    ("Memory Inspector", "🔍"),
]

# ── Init session state ──
if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"

# ── Sidebar brand ──
st.sidebar.markdown(
    """
    <div style="padding:20px 4px 8px;">
      <div style="display:flex;align-items:center;gap:10px;">
        <div style="width:36px;height:36px;background:#eff6ff;border-radius:10px;
                    display:flex;align-items:center;justify-content:center;font-size:18px;
                    flex-shrink:0;">🧠</div>
        <div>
          <div style="font-family:'Plus Jakarta Sans',sans-serif;font-weight:800;
                      font-size:.97rem;color:#111827;letter-spacing:-.3px;line-height:1.2;">
            Sales Memory</div>
          <div style="font-size:.68rem;color:#9ca3af;margin-top:1px;">
            Powered by Hindsight</div>
        </div>
      </div>
    </div>
    <div class="nav-divider"></div>
    """,
    unsafe_allow_html=True,
)

# ── Nav group label ──
st.sidebar.markdown('<div class="nav-group-label">Main Menu</div>', unsafe_allow_html=True)

# ── Clickable nav buttons ──
for key, icon in NAV_ITEMS:
    is_active = st.session_state.current_page == key

    # Active item: styled via markdown (non-clickable visual) — button overlaid via CSS trick
    # We render a real st.button per item, then style it to look like a nav row
    btn_type = "primary" if is_active else "secondary"

    # Label with icon baked in
    label = f"{icon}  {key}"

    if st.sidebar.button(
        label,
        key=f"nav_{key}",
        use_container_width=True,
        type=btn_type,
    ):
        st.session_state.current_page = key
        st.rerun()

st.sidebar.markdown('<div class="nav-divider" style="margin-top:8px;"></div>', unsafe_allow_html=True)

# ── Tools section ──
st.sidebar.markdown('<div class="nav-group-label">Tools</div>', unsafe_allow_html=True)
seed_button()

# ── Footer ──
st.sidebar.markdown(
    f"""
    <div style="padding:14px 4px 8px;margin-top:4px;">
      <div style="font-size:.68rem;color:#9ca3af;margin-bottom:4px;">Backend endpoint</div>
      <div class="backend-badge"><span class="status-live"></span>{API_URL}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Render active page ──
PAGES[st.session_state.current_page]()