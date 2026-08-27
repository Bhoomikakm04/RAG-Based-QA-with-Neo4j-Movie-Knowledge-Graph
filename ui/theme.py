import streamlit as st
from pathlib import Path

ASSET_DIR = Path(__file__).resolve().parent.parent / "assets"


def load_css():
    css_path = ASSET_DIR / "style.css"
    css = css_path.read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def inject_js():
    # The main interactive graph is powered by PyVis/vis-network JavaScript.
    # This lightweight script adds a polished page-load class without affecting
    # Streamlit's Python state or API behavior.
    js_path = ASSET_DIR / "app.js"
    js = js_path.read_text(encoding="utf-8")
    st.components.v1.html(f"<script>{js}</script>", height=0)


def page_header(eyebrow, title, description=None):
    desc = f'<p class="page-desc">{description}</p>' if description else ""
    st.markdown(
        f'''<div class="page-header">
            <div class="eyebrow">{eyebrow}</div>
            <h1>{title}</h1>
            {desc}
        </div>''',
        unsafe_allow_html=True,
    )


def metric_card(label, value, icon, tone="blue"):
    st.markdown(
        f'''<div class="metric-card {tone}">
            <div class="metric-icon">{icon}</div>
            <div><div class="metric-label">{label}</div><div class="metric-value">{value}</div></div>
        </div>''',
        unsafe_allow_html=True,
    )


def section_title(title, subtitle=None):
    sub = f'<div class="section-subtitle">{subtitle}</div>' if subtitle else ""
    st.markdown(f'<div class="section-title"><h2>{title}</h2>{sub}</div>', unsafe_allow_html=True)


def status_pill(label, ok=True):
    state = "online" if ok else "offline"
    dot = "●"
    return f'<span class="status-pill {state}"><span>{dot}</span>{label}</span>'
