Delete the old README and replace it with this `README.md`. I’ve made it more professional for GitHub while keeping the description aligned with what your project actually does.

````markdown
# RAG-Based QA with Neo4j Movie Knowledge Graph

A Retrieval-Augmented Generation (RAG) application that combines the **Neo4j Movies Knowledge Graph** with a local **Mistral Large Language Model (LLM)** through Ollama to answer natural-language questions using retrieved graph information.

The system converts user questions into Cypher queries, retrieves relevant information from the Neo4j knowledge graph, constructs grounded context, and uses Mistral to generate natural-language answers.

---

## Project Overview

Traditional question-answering systems may generate answers without directly referencing structured data.

This project uses a **Knowledge Graph + RAG architecture** to ground the generated answers in information retrieved from a Neo4j movie database.

The application provides an interactive Streamlit interface for:

- Asking natural-language movie questions
- Retrieving information from Neo4j
- Exploring movie and person relationships
- Viewing the RAG retrieval and generation process
- Evaluating the QA system

---

## Architecture

```text
User Question
      ↓
Question Processing
      ↓
Cypher Query / Query Template
      ↓
Neo4j Movie Knowledge Graph
      ↓
Relevant Graph Facts
      ↓
Retrieved Graph Context
      ↓
Mistral LLM via Ollama
      ↓
Grounded Natural-Language Answer
````

---

## Technologies Used

| Technology    | Purpose                               |
| ------------- | ------------------------------------- |
| Python        | Application development               |
| Streamlit     | Interactive web interface             |
| Neo4j         | Knowledge graph database              |
| Cypher        | Graph query language                  |
| Ollama        | Local LLM runtime                     |
| Mistral       | Natural-language generation           |
| RAG           | Retrieval-grounded question answering |
| python-dotenv | Environment configuration             |

---

## Knowledge Graph

The application uses the Neo4j Movies dataset containing movie and person information.

### Node Labels

* `Movie`
* `Person`

### Relationship Types

* `ACTED_IN`
* `DIRECTED`
* `FOLLOWS`
* `PRODUCED`
* `REVIEWED`
* `WROTE`

The application retrieves relationships between people and movies using read-only Cypher queries.

---

## Features

### 1. Ask Question

Users can enter natural-language movie-related questions.

Example questions:

```text
Which movies did Tom Hanks act in?

Who directed The Matrix?

Who acted in The Matrix?

Which movies were released after 2000?
```

The system processes the question, retrieves relevant information from Neo4j, and uses Mistral to generate a grounded response.

---

### 2. Graph Explorer

The Graph Explorer allows users to inspect relationships stored in the Neo4j Movies Knowledge Graph.

Users can search for a person and retrieve their connected movies and relationships.

Example:

```text
Tom Cruise
      ↓
ACTED_IN
      ↓
Top Gun
A Few Good Men
Jerry Maguire
```

The application also displays the graph schema and relationship types.

---

### 3. RAG Pipeline Transparency

The application exposes the major stages of the RAG workflow:

```text
Question
   ↓
Query Processing
   ↓
Cypher
   ↓
Neo4j Retrieval
   ↓
Graph Context
   ↓
Mistral
   ↓
Answer
```

This makes it easier to understand how retrieved knowledge is used to generate the final answer.

---

### 4. Evaluation

The project includes a basic evaluation workflow for testing the supplied question set and examining retrieval performance and response latency.

---

### 5. Graph Statistics

The dashboard displays statistics retrieved from Neo4j, including:

* Number of movies
* Number of people
* Number of relationships

---

## Project Structure

```text
RAG-Based-QA-with-Neo4j-Movie-Knowledge-Graph/
│
├── database/
│   ├── neo4j_connection.py
│   └── cypher_queries.py
│
├── rag/
│   └── question_processor.py
│
├── ui/
│   └── ...
│
├── evaluation/
│   └── ...
│
├── docs/
│   └── ...
│
├── app.py
├── config.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── run_app.bat
```

---

## Requirements

Before running the application, make sure the following are installed:

* Python 3.10 or higher
* Neo4j Aura or Neo4j Desktop
* Neo4j Movies dataset
* Ollama
* Mistral model

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Bhoomikakm04/RAG-Based-QA-with-Neo4j-Movie-Knowledge-Graph.git
```

