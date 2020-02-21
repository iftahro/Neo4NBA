from core_objects.graph_updater import GraphUpdater

ADD_ROSTER_WINS_AND_LOSSES = """
MATCH (r:Roster)
MATCH (h:Coach)-[c:COACHED]->(r)
WITH r, sum(c.wins) AS wins, sum(c.losses) AS losses, COLLECT(h.name) AS coach
WITH r, wins, losses, coach, wins + losses AS games
CALL apoc.create.setProperties([r],["wins","losses","coach","games"],[wins,losses,coach,games]) YIELD node
RETURN node
"""

ADD_PLAYER_PROPERTIES = """
MATCH (p:Player)-[r:PLAYED_AT]->(l:Roster)
WITH p, COLLECT(DISTINCT r.position) AS player_positions, COLLECT(DISTINCT l.team) AS teams
CALL apoc.create.setProperties([p], ["position","teams_played"], [player_positions,teams]) YIELD node
RETURN node
"""

ADD_COACH_PROPERTIES = """
MATCH (c:Coach)-[l:COACHED]->(r:Roster)
WITH c, COLLECT (DISTINCT r.team) as teams, sum(l.wins) AS wins, sum(l.losses) AS losses
WITH c, teams, wins, losses, wins + losses as games
CALL apoc.create.setProperties([c],["teams_coached","total_games","total_wins","total_losses"],
[teams, games, wins, losses]) YIELD node RETURN node
"""

ADD_WINNING_PERCENTAGE = """
MATCH (r:{label})
WITH r, toInteger(toFloat(r.{wins}) / toFloat(r.{games}) * 1000)/1000.0 as winning
SET r.`{win_name}` = winning
"""

ADD_SEASONS_PLAYED = """
MATCH (p:Player)-[r:PLAYED_AT]->(:Roster)
WITH SIZE(COLLECT(DISTINCT r.year)) as s, p
SET p.seasons_played = s
"""

ADD_LOYALTY = """
MATCH (p:Player)-[l:PLAYED_AT]->(:Roster)
WHERE SIZE(p.teams_played) = 1 AND p.seasons_played >= 5
SET p:Loyal
"""

initial_properties_graph_updater = GraphUpdater("initial_properties_graph_updater", [
    ADD_ROSTER_WINS_AND_LOSSES,
    ADD_PLAYER_PROPERTIES,
    ADD_COACH_PROPERTIES,
    ADD_WINNING_PERCENTAGE.format(label="Coach", wins="total_wins", games="total_games", win_name="total_win%"),
    ADD_WINNING_PERCENTAGE.format(label="Roster", wins="wins", games="games", win_name="win%"),
    ADD_SEASONS_PLAYED,
    ADD_LOYALTY
])
