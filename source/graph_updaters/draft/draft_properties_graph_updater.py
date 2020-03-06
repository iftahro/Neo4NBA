from source.core_objects.graph_updater import GraphUpdater

ADD_UNDRAFTED = """
MATCH (p:Player)
WHERE NOT EXISTS(p.draft_pick)
SET p:Undrafted
"""

ADD_PICK_LABEL = """
MATCH (p:Player)
WHERE p.draft_pick = {pick}
SET p:{label}Pick
"""

draft_properties_graph_updater = GraphUpdater("draft_properties", [
    ADD_UNDRAFTED,
    ADD_PICK_LABEL.format(pick=1, label='First'),
    ADD_PICK_LABEL.format(pick=2, label='Second'),
    ADD_PICK_LABEL.format(pick=3, label='Third'),
])
