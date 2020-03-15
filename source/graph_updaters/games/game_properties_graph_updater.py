from source.core_objects.graph_updater import GraphUpdater

SET_GAMES_TEAM_LABEL = """
MATCH (r:Roster)--(g:Games)
WITH LABELS(r) as l, g
UNWIND l as v
WITH v, g
WHERE SIZE(v) = 3
CALL apoc.create.addLabels([g], [v]) yield node RETURN NULL
"""

SET_GAME_WINNER_AND_FINAL_SCORE = """
MATCH (r1)-[:WON]->(g:Game)<-[:LOST]-(r2)
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

ADD_PLAYOFF_GAME_NUMBER = """
MATCH (p:Playoff:Series)
WITH p
MATCH (p)<-[:OF_SERIES]-(g:Game:Playoff)
WITH p, g
ORDER BY g.date
WITH COLLECT(g) AS games, p
UNWIND games AS game
WITH apoc.coll.indexOf(games, game) + 1 as number, game, p
SET game.game_number = number
"""

ADD_PLAYOFF_SERIES_DATE = """
MATCH (s:Playoff:Series)<-[:OF_SERIES]-(g:Game:Playoff)
WITH g, s ORDER BY g.game_number
WITH COLLECT(g) AS games, s
WITH games[0] AS p, games[-1] AS pp, s
SET s.date =  p.date.day + '.' + p.date.month + '-' + pp.date.day + '.' + pp.date.month, s.year = p.date.year
"""

game_properties_graph_updater = GraphUpdater("game properties", [
    SET_GAMES_TEAM_LABEL,
    SET_GAME_WINNER_AND_FINAL_SCORE,
    ADD_GAMES_WINS_LOSSES.format(relation='WON', prop='wins'),
    ADD_GAMES_WINS_LOSSES.format(relation='LOST', prop='losses'),
    ADD_GAMES_FINAL_SCORE,
    ADD_GAMES_WIN_PERCENTAGE,
    ADD_ROSTER_HOME_ROAD_STATS.format(game_label='Road', game_type='road'),
    ADD_ROSTER_HOME_ROAD_STATS.format(game_label='Home', game_type='home'),
    ADD_ROSTER_CHARACTER.format(prop='home_win%', min='0.85', character='HomeGuards'),
    ADD_ROSTER_CHARACTER.format(prop='road_win%', min='0.7', character='RoadHunters'),
    ADD_PLAYOFF_GAME_NUMBER,
    ADD_PLAYOFF_SERIES_DATE
])
