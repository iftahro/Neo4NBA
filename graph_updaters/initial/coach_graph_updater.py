from core_objects.graph_updater import GraphUpdater

CREATE_COACHES = """
LOAD CSV WITH HEADERS FROM "file:///coaches/{year}_coaches.csv" AS row
MATCH (roster:Roster{{year:{year}}})
WHERE row.team_label in LABELS(roster)
MERGE (c:Coach{{name:row.name}})
MERGE (c)-[r:COACHED]->(roster)

ON CREATE SET r = {{ 
games:toInteger(row.games),
wins:toInteger(row.wins),
losses:toInteger(row.losses)
}}

WITH r, toInteger((r.wins / toFloat(r.games) * 1000))/1000.0 as winning
SET r.`win%` = winning
"""

coaches_queries = []
for i in range(2010, 2021):
    coaches_queries.append(CREATE_COACHES.format(year=str(i)))

coaches_graph_updater = GraphUpdater("coaches_graph_updater", coaches_queries)
