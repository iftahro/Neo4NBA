from bs4 import BeautifulSoup

from config import BEAUTIFUL_SOUP_FEATURE
from core_objects.html_parser_base import HtmlParserBase
from utils.utils import ExtractHtmlFromUrl


class AwardHtmlParser(HtmlParserBase):
    def __init__(self, award_name):
        self.age_index = 4
        if award_name == "finals_mvp":
            self.age_index = 3
        self.award_name = award_name

    def parse(self, html_file):
        soup = BeautifulSoup(html_file, features=BEAUTIFUL_SOUP_FEATURE)
        award_table = soup.find(id=f"{self.award_name}_NBA")
        award_body = award_table.findNext("tbody")
        parsed_award = self._parse_award_body(award_body)
        parsed_award.insert(0, ["year", "name", "age", "games", "minutes", "points", "rebounds", "assists", "steals",
                                "blocks"])
        return parsed_award

    def _parse_award_body(self, award_body):
        rows = award_body.findAllNext("tr")
        parsed_award = []
        for row in rows[0:25]:
            parsed_row = [row.contents[2].string, row.contents[self.age_index].string,
                          row.contents[self.age_index + 2].string, row.contents[self.age_index + 3].string,
                          row.contents[self.age_index + 4].string, row.contents[self.age_index + 5].string,
                          row.contents[self.age_index + 6].string, row.contents[self.age_index + 7].string,
                          row.contents[self.age_index + 8].string]
            parsed_row.insert(0, row.contents[0].string.split("-")[0][0:2] + row.contents[0].string.split("-")[1])
            parsed_award.append(parsed_row)
        return parsed_award
