# GraphRAG Movie Knowledge Assistant

A small Retrieval-Augmented Generation (RAG) application that uses the
Neo4j Movies dataset as a knowledge graph backend and Mistral through Ollama
to generate grounded natural-language answers.

## Architecture

User Question
→ Question Processing
→ Cypher Query / Template
→ Neo4j Movies Knowledge Graph
→ Retrieved Graph Context
→ Mistral via Ollama
→ Grounded Answer

## Requirements

- Python 3.10+
- Neo4j Aura or Neo4j Desktop
- A Neo4j Movies dataset
- Ollama
- Mistral model

## Setup

1. Create and activate a virtual environment.

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env`.

4. Put your own Neo4j Aura connection details in `.env`.
   Do not commit `.env`.

5. Make sure Ollama is running and Mistral is available:

```bash
ollama list
ollama run mistral
```

6. Start the application:

```bash
streamlit run app.py
```

## Included features

- Neo4j connectivity check
- Graph statistics dashboard
- Cypher query templates
- Natural-language question processing
- Neo4j retrieval
- Context construction
- Mistral generation through Ollama
- RAG pipeline transparency
- Graph explorer
- Basic evaluation page

## Important security note

Never place Neo4j passwords directly in Python source code or screenshots.
Use `.env` locally and keep it out of Git.

## Assignment mapping

Expected outcome: Load and use Neo4j movie graph
→ `database/neo4j_connection.py`

Expected outcome: Convert questions into graph queries
→ `rag/question_processor.py` and `database/cypher_queries.py`

Expected outcome: Retrieve relevant actor/movie data
→ Neo4j read-only queries

Expected outcome: Generate grounded answers
→ Mistral context generation

Expected outcome: Basic movie-related QA/recommendation support
→ Ask Question + Graph Explorer + evaluation workflow
