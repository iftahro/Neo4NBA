from bs4 import BeautifulSoup

from config import BEAUTIFUL_SOUP_FEATURE
from constants import INVALID_TEAMS_LABELS
from core_objects.html_parser_base import HtmlParserBase


class CoachesHtmlParser(HtmlParserBase):
    def parse(self, html_file):
        soup = BeautifulSoup(html_file, features=BEAUTIFUL_SOUP_FEATURE)
        coaches_table = soup.find(id="NBA_coaches")
        coaches_body = coaches_table.findNext("tbody")
        parsed_coaches = self._parse_coaches_body(coaches_body)
        parsed_coaches.insert(0, ["name", "team_label", "games", "wins", "losses"])
        return parsed_coaches

    def _parse_coaches_body(self, coaches_body):
        rows = coaches_body.findAllNext("tr")
        parsed_body = []
        for row in rows:
            parsed_body.append(
                [row.contents[0].string,
                 row.contents[1].string if row.contents[1].string not in INVALID_TEAMS_LABELS.values() else
                 list(INVALID_TEAMS_LABELS.keys())[list(INVALID_TEAMS_LABELS.values()).index(row.contents[1].string)],
                 row.contents[6].string, row.contents[7].string,
                 row.contents[8].string])
        return parsed_body
