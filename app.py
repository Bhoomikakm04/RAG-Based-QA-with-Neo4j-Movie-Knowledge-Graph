import streamlit as st
from database.neo4j_connection import Neo4jConnection
from ui.dashboard import render_dashboard
from ui.ask_question import render_ask_question
from ui.graph_explorer import render_graph_explorer
from ui.evaluation import render_evaluation
from ui.theme import load_css, inject_js

st.set_page_config(
    page_title="GraphRAG Movie Assistant",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_css()
inject_js()

@st.cache_resource
def get_db():
    return Neo4jConnection()


def main():
    try:
        db = get_db()
        db.verify_connection()
        db_ok = True
    except Exception as e:
        db = None
        db_ok = False
        st.session_state["db_error"] = str(e)

    with st.sidebar:
        st.markdown('''<div class="brand"><div class="brand-mark">🎬</div><div><div class="brand-title">GraphRAG</div><div class="brand-sub">Movie Knowledge Assistant</div></div></div>''', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-section">Workspace</div>', unsafe_allow_html=True)
        nav_options = {
            "Home": "Home",
            "Ask Question": "Ask Question",
            "Graph Explorer": "Graph Explorer",
            "Evaluation": "Evaluation",
        }
        selected_nav = st.radio(
            "Navigation", list(nav_options.keys()),
            label_visibility="collapsed"
        )
        page = nav_options[selected_nav]
        st.markdown('<div class="sidebar-section">System status</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="margin-bottom:8px">{"🟢" if db_ok else "🔴"} <b>Neo4j</b> &nbsp; {"Connected" if db_ok else "Not connected"}</div>', unsafe_allow_html=True)
        st.markdown('<div style="margin-bottom:8px">🟡 <b>Ollama</b> &nbsp; On demand</div>', unsafe_allow_html=True)
        st.markdown('<div class="footer-note">Neo4j • Streamlit • Mistral</div>', unsafe_allow_html=True)

    if page == "Home":
        render_dashboard(db, db_ok)
    elif page == "Ask Question":
        render_ask_question(db)
    elif page == "Graph Explorer":
        render_graph_explorer(db)
    else:
        render_evaluation(db)

if __name__ == "__main__":
    main()
