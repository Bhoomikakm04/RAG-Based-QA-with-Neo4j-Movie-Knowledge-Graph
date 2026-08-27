import json
import time
from pathlib import Path
import streamlit as st
from rag.question_processor import process_question
from ui.theme import page_header, section_title

TEST_FILE = Path("evaluation/test_questions.json")


def render_evaluation(db):
    page_header("Quality / Evaluation", "Evaluate retrieval", "Run the included test set and inspect how reliably the application retrieves graph evidence.")
    if not TEST_FILE.exists():
        st.error("evaluation/test_questions.json not found.")
        return
    tests = json.loads(TEST_FILE.read_text(encoding="utf-8"))
    c1, c2 = st.columns(2)
    with c1: st.metric("Test questions", len(tests))
    with c2: st.metric("Evaluation mode", "Graph retrieval")

    if st.button("Run evaluation  →", type="primary", use_container_width=True):
        results = []
        progress = st.progress(0)
        for i, item in enumerate(tests):
            start = time.perf_counter()
            try:
                result = process_question(db, item["question"])
                elapsed = time.perf_counter() - start
                results.append({
                    "id": item["id"], "category": item["category"], "question": item["question"],
                    "expected_type": item["expected_type"], "intent": result["intent"],
                    "retrieved_records": len(result["rows"]), "latency_seconds": round(elapsed, 2),
                    "status": "Retrieved" if result["rows"] else "No retrieval",
                })
            except Exception as e:
                results.append({"id": item["id"], "category": item["category"], "question": item["question"], "expected_type": item["expected_type"], "intent": "error", "retrieved_records": 0, "latency_seconds": 0, "status": str(e)})
            progress.progress((i + 1) / len(tests))
        st.session_state["evaluation_results"] = results

    results = st.session_state.get("evaluation_results")
    if results:
        retrieved = sum(r["retrieved_records"] > 0 for r in results)
        section_title("Results", f"{retrieved} of {len(results)} questions returned graph evidence")
        st.dataframe(results, use_container_width=True)
