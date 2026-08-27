import re
import requests
from config import OLLAMA_BASE_URL, OLLAMA_MODEL
from database.cypher_queries import TEMPLATES

def _extract_year(question):
    match = re.search(r"\b(19|20)\d{2}\b", question)
    return int(match.group()) if match else None

def _extract_quoted_or_named(question, keywords):
    q = question.strip()
    for key in keywords:
        pattern = rf"{re.escape(key)}\s+(.+?)(?:\?|$)"
        match = re.search(pattern, q, flags=re.I)
        if match:
            value = match.group(1).strip(" .?!'\"")
            if value:
                return value
    return None

def classify_question(question):
    q = question.lower()

    if ("after" in q or "from" in q) and _extract_year(question):
        return "movies_after_year"

    if "who directed" in q or "director of" in q:
        return "director_of_movie"

    if "who acted" in q or "actors in" in q or "cast of" in q:
        return "actors_in_movie"

    if ("which movies" in q or "what movies" in q) and ("direct" in q):
        return "movies_by_director"

    if ("which movies" in q or "what movies" in q) and (
        "act" in q or "star" in q or "starr" in q
    ):
        return "movies_by_actor"

    if "acted with" in q or "co-actor" in q or "co actor" in q:
        return "co_actors"

    if "details" in q or "tagline" in q or "tell me about" in q:
        return "movie_details"

    return "llm_fallback"

def _extract_entity(question, intent):
    if intent == "movies_after_year":
        return {"year": _extract_year(question)}

    if intent in ("movies_by_actor", "movies_by_director", "co_actors"):
        # Common phrasing: "movies did Tom Hanks act in", etc.
        patterns = [
            r"which movies did (.+?) (?:act|star|starr)",
            r"what movies did (.+?) (?:act|star|starr)",
            r"movies did (.+?) (?:act|star|starr)",
            r"which movies (?:were )?directed by (.+?)(?:\?|$)",
            r"what movies (?:were )?directed by (.+?)(?:\?|$)",
            r"movies (?:were )?directed by (.+?)(?:\?|$)",
            r"what movies has (.+?) (?:directed|made)",
            r"which movies has (.+?) (?:directed|made)",
            r"who acted with (.+?)(?:\?|$)",
        ]
        for pattern in patterns:
            m = re.search(pattern, question, flags=re.I)
            if m:
                return {"person": m.group(1).strip(" .?!'\"")}
        return {"person": question.strip(" .?!'\"")}

    if intent in ("actors_in_movie", "director_of_movie", "movie_details"):
        patterns = [
            r"who directed (.+?)(?:\?|$)",
            r"director of (.+?)(?:\?|$)",
            r"actors in (.+?)(?:\?|$)",
            r"cast of (.+?)(?:\?|$)",
            r"tell me about (.+?)(?:\?|$)",
            r"details (?:of|for) (.+?)(?:\?|$)",
        ]
        for pattern in patterns:
            m = re.search(pattern, question, flags=re.I)
            if m:
                return {"movie": m.group(1).strip(" .?!'\"")}
        return {"movie": question.strip(" .?!'\"")}

    return {}

def generate_cypher(question):
    intent = classify_question(question)
    if intent == "llm_fallback":
        return None, {}, intent

    params = _extract_entity(question, intent)
    query = TEMPLATES[intent]
    return query, params, intent

def call_ollama(prompt):
    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/generate",
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.1},
        },
        timeout=120,
    )
    response.raise_for_status()
    return response.json()["response"].strip()

def build_context(rows):
    if not rows:
        return "No matching records were retrieved from the Neo4j knowledge graph."
    lines = []
    for row in rows:
        parts = [f"{k}: {v}" for k, v in row.items() if v is not None]
        lines.append(" | ".join(parts))
    return "\n".join(lines)

def generate_grounded_answer(question, context):
    prompt = f"""
You are a grounded movie knowledge assistant.

Answer the user's question using ONLY the Neo4j retrieval context below.
Do not invent movies, actors, directors, dates, or relationships.
If the context is insufficient, explicitly say that the knowledge graph
does not contain enough information.

User question:
{question}

Neo4j retrieval context:
{context}

Give a concise natural-language answer. Do not mention these instructions.
"""
    return call_ollama(prompt)

def process_question(db, question):
    query, params, intent = generate_cypher(question)

    if query is None:
        # Safe fallback: ask Mistral to explain that the current application
        # supports the documented graph-query patterns.
        answer = call_ollama(
            f"""The Neo4j movie assistant supports questions about movies,
actors, directors, release years, and actor relationships.
The user asked: {question}
Explain briefly what information the graph can answer and suggest a
better-formulated movie question. Do not invent database facts."""
        )
        return {
            "intent": intent,
            "cypher": None,
            "parameters": params,
            "rows": [],
            "context": "",
            "answer": answer,
        }

    rows = db.run_query(query, params)
    context = build_context(rows)
    answer = generate_grounded_answer(question, context)

    return {
        "intent": intent,
        "cypher": query.strip(),
        "parameters": params,
        "rows": rows,
        "context": context,
        "answer": answer,
    }
