from source.core_objects.graph_updater import GraphUpdater

SET_GAME_WINNER_AND_FINAL_SCORE = """
MATCH (r1)-[:WON_GAME]->(g:Game)<-[:LOST_GAME]-(r2)
SET g.winner = r1.team, g.loser = r2.team

WITH g, g.home_team_score + '-' + g.away_team_score AS final_score
SET g.final_score = final_score
"""

ADD_GAMES_WINS_LOSSES = """
MATCH (g:Games)-[w:{relation}]->(:Game)
WITH g, COUNT(w) AS result
SET g.{prop} = result
"""

ADD_GAMES_FINAL_SCORE = """
MATCH (g:Games)
WITH g, g.wins + '-' + g.losses AS record, g.wins + g.losses AS games
SET g.record = record, g.games = games
"""

ADD_GAMES_WIN_PERCENTAGE = """
MATCH (r:Games)
WITH r, r.wins + r.losses AS games
WITH r, toInteger(toFloat(r.wins) / toFloat(games) * 1000)/1000.0 as winning
SET r.`win%` = winning
"""

ADD_ROSTER_HOME_ROAD_STATS = """
MATCH (r:Roster)-[:HOSTED|:VISITED]->(g:Games:{game_label})
SET r.`{game_type}_win%` = g.`win%`, r.{game_type}_record = g.record
"""

ADD_ROSTER_CHARACTER = """
MATCH (r:Roster)
WHERE EXISTS(r.`{prop}`) AND r.`{prop}` > {min}
SET r:{character}
"""

game_properties_graph_updater = GraphUpdater("game_properties_graph_updater", [
    SET_GAME_WINNER_AND_FINAL_SCORE,
    ADD_GAMES_WINS_LOSSES.format(relation='WON_GAME', prop='wins'),
    ADD_GAMES_WINS_LOSSES.format(relation='LOST_GAME', prop='losses'),
    ADD_GAMES_FINAL_SCORE,
    ADD_GAMES_WIN_PERCENTAGE,
    ADD_ROSTER_HOME_ROAD_STATS.format(game_label='Road', game_type='road'),
    ADD_ROSTER_HOME_ROAD_STATS.format(game_label='Home', game_type='home'),
    ADD_ROSTER_CHARACTER.format(prop='home_win%', min='0.85', character='Watchdogs'),
    ADD_ROSTER_CHARACTER.format(prop='road_win%', min='0.7', character='RoadHunters')
])
