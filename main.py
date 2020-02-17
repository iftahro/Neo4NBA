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
    # storylines = []
    # # All NBA teams
    # storylines.append(CsvStoryline(team_graph_updater(), TeamsHtmlParser(), TEAMS_URL))
    # # Divisions and conferences
    # storylines.append(BasicStoryline(division_graph_updater("nba_divisions.csv")))
    #
    # # Rosters and coaches
    # for i in range(2015, 2021):
    #     for short in NBA_SHORTS:
    #         roster_url = ROSTER_URL.format(team_label=short, year=str(i))
    #         if short in INVALID_TEAMS_LABELS.keys():
    #             roster_url = ROSTER_URL.format(team_label=INVALID_TEAMS_LABELS[short], year=str(i))
    #         storylines.append(CsvStoryline(roster_graph_updater(short, str(i)), RosterHtmlParser(), roster_url))
    #     # Coaches
    #     storylines.append(CsvStoryline(coaches_graph_updater(str(i)), CoachesHtmlParser(),
    #                                    COACHES_URL.format(year=str(i))))
    # # Positions
    # storylines.append(BasicStoryline(PositionsGraphUpdater()))
    #
    # # Personal awards
    # for award in NBA_AWARDS.keys():
    #     storylines.append(CsvStoryline(award_graph_updater(award), AwardHtmlParser(award),
    #                                    AWARD_URL.format(award_name=award)))
    # storylines.append(CsvStoryline(ChampionsGraphUpdater("nba_champions.csv"), ChampionsHtmlParser(), CHAMPIONS_URL))

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
