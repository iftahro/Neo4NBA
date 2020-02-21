from core_objects.graph_updater import GraphUpdater

ADD_CHAMPIONS_LABEL = """
MATCH (r:Roster)-[:WON_SERIES]->(:Series:Playoffs{name: "NBA Finals"})
SET r:NBAChampions
"""

ADD_TEAM_CHAMPIONS = """
MATCH (r:Roster:NBAChampions)-[:OF_TEAM]->(t:Team)
WITH COLLECT(r.year) AS years, t
SET t.championships=years
"""

ADD_PLAYER_COACH_CHAMPIONS = """
MATCH (r:Roster:NBAChampions)<-[]-(a)
WHERE a:Coach OR a:Player
WITH a, COLLECT(r.year) AS years
SET a.championships = years
"""

champions_graph_updater = GraphUpdater("champions_graph_updater", [
    ADD_CHAMPIONS_LABEL,
    ADD_TEAM_CHAMPIONS,
    ADD_PLAYER_COACH_CHAMPIONS
])
