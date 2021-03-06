from source.core_objects.graph_updater import GraphUpdater

CREATE_DRAFT_PROPERTIES = """
MATCH (p:Player{{name:name}})
CALL apoc.create.setProperties([p],["draft_pick","draft_class","pre_draft_team"],
[toInteger(row.{pick}),toInteger({year}), row.Pre]) YIELD node
RETURN node
"""

ADD_OLD_DRAFTS = """
LOAD CSV WITH HEADERS FROM "file:///draft/1993_2017_drafts.csv" AS row
WITH SPLIT(row.player, ",") AS names, row
WITH names[1] + " " + names[0] AS name, row
""" + CREATE_DRAFT_PROPERTIES

ADD_SPECIFIC_DRAFT = """
LOAD CSV WITH HEADERS FROM "file:///draft/{year}_draft.csv" AS row
WITH row, row.Player as name
""" + CREATE_DRAFT_PROPERTIES

ADD_PRE_DRAFT_TEAM = """
MATCH (p:Player)
WHERE EXISTS(p.pre_draft_team)
MERGE (r:Team:PreDraft{name:p.pre_draft_team})
MERGE (p)-[:PLAYED_AT]->(r)
"""

draft_graph_updater = GraphUpdater("draft", [
    ADD_SPECIFIC_DRAFT.format(year="1992", pick="Pk"),
    ADD_OLD_DRAFTS.format(year="row.year", pick="pick"),
    ADD_SPECIFIC_DRAFT.format(year="2018", pick="Pk"),
    ADD_SPECIFIC_DRAFT.format(year="2019", pick="Pk"),
    ADD_PRE_DRAFT_TEAM
])
