from neo4j import GraphDatabase

from config import NEO4J_USERNAME, NEO4J_BOLT_CONNECTION, NEO4J_PASSWORD
from constants import NBA_SHORTS, NBA_AWARDS, TEAMS_URL, ROSTER_URL, AWARD_URL, COACHES_URL, INVALID_TEAMS_LABELS, \
    CHAMPIONS_URL
from graph_updaters.award_graph_updater import award_graph_updater
from graph_updaters.champions_graph_updater import ChampionsGraphUpdater
from graph_updaters.coaches_graph_updater import CoachesGraphUpdater
from graph_updaters.division_graph_updater import DivisionGraphUpdater
from graph_updaters.positions_graph_updater import PositionsGraphUpdater
from graph_updaters.roster_graph_updater import RosterGraphUpdater
from graph_updaters.teams_graph_updater import TeamGraphUpdater
from hosted_service import HostedService
from parsers.award_html_parser import AwardHtmlParser
from parsers.champions_html_parser import ChampionsHtmlParser
from parsers.coaches_html_parser import CoachesHtmlParser
from parsers.roster_html_parser import RosterHtmlParser
from parsers.teams_html_parser import TeamsHtmlParser
from storylines.basic_storyline import BasicStoryline
from storylines.csv_storyline import CsvStoryline


def main():
    neo4j_driver = GraphDatabase.driver(NEO4J_BOLT_CONNECTION, auth=(NEO4J_USERNAME, NEO4J_PASSWORD), encrypted=False)
    storylines = []
    # All NBA teams
    storylines.append(CsvStoryline(TeamGraphUpdater(), TeamsHtmlParser(), TEAMS_URL))
    # Divisions and conferences
    storylines.append(BasicStoryline(DivisionGraphUpdater("nba_divisions.csv")))

    # Rosters and coaches
    for i in range(2015, 2021):
        for short in NBA_SHORTS:
            roster_url = ROSTER_URL.format(team_label=short, year=str(i))
            if short in INVALID_TEAMS_LABELS.keys():
                roster_url = ROSTER_URL.format(team_label=INVALID_TEAMS_LABELS[short], year=str(i))
            storylines.append(CsvStoryline(RosterGraphUpdater(short, str(i)), RosterHtmlParser(), roster_url))
        # Coaches
        storylines.append(CsvStoryline(CoachesGraphUpdater(str(i)), CoachesHtmlParser(),
                                       COACHES_URL.format(year=str(i))))
    # Positions
    storylines.append(BasicStoryline(PositionsGraphUpdater()))

    # Personal awards
    for award in NBA_AWARDS.keys():
        storylines.append(CsvStoryline(award_graph_updater(award), AwardHtmlParser(award),
                                       AWARD_URL.format(award_name=award)))
    storylines.append(CsvStoryline(ChampionsGraphUpdater("nba_champions.csv"), ChampionsHtmlParser(), CHAMPIONS_URL))

    # Starts the program
    hosted_service = HostedService(storylines)
    hosted_service.run(neo4j_driver)


main()
print("Done")
