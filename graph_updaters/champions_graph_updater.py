from core_objects.graph_updater_base import CsvGraphUpdater


class ChampionsGraphUpdater(CsvGraphUpdater):
    ADD_NBA_CHAMPIONS = """
    MERGE (t:Title:NBAChampions{{name:"NBA Champions"}})
    WITH t
    LOAD CSV WITH HEADERS FROM "file:///{file_name}" AS row
    WITH t, row, toInteger(row.year) AS year
    MATCH (winner:Roster{{team:row.winner, year:year}})
    CALL apoc.create.addLabels(winner,["NBAChampions"]) YIELD node AS b
    MATCH (loser:Roster{{team:row.opponent, year:year}})
    CALL apoc.create.addLabels([winner,loser],["ConferenceChampions"]) YIELD node AS y
    MERGE (winner)-[w:WON_TITLE]->(t)
    SET w = row
    REMOVE w.winner, w.year
    """

    B = """
    MATCH (r:Roster:NBAChampions)-[:OF_TEAM]->(t:Team)
    WITH COLLECT (r.year) as years, t
    CALL apoc.create.setProperty([t], "champions", years) YIELD node
    RETURN node
    """

    def update_graph(self, driver):
        with driver.session() as session:
            session.run(self.ADD_NBA_CHAMPIONS.format(file_name=self.file_name))
            session.run(self.B)
