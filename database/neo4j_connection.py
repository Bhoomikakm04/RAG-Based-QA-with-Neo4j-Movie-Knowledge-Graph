from neo4j import GraphDatabase
from config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD

class Neo4jConnection:
    def __init__(self):
        if not NEO4J_URI or not NEO4J_PASSWORD:
            raise ValueError(
                "Neo4j credentials are missing. Create .env from .env.example."
            )
        self.driver = GraphDatabase.driver(
            NEO4J_URI,
            auth=(NEO4J_USERNAME, NEO4J_PASSWORD),
        )

    def verify_connection(self):
        with self.driver.session() as session:
            return session.run("RETURN 1 AS ok").single()["ok"] == 1

    def run_query(self, query, parameters=None):
        parameters = parameters or {}
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return [record.data() for record in result]

    def get_counts(self):
        query = """
        OPTIONAL MATCH (m:Movie)
        WITH count(m) AS movies
        OPTIONAL MATCH (p:Person)
        WITH movies, count(p) AS people
        OPTIONAL MATCH ()-[r]->()
        RETURN movies, people, count(r) AS relationships
        """
        rows = self.run_query(query)
        return rows[0] if rows else {"movies": 0, "people": 0, "relationships": 0}

    def get_schema(self):
        labels = self.run_query("CALL db.labels() YIELD label RETURN label ORDER BY label")
        rels = self.run_query(
            "CALL db.relationshipTypes() YIELD relationshipType "
            "RETURN relationshipType ORDER BY relationshipType"
        )
        return {
            "labels": [x["label"] for x in labels],
            "relationships": [x["relationshipType"] for x in rels],
        }

    def close(self):
        self.driver.close()
