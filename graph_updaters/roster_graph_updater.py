from core_objects.graph_updater import GraphUpdater

CREATE_ROSTERS_BY_PLAYERS = """
LOAD CSV WITH HEADERS FROM "file:///{file_name}.csv" AS row
WITH row, toInteger(row.Year) as year
WHERE NOT row.Tm = "TOT"
MATCH (t:Team)
WHERE row.Tm IN LABELS(t)
MERGE (r:Roster{{team:t.name, year:year}})-[:OF_TEAM]->(t)
MERGE (p:Player{{name:row.Player}})
MERGE (p)-[m:PLAYED_AT]->(r)

// Player regular season stats 
ON CREATE SET m = {{ position: row.Pos, age: toInteger(row.Age), games:toInteger(row.G), 
games_started:toInteger(row.GS), minutes:toFloat(row.MP),  points:toFloat(row.PTS),  assists:toFloat(row.AST), 
rebounds:toFloat(row.TRB),  steals:toFloat(row.STL),  blocks:toFloat(row.BLK),  `ft%`:toFloat(row.FTP), 
`fg%`:toFloat(row.FGP),  `2p%`:toFloat(row.`2PP`),  `3p%`:toFloat(row.`3PP`) }}

WITH row, r, t
CALL apoc.create.addLabels(r, [row.Tm, t.short]) YIELD node
RETURN node
"""

roster_creator_graph_updater = GraphUpdater([
    CREATE_ROSTERS_BY_PLAYERS.format(file_name="2010_2016_players"),
    CREATE_ROSTERS_BY_PLAYERS.format(file_name="2018_players"),
    CREATE_ROSTERS_BY_PLAYERS.format(file_name="2019_players")
])
