from constants import PLAYED_AT_RELATION_NAME
from core_objects.graph_updater_base import CsvGraphUpdater


class RosterGraphUpdater(CsvGraphUpdater):
    LOAD_ROSTER = """
        MATCH (t:Team:{team_label})
        MERGE (r:Roster:{team_label}:`{year}`{{team:t.name, year:{year}}})-[:OF_TEAM]->(t)
        WITH r
        LOAD CSV WITH HEADERS FROM "file:///{file_name}" AS row
        MERGE (p:Player{{name:row.name, birth_date:row.birth_date}})
        MERGE (p)-[l:{relation_name}]->(r)
        SET l = {{ number: row.number, experience: row.experience, position: row.position }}
        SET p = {{ name: row.name, height: row.height,weight: row.weight,
         birth_date: row.birth_date, birth_country: row.birth_country, college: row.college }}
        """

    def __init__(self, team_label: str, year: str):
        file_name = f"{team_label}_{year}_roster.csv"
        super().__init__(file_name)
        self.team_label = team_label
        self.year = year

    def update_graph(self, driver):
        with driver.session() as session:
            session.run(self.LOAD_ROSTER.format(team_label=self.team_label, year=self.year, file_name=self.file_name,
                                                relation_name=PLAYED_AT_RELATION_NAME))
