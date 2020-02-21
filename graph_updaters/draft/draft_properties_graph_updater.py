from core_objects.graph_updater import GraphUpdater

ADD_UNDRAFTED = """
MATCH (p:Player)
WHERE NOT EXISTS(p.draft_pick)
SET p:Undrafted
"""

ADD_FIRST_PICK = """
MATCH (p:Player)
WHERE p.draft_pick = 1
SET p:FirstPick
"""

draft_properties_graph_updater = GraphUpdater("draft_properties_graph_updater", [
    ADD_UNDRAFTED,
    ADD_FIRST_PICK
])
