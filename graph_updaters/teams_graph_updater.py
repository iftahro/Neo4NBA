from core_objects.graph_updater_base import CsvGraphUpdater


class TeamGraphUpdater(CsvGraphUpdater):
    CREATE_NBA_TEAMS = """
    LOAD CSV WITH HEADERS FROM "file:///{file_name}" AS row
    MERGE (t:Team{{name:row.full_name}})
    WITH t, row.short AS short
    CALL apoc.create.addLabels(t, [short]) YIELD node
    RETURN node
    """

    def __init__(self):
        file_name = "nba_teams.csv"
        super().__init__(file_name)

    def update_graph(self, driver):
        with driver.session() as session:
            session.run(self.CREATE_NBA_TEAMS.format(file_name=self.file_name))
