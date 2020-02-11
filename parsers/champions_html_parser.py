from bs4 import BeautifulSoup
from config import BEAUTIFUL_SOUP_FEATURE
from core_objects.html_parser_base import HtmlParserBase


class ChampionsHtmlParser(HtmlParserBase):
    def parse(self, html_file):
        soup = BeautifulSoup(html_file, features=BEAUTIFUL_SOUP_FEATURE)
        champions = soup.find(attrs={"dir": "ltr"}).findNext("tbody")
        parsed_champions = self._parse_champions(champions)
        parsed_champions.insert(0, ["year", "winner", "wins", "losses", "opponent"])
        return parsed_champions

    def _parse_champions(self, champions):
        rows = champions.findAllNext("tr")
        parsed_champions = [
            [rows[1].contents[1].string, rows[1].contents[3].string, rows[1].contents[7].text.split("-")[0],
             rows[1].contents[7].text.split("-")[1], rows[1].contents[9].string]]
        for row in rows[2:9]:
            parsed_champions.append(
                [row.contents[1].string, row.contents[3].string, row.contents[7].text.split("–")[0],
                 row.contents[7].text.split("–")[1], row.contents[9].string])

        return parsed_champions
