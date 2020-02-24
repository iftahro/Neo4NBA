import os
from neo4j import GraphDatabase

from source.config import NEO4J_USERNAME, NEO4J_BOLT_ADDRESS, NEO4J_PASSWORD, SHOULD_COPY_FILES_TO_SERVER, \
    NEO4J_IMPORT_DIRECTORY
from source.neo4nba_hosted_service import Neo4NBAHostedService
from source.utils import configure_logging, copy_files_to_neo4j_server


def main():
    configure_logging()

    # Copies all files that the graph is based on (from 'graph_files' folder) to local neo4j server
    if SHOULD_COPY_FILES_TO_SERVER:
        src = os.path.dirname(__file__).replace("source", "graph_files")
        copy_files_to_neo4j_server(src, NEO4J_IMPORT_DIRECTORY)

    neo4j_driver = GraphDatabase.driver(NEO4J_BOLT_ADDRESS, auth=(NEO4J_USERNAME, NEO4J_PASSWORD), encrypted=False)

    hosted_service = Neo4NBAHostedService()
    hosted_service.run(neo4j_driver)


if __name__ == "__main__":
    main()
