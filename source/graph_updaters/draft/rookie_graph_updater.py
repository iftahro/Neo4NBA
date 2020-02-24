from source.constants import CURRENT_YEAR
from source.core_objects.graph_updater import GraphUpdater

ADD_ROOKIE_LABEL = """
MATCH (p:Player)-[r:PLAYED_AT]->(:Roster)
WHERE r.year = 2020 AND p.seasons_played = 1
SET p:Rookie
"""

rookie_graph_updater = GraphUpdater("rookie_graph_updater", [
    ADD_ROOKIE_LABEL.format(year=str(CURRENT_YEAR - 1))
])
