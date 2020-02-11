from core_objects.graph_updater_base import CsvGraphUpdater


class DivisionGraphUpdater(CsvGraphUpdater):
    ADD_DIVISIONS_AND_CONFERENCES = """
    LOAD CSV WITH HEADERS FROM "file:///{file_name}" AS row
    MERGE (c:Conference{{name:row.conference}})
    MERGE (d:Division{{name:row.division}})-[:FROM_CONFERENCE]->(c)
    
    WITH row, c, d
    MATCH (t:Team{{name:row.name}})
    MERGE (t)-[:FROM_DIVISION]->(d)
    
    WITH row, c, d, t
    CALL apoc.create.addLabels([d],[row.division]) YIELD node AS l
    CALL apoc.create.addLabels([t,d,c],[row.conference]) YIELD node AS m
    CALL apoc.create.setProperty([t,d], "conference", [row.conference]) YIELD node AS n
    CALL apoc.create.setProperty([t], "division", [row.division]) YIELD node AS o
    RETURN o  
    """

    def update_graph(self, driver):
        with driver.session() as session:
            session.run(self.ADD_DIVISIONS_AND_CONFERENCES.format(file_name=self.file_name))
