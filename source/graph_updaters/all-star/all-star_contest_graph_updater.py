from source.core_objects.graph_updater import GraphUpdater

a = """
LOAD CSV WITH HEADERS FROM 'file:///allstar_contests.csv' AS row
MERGE (c:Contest:`All-Star`{name:row.Contest, year:toInteger(row.Year)})
ON CREATE SET c += {winner:row.Winner, participants:row.Others}
ON MATCH SET c.winner = c.winner + ',' + row.Winner, c.participants = row.Others

WITH c, row
MATCH (p:Player{name:row.Winner})
MERGE (p)-[:WON]->(c)
SET c.participants = c.winner + ',' + c.participants
"""

b = """
MATCH (n:Contest)
WITH SPLIT(n.participants, ',') AS participants, n
UNWIND participants AS participant

MATCH (p:Player{name:participant})
WHERE NOT EXISTS ((p)-[:WON]->(n))
MERGE (p)-[:PARTICIPATED]->(n)
"""

c = """
MATCH (n:Contest)
SET n.participants = n.winner + ',' + n.participants
"""

all_star_contest_graph_updater = GraphUpdater('all star contest', [a, b])
