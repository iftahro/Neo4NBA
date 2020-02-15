from core_objects.graph_updater import GraphUpdater

ADD_DIVISIONS = """
LOAD CSV WITH HEADERS FROM "file:///divisions.csv" AS row
MERGE (c:Conference{name:row.conference})
MERGE (d:Division{name:row.division})-[:FROM_CONFERENCE]->(c)

WITH row, c, d
MATCH (t:Team{name:row.name})
MERGE (t)-[:FROM_DIVISION]->(d)

WITH row, c, d, t
CALL apoc.create.addLabels([t,d,c],[row.conference]) YIELD node AS m
CALL apoc.create.setProperty([t,d], "conference", [row.conference]) YIELD node AS n
CALL apoc.create.setProperty([t], "division", [row.division]) YIELD node AS o
RETURN o  
"""

division_graph_updater = GraphUpdater([
    ADD_DIVISIONS
])
