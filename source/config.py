import os

# Neo4j driver
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "Neo4j$"
NEO4J_BOLT_ADDRESS = "bolt://localhost:7687"

# Setup
GRAPH_FILES_DIRECTORY_PATH = os.path.dirname(__file__).replace("source", "graph_files")
NEO4J_IMPORT_DIRECTORY = r"D:\Programming\neo4j-community-4.0.0\import"
SHOULD_COPY_FILES_TO_SERVER = False

LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
