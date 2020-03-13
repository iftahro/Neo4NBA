from source.core_objects.graph_updater import GraphUpdater

ADD_AWARD_PROPERTY = """
MATCH (m:Award)<-[w:WON]-(a)
WHERE a:Coach OR a:Player
WITH toLower(m.short) AS award, w, a
WITH replace(award," ","_") AS award_name, w, a
ORDER BY w.year
WITH COLLECT(w.year) AS v, award_name, a
CALL apoc.create.setProperty([a], award_name, v) YIELD node
RETURN node
"""

ADD_AWARD_LABEL = """
MATCH (p:Player)-[:WON]->(a:Award)
CALL apoc.create.addLabels([p], [a.short]) yield node RETURN NULL
"""

award_properties_graph_updater = GraphUpdater("award properties", [
    ADD_AWARD_PROPERTY,
    ADD_AWARD_LABEL
])
