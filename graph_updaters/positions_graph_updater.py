from constants import PLAYED_AT_RELATION_NAME
from core_objects.graph_updater_base import GraphUpdaterBase


class PositionsGraphUpdater(GraphUpdaterBase):
    ADD_POSITION_PROPERTY = """
    MATCH (p:Player)-[r:{relation_name}]->(:Roster)
    WITH COLLECT(DISTINCT r.position) AS player_positions, p
    CALL apoc.create.setProperty([p], "position", player_positions) YIELD node
    RETURN node
    """

    def update_graph(self, driver):
        with driver.session() as session:
            session.run(self.ADD_POSITION_PROPERTY.format(relation_name=PLAYED_AT_RELATION_NAME))
