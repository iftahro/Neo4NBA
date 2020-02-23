from constants import YEARS_SUPPORTED
from core_objects.graph_updater import GraphUpdater

CREATE_PLAYERS_AND_ROSTERS = """
LOAD CSV WITH HEADERS FROM "file:///players/{year}_players.csv" AS row
WITH row, toInteger("{year}") as year
WHERE NOT row.Tm = "TOT"
MATCH (t:Team)
WHERE row.Tm IN LABELS(t)
MERGE (r:Roster{{team:t.name, year:year}})-[:OF_TEAM]->(t)
MERGE (p:Player{{name:row.Player}})
MERGE (p)-[m:PLAYED_AT]->(r)

// Player regular season stats 
ON CREATE SET m = {{ position: row.Pos, age: toInteger(row.Age), games:toInteger(row.G), year:year, 
games_started:toInteger(row.GS), minutes:toFloat(row.MP),  points:toFloat(row.PTS),  assists:toFloat(row.AST), 
rebounds:toFloat(row.TRB),  steals:toFloat(row.STL),  blocks:toFloat(row.BLK),  `ft%`:toFloat(row.FTP), 
`fg%`:toFloat(row.FGP),  `2p%`:toFloat(row.`2PP`),  `3p%`:toFloat(row.`3PP`) }}

WITH row, r, t
CALL apoc.create.addLabels(r, [row.Tm, t.short]) YIELD node
RETURN node
"""

players_queries = []
for year in YEARS_SUPPORTED:
    players_queries.append(CREATE_PLAYERS_AND_ROSTERS.format(year=str(year)))

player_graph_updater = GraphUpdater("player_graph_updater",
                                    players_queries)
