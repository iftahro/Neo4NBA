import os
from neo4j import GraphDatabase

from source.config import NEO4J_USERNAME, NEO4J_BOLT_ADDRESS, NEO4J_PASSWORD, SHOULD_COPY_FILES_TO_SERVER, \
    NEO4J_IMPORT_DIRECTORY, GRAPH_FILES_DIRECTORY_PATH
from source.neo4nba_hosted_service import Neo4NBAHostedService
from source.setup import configure_logging, copy_tree


def main():
    configure_logging()

    # Copies all files that the graph is based on (from 'graph_files' folder) to local neo4j server
    if SHOULD_COPY_FILES_TO_SERVER:
        copy_tree(GRAPH_FILES_DIRECTORY_PATH, NEO4J_IMPORT_DIRECTORY)

    neo4j_driver = GraphDatabase.driver(NEO4J_BOLT_ADDRESS, auth=(NEO4J_USERNAME, NEO4J_PASSWORD), encrypted=False)

    hosted_service = Neo4NBAHostedService()
    hosted_service.run(neo4j_driver)


if __name__ == "__main__":
    main()
