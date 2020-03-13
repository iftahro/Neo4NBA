from source.core_objects.graph_updater import GraphUpdater

ADD_PLAYOFF_SERIES = """
LOAD CSV WITH HEADERS FROM "file:///playoff_series.csv" AS row
WITH substring(row.Winner, 0, SIZE(row.Winner) - 4) AS winner, substring(row.Loser, 0, SIZE(row.Loser) - 4) AS loser, 
toInteger(row.Yr) AS year ,row
MATCH (w:Roster{year:year, team:winner})
MATCH (l:Roster{year:year, team:loser})

MERGE (w)-[a:WON_SERIES]->(s:Series:Playoff{round:row.Series})<-[b:LOST_SERIES]-(l)
ON CREATE SET s += {
date:row.Date,
winner:winner,
loser:loser,
conference:row.Conference},
a.opponent = loser, b.opponent = winner

WITH s, row, a, b 
SET a.wins = toInteger(row.Wins), a.losses = toInteger(row.Losses),
b.wins = toInteger(row.Losses), b.losses = toInteger(row.Wins)

WITH s,row, a
CALL apoc.create.addLabels([s],[row.Conference]) YIELD node AS ser
SET s.games= a.wins + a.losses
"""

ADD_FINAL_SCORE = """
MATCH (s:Series:Playoff)<-[r:WON_SERIES]-(:Roster)
WITH toString(r.wins) + "-" + toString(r.losses) AS games, s
SET s.final_score = games
"""

ADD_IS_SWEEP = """
MATCH (s:Series:Playoff)

CALL apoc.do.when(s.games = 4,
'SET s.is_sweep=true, s:Sweep',
'SET s.is_sweep=false',{s:s}) YIELD value
RETURN value
"""

playoff_series_graph_updater = GraphUpdater("playoff series", [
    ADD_PLAYOFF_SERIES,
    ADD_FINAL_SCORE,
    ADD_IS_SWEEP
])
