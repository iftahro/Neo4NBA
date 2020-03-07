from source.constants import SUPPORTED_YEARS, EXCEPTIONAL_YEAR_GAMES
from source.core_objects.graph_updater import GraphUpdater

CREATE_PLAYOFF_GAMES = """
LOAD CSV WITH HEADERS FROM "file:///games/{year}_games.csv" AS row
WITH row SKIP {games}
MATCH (r1:Roster{{year:{year}}}), (r2:Roster{{year:{year}}})
WHERE toUpper(r1.team) = row.home_team AND toUpper(r2.team) = row.away_team
MATCH (r1)--(s:Series:Playoff)--(r2)

WITH date(row.start_time) AS date, row, r1, r2, s
MERGE (g:Game:Playoff{{date:date, away_team:r2.team, home_team:r1.team,
away_team_score:toInteger(row.away_team_score) ,home_team_score:toInteger(row.home_team_score)}})
MERGE (g)-[:OF_SERIES]->(s)
SET g.final_score = g.home_team_score + '-' + g.away_team_score
"""

ADD_PLAYOFF_GAME_WINNER = """
MATCH (g:Game:Playoff)
CALL apoc.do.when(g.home_team_score > g.away_team_score,
'SET g.winner = g.home_team, g.loser = g.away_team',
'SET g.winner = g.away_team, g.loser = g.home_team',
{g:g}) YIELD value RETURN NULL
"""

queries = []

for year in SUPPORTED_YEARS:
    if year in EXCEPTIONAL_YEAR_GAMES.keys():
        queries.append(CREATE_PLAYOFF_GAMES.format(year=year, games=EXCEPTIONAL_YEAR_GAMES[year]))
    else:
        queries.append(CREATE_PLAYOFF_GAMES.format(year=year, games=1230))
queries.append(ADD_PLAYOFF_GAME_WINNER)

playoff_game_graph_updater = GraphUpdater("playoff game", queries)
