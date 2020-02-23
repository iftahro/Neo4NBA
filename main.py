import logging
from neo4j import GraphDatabase

from hosted_service import HostedService
from source.core_objects.storyline import Storyline
from config import NEO4J_USERNAME, NEO4J_BOLT_ADDRESS, NEO4J_PASSWORD

from source.graph_updaters.awards.award_properties_graph_updater import award_properties_graph_updater
from source.graph_updaters.awards.awards_graph_updater import awards_graph_updater
from source.graph_updaters.draft.draft_graph_updater import draft_graph_updater
from source.graph_updaters.draft.draft_properties_graph_updater import draft_properties_graph_updater
from source.graph_updaters.draft.rookie_graph_updater import rookie_graph_updater
from source.graph_updaters.initial.coach_graph_updater import coaches_graph_updater
from source.graph_updaters.initial.initial_properties_graph_updater import initial_properties_graph_updater
from source.graph_updaters.playoffs.champions_graph_updater import champions_graph_updater
from source.graph_updaters.playoffs.playoff_series_graph_updater import playoff_series_graph_updater
from source.graph_updaters.initial.player_graph_updater import player_graph_updater
from source.graph_updaters.initial.team_graph_updater import team_graph_updater


def configure_logging():
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.DEBUG,
        handlers=[logging.StreamHandler()])

    logging.getLogger("neobolt").setLevel(logging.WARNING)


def main():
    configure_logging()

    neo4j_driver = GraphDatabase.driver(NEO4J_BOLT_ADDRESS, auth=(NEO4J_USERNAME, NEO4J_PASSWORD), encrypted=False)

    initial_storyline = Storyline([
        team_graph_updater,
        player_graph_updater,
        coaches_graph_updater,
        initial_properties_graph_updater
    ])

    playoffs_storyline = Storyline([
        playoff_series_graph_updater,
        champions_graph_updater
    ])

    award_storyline = Storyline([
        awards_graph_updater,
        award_properties_graph_updater
    ])

    draft_storyline = Storyline([
        draft_graph_updater,
        draft_properties_graph_updater,
        rookie_graph_updater
    ])

    hosted_service = HostedService([
        initial_storyline,
        playoffs_storyline,
        award_storyline,
        draft_storyline
    ])

    hosted_service.run(neo4j_driver)


if __name__ == "__main__":
    main()
