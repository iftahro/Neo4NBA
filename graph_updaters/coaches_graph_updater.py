from core_objects.graph_updater import GraphUpdater

CREATE_COACHES = """
LOAD CSV WITH HEADERS FROM "file:///{year}_coaches.csv" AS row
MATCH (roster:Roster:`{year}`)
WHERE row.team_label in LABELS(roster)
MERGE (c:Coach{{name:row.name}})
MERGE (c)-[r:COACHED]->(roster)
ON CREATE SET r = {{ games: row.games, wins: row.wins, losses: row.losses}}
"""

coaches_graph_updater = GraphUpdater([
    CREATE_COACHES.format(year="2015"),
    CREATE_COACHES.format(year="2016"),
    CREATE_COACHES.format(year="2017"),
    CREATE_COACHES.format(year="2018"),
    CREATE_COACHES.format(year="2019"),
    CREATE_COACHES.format(year="2020")
])
