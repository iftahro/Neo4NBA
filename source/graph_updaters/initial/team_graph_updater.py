from source.constants import INVALID_TEAMS_LABELS
from source.core_objects.graph_updater import GraphUpdater

CREATE_NBA_TEAMS = """
LOAD CSV WITH HEADERS FROM "file:///teams.csv" AS row
WITH row, toInteger(row.MIN_YEAR) as year
MERGE (t:Team{name:row.FULLNAME})
ON CREATE SET t += {
short:row.ABBREVIATION, general_manager:row.GENERALMANAGER, owner:row.OWNER, 
arena:row.ARENA, year_founded:year, city:row.CITY }

WITH t, row.ABBREVIATION AS short
CALL apoc.create.addLabels(t, [short]) YIELD node
RETURN node
"""

ADD_ADDITIONAL_LABELS = """
MATCH (t:Team{{short:{short}}})
CALL apoc.create.addLabels(t,{labels}) YIELD node
RETURN node
"""

CREATE_DIVISIONS_AND_CONFERENCES = """
LOAD CSV WITH HEADERS FROM "file:///divisions.csv" AS row
MERGE (c:Conference{name:row.conference})
MERGE (d:Division{name:row.division})-[:FROM]->(c)

WITH row, c, d
MATCH (t:Team{name:row.name})
MERGE (t)-[:FROM]->(d)

WITH row, c, d, t
CALL apoc.create.addLabels([t,d,c],[row.conference]) YIELD node AS m
CALL apoc.create.setProperty([t,d], "conference", [row.conference]) YIELD node AS n
CALL apoc.create.setProperty([t], "division", [row.division]) YIELD node AS o
RETURN o  
"""

team_queries = [CREATE_NBA_TEAMS]
for team, labels in INVALID_TEAMS_LABELS.items():
    team_queries.append(ADD_ADDITIONAL_LABELS.format(short=team, labels=labels))
team_queries.append(CREATE_DIVISIONS_AND_CONFERENCES)

team_graph_updater = GraphUpdater("team", team_queries)