Move into the project directory:

```bash
cd RAG-Based-QA-with-Neo4j-Movie-Knowledge-Graph
```

---

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Neo4j Configuration

Create a `.env` file in the project root.

Use `.env.example` as the template.

Example:

```env
NEO4J_URI=bolt://your-neo4j-host:7687
NEO4J_USERNAME=your-username
NEO4J_PASSWORD=your-password
```

Replace the placeholder values with your own Neo4j credentials.

**Do not upload `.env` to GitHub.**

The project uses environment variables so that database credentials are kept separate from the source code.

---

## Ollama Configuration

Make sure Ollama is installed and running.

Check the available models:

```bash
ollama list
```

If Mistral is not available, download it:

```bash
ollama pull mistral
```

Test the model:

```bash
ollama run mistral
```

---

## Run the Application

Activate the virtual environment first:

```powershell
.venv\Scripts\Activate.ps1
```

Then start Streamlit:

```bash
streamlit run app.py
```

The application will open in your browser.

Usually it will be available at:

```text
http://localhost:8501
```

---

## Example Workflow

A typical question-answering workflow looks like this:

### User Question

```text
Which movies did Tom Hanks act in?
```

### Query Processing

The question is mapped to an appropriate Cypher query.

### Neo4j Retrieval

Relevant movie and actor information is retrieved from the knowledge graph.

### Graph Context

The retrieved facts are converted into context for the language model.

### Mistral Generation

Mistral receives the retrieved context and generates a natural-language response.

### Final Answer

The user receives an answer grounded in the retrieved Neo4j information.

---

## Security

Never commit database credentials to GitHub.

The following file should remain local:

```text
.env
```

The repository contains:

```text
.env.example
```

as a template for configuring the application.

---

## Assignment Mapping

| Expected Outcome                     | Implementation                 |
| ------------------------------------ | ------------------------------ |
| Load and use Neo4j movie graph       | `database/neo4j_connection.py` |
| Convert questions into graph queries | `rag/question_processor.py`    |
| Execute Cypher queries               | `database/cypher_queries.py`   |
| Retrieve movie/person information    | Neo4j read-only queries        |
| Construct retrieved context          | RAG pipeline                   |
| Generate natural-language answers    | Mistral through Ollama         |
| Explore graph relationships          | Graph Explorer                 |
| Evaluate QA workflow                 | Evaluation module              |
| Provide interactive interface        | Streamlit                      |

---

## RAG Pipeline

The core RAG process can be summarized as:

```text
        ┌─────────────────┐
        │  User Question  │
        └────────┬────────┘
                 ↓
        ┌─────────────────┐
        │    Question     │
        │   Processing    │
        └────────┬────────┘
                 ↓
        ┌─────────────────┐
        │  Cypher Query   │
        └────────┬────────┘
                 ↓
        ┌─────────────────┐
        │      Neo4j      │
        │ Knowledge Graph │
        └────────┬────────┘
                 ↓
        ┌─────────────────┐
        │  Graph Context  │
        └────────┬────────┘
                 ↓
        ┌─────────────────┐
        │ Mistral via     │
        │     Ollama      │
        └────────┬────────┘
                 ↓
        ┌─────────────────┐
        │ Grounded Answer │
        └─────────────────┘
```

---

## Future Enhancements

Possible extensions include:

* More natural-language query types
* Advanced graph visualization
* Larger movie knowledge graphs
* Semantic retrieval using embeddings
* Hybrid graph + vector retrieval
* Improved evaluation metrics
* Multi-turn conversational QA
* Additional LLM models

---

## Author

**Bhoomika K M**

GitHub: `Bhoomikakm04`

---

## License

This project is developed for educational and academic purposes.

```

### One important correction

Your old README says **"Mistral Large Language Model"** only indirectly and calls this a "small RAG application." The new version makes the actual architecture much clearer without claiming capabilities your project doesn't have.

Also, **don't put your real `.env` in the repository**. Keep `.env.example` in GitHub and `.env` in `.gitignore`.
```
