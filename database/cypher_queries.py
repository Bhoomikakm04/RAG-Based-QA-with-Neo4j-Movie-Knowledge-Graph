# Read-only Cypher templates for the standard Neo4j Movies dataset.
# Parameters are used instead of string interpolation.

TEMPLATES = {
    "movies_by_actor": """
        MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
        WHERE toLower(p.name) = toLower($person)
        RETURN m.title AS movie, m.released AS released
        ORDER BY released, movie
    """,

    "movies_by_director": """
        MATCH (p:Person)-[:DIRECTED]->(m:Movie)
        WHERE toLower(p.name) = toLower($person)
        RETURN m.title AS movie, m.released AS released
        ORDER BY released, movie
    """,

    "actors_in_movie": """
        MATCH (m:Movie)-[:ACTED_IN]-(p:Person)
        WHERE toLower(m.title) = toLower($movie)
        RETURN p.name AS actor
        ORDER BY actor
    """,

    "director_of_movie": """
        MATCH (m:Movie)<-[:DIRECTED]-(p:Person)
        WHERE toLower(m.title) = toLower($movie)
        RETURN p.name AS director
        ORDER BY director
    """,

    "co_actors": """
        MATCH (p1:Person)-[:ACTED_IN]->(m:Movie)<-[:ACTED_IN]-(p2:Person)
        WHERE toLower(p1.name) = toLower($person)
          AND p1 <> p2
        RETURN DISTINCT p2.name AS person, m.title AS movie
        ORDER BY person, movie
    """,

    "movies_after_year": """
        MATCH (m:Movie)
        WHERE m.released >= $year
        RETURN m.title AS movie, m.released AS released
        ORDER BY released, movie
    """,

    "movie_details": """
        MATCH (m:Movie)
        WHERE toLower(m.title) = toLower($movie)
        OPTIONAL MATCH (director:Person)-[:DIRECTED]->(m)
        OPTIONAL MATCH (actor:Person)-[:ACTED_IN]->(m)
        RETURN m.title AS movie,
               m.released AS released,
               m.tagline AS tagline,
               collect(DISTINCT director.name) AS directors,
               collect(DISTINCT actor.name) AS actors
    """,
}
