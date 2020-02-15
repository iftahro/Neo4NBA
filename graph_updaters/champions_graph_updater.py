from core_objects.graph_updater import GraphUpdater

ADD_NBA_CHAMPIONS = """
MERGE (t:Title{name:"NBA Champions"})
WITH t
LOAD CSV WITH HEADERS FROM "file:///nba_champions.csv" AS row
WITH t, row, toInteger(row.year) AS year
MATCH (winner:Roster{team:row.winner, year:year})
CALL apoc.create.addLabels(winner,["NBAChampions"]) YIELD node AS b
MATCH (loser:Roster{team:row.opponent, year:year})
CALL apoc.create.addLabels([winner,loser],["ConferenceChampions"]) YIELD node AS y
MERGE (winner)-[w:WON_TITLE]->(t)
SET w = row
REMOVE w.winner, w.year
"""

ADD_CHAMPIONS_PROPERTY = """
MATCH (r:Roster:NBAChampions)-[:OF_TEAM]->(t:Team)
WITH COLLECT (r.year) as years, t
CALL apoc.create.setProperty([t], "champions", years) YIELD node
RETURN node
"""

champions_graph_updater = GraphUpdater([
    ADD_NBA_CHAMPIONS,
    ADD_CHAMPIONS_PROPERTY
])
