from neo4j import GraphDatabase


class GraphUpdater:
    def __init__(self, queries):
        self.queries = queries

    def update_graph(self, driver: GraphDatabase.driver):
        with driver.session() as session:
            for query in self.queries:
                session.run(query)
