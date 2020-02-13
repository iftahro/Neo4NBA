from constants import PERSONAL_AWARDS
from core_objects.graph_updater import GraphUpdater

ADD_AWARD = """
MERGE (a:Award{{name:"{name}", short:"{short}"}})
WITH a
LOAD CSV WITH HEADERS FROM "file:///{short}.csv" AS row
MATCH (p:Player{{name:row.name}})
WITH SPLIT(p.birth_date, " ")[2] AS birth_year, p, row, a
WITH toInteger(row.year) - toInteger(birth_year) AS result, p, row, a
WHERE result > 15
MERGE (p)-[w:WON_AWARD {{year:row.year}}]->(a)
ON CREATE SET w = row
REMOVE w.name
"""

ADD_AWARD_PROPERTY_TO_PLAYERS = """
MATCH (m:Award)<-[w:WON_AWARD]-(p:Player)
WITH toLower(m.name) AS award, w,p
WITH replace(award," ","_") AS award_name,w,p
ORDER BY w.year
WITH COLLECT(w.year) AS v, award_name,p
CALL apoc.create.setProperty([p], award_name, v) YIELD node
RETURN node
"""

award_graph_updater = GraphUpdater([
    ADD_AWARD.format(name=PERSONAL_AWARDS.keys()[0], short=PERSONAL_AWARDS[PERSONAL_AWARDS.keys()[0]]),
    ADD_AWARD.format(name=PERSONAL_AWARDS.keys()[1], short=PERSONAL_AWARDS[PERSONAL_AWARDS.keys()[1]]),
    ADD_AWARD.format(name=PERSONAL_AWARDS.keys()[2], short=PERSONAL_AWARDS[PERSONAL_AWARDS.keys()[2]]),
    ADD_AWARD.format(name=PERSONAL_AWARDS.keys()[3], short=PERSONAL_AWARDS[PERSONAL_AWARDS.keys()[3]]),
    ADD_AWARD.format(name=PERSONAL_AWARDS.keys()[4], short=PERSONAL_AWARDS[PERSONAL_AWARDS.keys()[4]])
])
