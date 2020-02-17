from neo4j import GraphDatabase
from config import NEO4J_USERNAME, NEO4J_BOLT_CONNECTION, NEO4J_PASSWORD
from graph_updaters.coach_graph_updater import coaches_graph_updater
from graph_updaters.division_graph_updater import division_graph_updater
from graph_updaters.object_properties_graph_updater import object_properties_graph_updater
from graph_updaters.roster_graph_updater import roster_creator_graph_updater
from graph_updaters.team_graph_updater import team_graph_updater
from hosted_service import HostedService
from storylines.basic_storyline import BasicStoryline


def main():
    neo4j_driver = GraphDatabase.driver(NEO4J_BOLT_CONNECTION, auth=(NEO4J_USERNAME, NEO4J_PASSWORD), encrypted=False)

    # Starts the program
    hosted_service = HostedService([
        BasicStoryline(team_graph_updater),
        BasicStoryline(division_graph_updater),
        BasicStoryline(roster_creator_graph_updater),
        BasicStoryline(coaches_graph_updater),
        BasicStoryline(object_properties_graph_updater)
    ])
    hosted_service.run(neo4j_driver)


if __name__ == "__main__":
    main()
