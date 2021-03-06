from source.constants import SUPPORTED_YEARS, CURRENT_YEAR
from source.core_objects.graph_updater import GraphUpdater

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
games_started:toInteger(row.GS), minutes:toFloat(row.MP), points:toFloat(row.PTS), assists:toFloat(row.AST), 
rebounds:toFloat(row.TRB), steals:toFloat(row.STL), blocks:toFloat(row.BLK), `ft%`:toFloat(row.FTP), 
`fg%`:toFloat(row.FGP), `2p%`:toFloat(row.`2PP`), `3p%`:toFloat(row.`3PP`) }}

WITH row, r, t
CALL apoc.create.addLabels(r, [row.Tm, t.short]) YIELD node
RETURN node
"""

ADD_PLAYER_CURRENT_AGE = """
MATCH (p:Player)-[r:PLAYED_AT{{year:{current_year}}}]->(:Roster)
SET p.age = r.age
"""

players_queries = []
for year in SUPPORTED_YEARS:
    players_queries.append(CREATE_PLAYERS_AND_ROSTERS.format(year=str(year)))
players_queries.append(ADD_PLAYER_CURRENT_AGE.format(current_year=CURRENT_YEAR))

player_graph_updater = GraphUpdater("player", players_queries)
