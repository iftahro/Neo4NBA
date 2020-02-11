from constants import NBA_AWARDS
from core_objects.graph_updater_base import CsvGraphUpdater
import re


class AwardGraphUpdater(CsvGraphUpdater):
    ADD_AWARD = """
    MERGE (a:Award:{award_name}{{name:"{name}", short:"{short}"}})
    WITH a
    LOAD CSV WITH HEADERS FROM "file:///{file_name}" AS row
    MATCH (p:Player{{name:row.name}})
    WITH SPLIT(p.birth_date, " ")[2] AS birth_year, p, row, a
    WITH toInteger(row.year) - toInteger(birth_year) AS result, p, row, a
    WHERE result > 15
    MERGE (p)-[w:WON_AWARD {{year:row.year}}]->(a)
    ON CREATE SET w = row
    REMOVE w.name
    """

    ADD_AWARD_PROPERTY_TO_PLAYERS = """
    MATCH (m:Award)<-[w:WON_AWARD]-(p:Player)
    WITH toLower(m.name) AS award, w,p
    WITH replace(award," ","_") AS award_name,w,p
    ORDER BY w.year
    WITH COLLECT(w.year) AS v, award_name,p
    CALL apoc.create.setProperty([p], award_name, v) YIELD node
    RETURN node
    """

    def __init__(self, award_name):
        file_name = f"{award_name}.csv"
        super().__init__(file_name)
        self.award_name = award_name
        self.beautify_name = " ".join(re.findall('[A-Z][^A-Z]*', NBA_AWARDS[award_name]))

    def update_graph(self, driver):
        with driver.session() as session:
            session.run(self.ADD_AWARD.format(award_name=NBA_AWARDS[self.award_name], file_name=self.file_name,
                                              name=self.beautify_name,
                                              short=self.award_name.upper() if self.award_name != "finals_mvp" else "FMVP"))

            session.run(self.ADD_AWARD_PROPERTY_TO_PLAYERS)
