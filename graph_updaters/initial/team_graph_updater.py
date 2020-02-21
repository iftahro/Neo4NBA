from core_objects.graph_updater import GraphUpdater

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

team_graph_updater = GraphUpdater("team_graph_updater", [
    CREATE_NBA_TEAMS,
    ADD_ADDITIONAL_LABELS.format(short="'BKN'", labels=['NJN', 'BRK']),
    ADD_ADDITIONAL_LABELS.format(short="'NOP'", labels=['NOH']),
    ADD_ADDITIONAL_LABELS.format(short="'PHX'", labels=['PHO']),
    ADD_ADDITIONAL_LABELS.format(short="'CHA'", labels=['CHO'])
])
