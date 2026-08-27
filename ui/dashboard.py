import streamlit as st
from ui.theme import page_header, metric_card, section_title


def render_dashboard(db, db_ok):
    st.markdown('''<div class="hero">
      <div class="hero-kicker">Knowledge Graph • Retrieval • Generation</div>
      <h1>Explore movies through a connected knowledge graph.</h1>
      <p>Ask natural-language questions, retrieve grounded facts from Neo4j, and let the local Mistral model turn graph evidence into concise answers.</p>
      <div class="hero-flow">
        <span class="flow-chip">Question</span><span class="flow-arrow">→</span>
        <span class="flow-chip">Cypher</span><span class="flow-arrow">→</span>
        <span class="flow-chip">Neo4j</span><span class="flow-arrow">→</span>
        <span class="flow-chip">Graph Context</span><span class="flow-arrow">→</span>
        <span class="flow-chip">Mistral</span>
      </div>
    </div>''', unsafe_allow_html=True)

    if not db_ok:
        st.error("Neo4j is not connected. Check your local .env configuration.")
        if "db_error" in st.session_state:
            st.code(st.session_state["db_error"])
        return

    try:
        counts = db.get_counts()
    except Exception as e:
        st.error(f"Could not read graph statistics: {e}")
        return

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: metric_card("Movies", counts.get("movies", 0), "🎞️", "blue")
    with c2: metric_card("People", counts.get("people", 0), "👤", "violet")
    with c3: metric_card("Relationships", counts.get("relationships", 0), "🔗", "green")

    section_title("What you can do", "Four parts of the assignment prototype")
    cols = st.columns(4)
    cards = [
        ("💬", "Ask questions", "Convert supported natural-language movie questions into Cypher retrieval queries."),
        ("🕸️", "Explore the graph", "Visualize people, movies, and their relationships as an interactive network."),
        ("🧠", "Ground answers", "Use retrieved Neo4j facts as context for the local Mistral model."),
        ("📊", "Evaluate", "Run the supplied question set and inspect retrieval coverage and latency."),
    ]
    for col, (icon, title, text) in zip(cols, cards):
        with col:
            st.markdown(f'<div class="info-card"><div class="info-icon">{icon}</div><h3>{title}</h3><p>{text}</p></div>', unsafe_allow_html=True)

    section_title("Try these questions", "Examples that match the current graph-query templates")
    examples = [
        "Which movies did Tom Hanks act in?",
        "Who directed The Matrix?",
        "Who acted in The Matrix?",
        "Which movies were released after 2000?",
        "Who acted with Tom Hanks?",
    ]
    cols = st.columns(2)
    for i, q in enumerate(examples):
        with cols[i % 2]:
            st.markdown(f'<div class="schema-box" style="margin-bottom:10px"><span class="schema-chip">{q}</span></div>', unsafe_allow_html=True)

    try:
        schema = db.get_schema()
        section_title("Knowledge graph schema", "Live schema read directly from Neo4j")
        a, b = st.columns(2)
        with a:
            st.markdown('<div class="schema-box"><div class="schema-label">Node labels</div>' + ''.join(f'<span class="schema-chip">{x}</span>' for x in schema["labels"]) + '</div>', unsafe_allow_html=True)
        with b:
            st.markdown('<div class="schema-box"><div class="schema-label">Relationship types</div>' + ''.join(f'<span class="schema-chip rel">{x}</span>' for x in schema["relationships"]) + '</div>', unsafe_allow_html=True)
    except Exception as e:
        st.warning(str(e))
