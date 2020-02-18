from neo4j import GraphDatabase
from config import NEO4J_USERNAME, NEO4J_BOLT_CONNECTION, NEO4J_PASSWORD
from graph_updaters.coach_graph_updater import coaches_graph_updater
from graph_updaters.division_graph_updater import division_graph_updater
from graph_updaters.object_properties_graph_updater import object_properties_graph_updater
from graph_updaters.playoffs.nba_champions_graph_updater import nba_champions_graph_updater
from graph_updaters.playoffs.playoff_series_graph_updater import playoff_series_graph_updater
from graph_updaters.roster_graph_updater import roster_graph_updater
from graph_updaters.team_graph_updater import team_graph_updater
from hosted_service import HostedService
from storylines.basic_storyline import BasicStoryline


def main():
    neo4j_driver = GraphDatabase.driver(NEO4J_BOLT_CONNECTION, auth=(NEO4J_USERNAME, NEO4J_PASSWORD), encrypted=False)

    initial_storyline = BasicStoryline([
        team_graph_updater,
        # division_graph_updater,
        # roster_graph_updater,
        coaches_graph_updater,
        object_properties_graph_updater
    ])

    playoffs_storyline = BasicStoryline([
        playoff_series_graph_updater,
        nba_champions_graph_updater
    ])

    hosted_service = HostedService([initial_storyline,
                                    playoffs_storyline])

    hosted_service.run(neo4j_driver)


if __name__ == "__main__":
    main()
