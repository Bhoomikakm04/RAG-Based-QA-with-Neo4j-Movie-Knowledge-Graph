import streamlit as st
from rag.question_processor import process_question
from ui.theme import page_header, section_title


def render_ask_question(db):
    page_header("GraphRAG / Query", "Ask the movie graph", "Ask about movies, actors, directors, relationships, or release years. Retrieval happens against the live Neo4j database.")

    examples = [
        "Which movies did Tom Hanks act in?",
        "Who directed The Matrix?",
        "Who acted in The Matrix?",
        "Which movies were released after 2000?",
        "Who acted with Tom Hanks?",
    ]
    selected = st.selectbox("Start from an example", ["Type your own"] + examples)
    default = "" if selected == "Type your own" else selected
    question = st.text_input("Your question", value=default, placeholder="e.g. Which movies did Tom Hanks act in?")

    if st.button("Run GraphRAG  →", type="primary", use_container_width=True):
        if not question.strip():
            st.warning("Enter a question first.")
            return
        with st.spinner("Retrieving graph evidence and generating a grounded answer..."):
            try:
                result = process_question(db, question)
            except Exception as e:
                st.error(f"Pipeline error: {e}")
                return

        section_title("Answer", "Generated from the retrieved Neo4j context")
        st.markdown(f'<div class="hero" style="padding:24px"><p style="font-size:17px;color:#e8eef9;margin:0;line-height:1.7">{result["answer"]}</p></div>', unsafe_allow_html=True)

        section_title("Retrieval summary")
        a, b, c = st.columns(3)
        with a: st.metric("Intent", result["intent"].replace("_", " ").title())
        with b: st.metric("Retrieved records", len(result["rows"]))
        with c: st.metric("Grounded", "Yes" if result["rows"] else "No")

        with st.expander("① Generated / selected Cypher"):
            if result["cypher"]:
                st.code(result["cypher"], language="cypher")
                st.json(result["parameters"])
            else:
                st.info("No supported Cypher template was selected.")
        with st.expander("② Neo4j retrieved data"):
            if result["rows"]: st.dataframe(result["rows"], use_container_width=True)
            else: st.info("No records were retrieved.")
        with st.expander("③ Context supplied to Mistral"):
            st.text(result["context"] or "No graph context.")
