from source.core_objects.graph_updater import GraphUpdater

ADD_CHAMPIONS_LABEL = """
MATCH (r:Roster)-[:WON]->(:Series:Playoff{round: "NBA Finals"})
SET r:Champions
"""

ADD_TEAM_CHAMPIONS = """
MATCH (r:Roster:Champions)-[:OF_TEAM]->(t:Team)
WITH COLLECT(r.year) AS years, t
SET t.titles=years
"""

ADD_PLAYER_COACH_CHAMPIONS = """
MATCH (r:Roster:Champions)<-[]-(a)
WHERE a:Coach OR a:Player
WITH a, COLLECT(r.year) AS years
SET a.titles = years
"""

champion_graph_updater = GraphUpdater("champion", [
    ADD_CHAMPIONS_LABEL,
    ADD_TEAM_CHAMPIONS,
    ADD_PLAYER_COACH_CHAMPIONS
])
