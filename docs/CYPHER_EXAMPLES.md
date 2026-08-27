# Cypher Examples

## Movies by actor

```cypher
MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
WHERE toLower(p.name) = toLower($person)
RETURN m.title AS movie, m.released AS released
ORDER BY released, movie
```

## Actors in a movie

```cypher
MATCH (m:Movie)-[:ACTED_IN]-(p:Person)
WHERE toLower(m.title) = toLower($movie)
RETURN p.name AS actor
ORDER BY actor
```

## Director of a movie

```cypher
MATCH (m:Movie)<-[:DIRECTED]-(p:Person)
WHERE toLower(m.title) = toLower($movie)
RETURN p.name AS director
```

## Co-actors

```cypher
MATCH (p1:Person)-[:ACTED_IN]->(m:Movie)<-[:ACTED_IN]-(p2:Person)
WHERE toLower(p1.name) = toLower($person)
  AND p1 <> p2
RETURN DISTINCT p2.name AS person, m.title AS movie
ORDER BY person, movie
```
