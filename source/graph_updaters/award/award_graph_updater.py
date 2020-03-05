from source.constants import PERSONAL_AWARDS
from source.core_objects.graph_updater import GraphUpdater

CREATE_PERSONAL_AWARDS = """
MERGE (a:Award{{name:"{name}", short:"{short}"}})
WITH a
LOAD CSV WITH HEADERS FROM "file:///award/{short}.csv" AS row
MATCH (p:Player{{name:row.Player}})
MERGE (p)-[w:WON_AWARD{{year:toInteger(row.Season)}}]->(a)

ON CREATE SET w += {{ games:toInteger(row.G), minutes:toFloat(row.MP),  points:toFloat(row.PTS),  
assists:toFloat(row.AST), rebounds:toFloat(row.TRB), steals:toFloat(row.STL), 
blocks:toFloat(row.BLK), `ft%`:toFloat(row.FTP), `fg%`:toFloat(row.FGP), `3p%`:toFloat(row.`3PP`) }}

WITH p,w
MATCH (p)-[l:PLAYED_AT]->(r:Roster{{year:w.year}})
SET w.age = l.age
"""

CREATE_COACH_AWARD = """
MERGE (a:Award{name:"Coach of the Year", short:"COY"})
WITH a
LOAD CSV WITH HEADERS FROM "file:///award/COY.csv" AS row
MATCH (c:Coach{name:row.Coach})
MERGE (c)-[w:WON_AWARD{year:toInteger(row.Season)}]->(a)

ON CREATE SET w += { games:toInteger(row.G), wins:toInteger(row.W), losses:toInteger(row.L), 
`win%`:toFloat(row.`W/LP`)}
"""

award_queries = []

for key, value in PERSONAL_AWARDS.items():
    award_queries.append(CREATE_PERSONAL_AWARDS.format(name=key, short=value))
award_queries.append(CREATE_COACH_AWARD)

award_graph_updater = GraphUpdater("award", award_queries)
