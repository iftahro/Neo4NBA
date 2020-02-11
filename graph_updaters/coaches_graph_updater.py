from core_objects.graph_updater_base import CsvGraphUpdater


class CoachesGraphUpdater(CsvGraphUpdater):
    CREATE_COACHES = """
    LOAD CSV WITH HEADERS FROM "file:///{file_name}" AS row
    MATCH (roster:Roster:`{year}`)
    WHERE row.team_label in LABELS(roster)
    MERGE (c:Coach{{name:row.name}})
    MERGE (c)-[r:COACHED]->(roster)
    ON CREATE SET r = {{ games: row.games, wins: row.wins, losses: row.losses}}
    """

    def __init__(self, year):
        file_name = f"{year}_coaches.csv"
        super().__init__(file_name)
        self.year = year

    def update_graph(self, driver):
        with driver.session() as session:
            session.run(self.CREATE_COACHES.format(file_name=self.file_name, year=self.year))
