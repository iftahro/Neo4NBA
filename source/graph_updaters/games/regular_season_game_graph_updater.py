from source.constants import SUPPORTED_YEARS, EXCEPTIONAL_YEAR_GAMES
from source.core_objects.graph_updater import GraphUpdater

CREATE_ALL_GAMES = """
LOAD CSV WITH HEADERS FROM "file:///games/{year}_games.csv" AS row
WITH row LIMIT {games}
WITH date(row.start_time) AS date, row
MERGE (g:Game:RegularSeason:New{{date:date, away_team:row.away_team, home_team:row.home_team,
away_team_score:toInteger(row.away_team_score) ,home_team_score:toInteger(row.home_team_score)}})
"""

CREATE_HOME_AWAY_GAMES = """
MATCH (n:Game:RegularSeason:New)
MATCH (home_team:Roster{{year:{year}}}), (away_team:Roster{{year:{year}}})
WHERE toLower(home_team.team) = toLower(n.home_team) AND toLower(away_team.team) = toLower(n.away_team)
SET n.home_team = home_team.team, n.away_team = away_team.team

WITH home_team, away_team, n
MERGE (home_team)-[:HOSTED]->(g1:Home:Games:RegularSeason{{team:home_team.team, year:home_team.year}})
MERGE (away_team)-[:VISITED]->(g2:Road:Games:RegularSeason{{team:away_team.team, year:away_team.year}})

WITH g1, g2, n
CALL apoc.do.when(n.home_team_score > n.away_team_score,
'MERGE (g1)-[:WON]->(n)<-[:LOST]-(g2)',
'MERGE (g1)-[:LOST]->(n)<-[:WON]-(g2)',
{{g1:g1, g2:g2, n:n}}) 
YIELD value AS v RETURN NULL
"""

DELETE_NEW_LABEL = """
MATCH (n:New)
REMOVE n:New
"""

queries = []

for year in SUPPORTED_YEARS:
    if year in EXCEPTIONAL_YEAR_GAMES.keys():
        queries.append(CREATE_ALL_GAMES.format(year=year, games=EXCEPTIONAL_YEAR_GAMES[year]))
    else:
        queries.append(CREATE_ALL_GAMES.format(year=year, games=1230))
    queries.append(CREATE_HOME_AWAY_GAMES.format(year=year))
    queries.append(DELETE_NEW_LABEL)

regular_season_game_graph_updater = GraphUpdater("regular season game", queries)
