from source.core_objects.graph_updater import GraphUpdater

ADD_AWARD_PROPERTY = """
MATCH (m:Award)<-[w:WON]-(a)
WHERE a:Coach OR a:Player
WITH toLower(m.short) AS award, w, a
WITH replace(award," ","_") AS award_name, w, a
ORDER BY w.year
WITH COLLECT(w.year) AS v, award_name, a
CALL apoc.do.when(SIZE(v) > 1,
'CALL apoc.create.setProperty([a], award_name, v) YIELD node RETURN NULL',
'CALL apoc.create.setProperty([a], award_name, v[0]) YIELD node RETURN NULL',
{a:a, award_name:award_name, v:v}) YIELD value RETURN NULL
"""

award_properties_graph_updater = GraphUpdater("award properties", [
    ADD_AWARD_PROPERTY
])
