from core_objects.graph_updater import GraphUpdater

ADD_POSITION_PROPERTY = """
MATCH (p:Player)-[r:PLAYED_AT]->(:Roster)
WITH COLLECT(DISTINCT r.position) AS player_positions, p
CALL apoc.create.setProperty([p], "position", player_positions) YIELD node
RETURN node
"""

position_graph_updater = GraphUpdater([
    ADD_POSITION_PROPERTY
])
