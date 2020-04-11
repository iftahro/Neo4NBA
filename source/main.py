import logging
from neo4j import GraphDatabase

from source.utils import utils
from source.constants import LOG_LEVEL, GRAPH_FILES_DIRECTORY_PATH, LOGGING_FORMAT
from source.config import NEO4J_USERNAME, NEO4J_BOLT_ADDRESS, NEO4J_PASSWORD, SHOULD_COPY_FILES_TO_SERVER, \
    NEO4J_IMPORT_DIRECTORY, SHOULD_RESET_GRAPH
from source.neo4nba_service import Neo4NBAService


def main():
    utils.configure_logging(LOG_LEVEL, LOGGING_FORMAT)

    # Copies all files that the graph is based on to the local neo4j server
    if SHOULD_COPY_FILES_TO_SERVER:
        logging.info("Copying graph based files to local neo4j server")
        utils.copy_tree(GRAPH_FILES_DIRECTORY_PATH, NEO4J_IMPORT_DIRECTORY)

    neo4j_driver = GraphDatabase.driver(NEO4J_BOLT_ADDRESS, auth=(NEO4J_USERNAME, NEO4J_PASSWORD), encrypted=False)

    # Resets the neo4j db
    if SHOULD_RESET_GRAPH:
        logging.info("Resetting neo4j db (deleting all nodes and relations)")
        utils.reset_neo4j_db(neo4j_driver)

    neo4nba_service = Neo4NBAService()
    neo4nba_service.run(neo4j_driver)


if __name__ == "__main__":
    main()
