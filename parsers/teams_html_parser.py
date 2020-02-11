from bs4 import BeautifulSoup

from config import BEAUTIFUL_SOUP_FEATURE
from core_objects.html_parser_base import HtmlParserBase


class TeamsHtmlParser(HtmlParserBase):
    def parse(self, html_file):
        soup = BeautifulSoup(html_file, features=BEAUTIFUL_SOUP_FEATURE)
        shorts = soup.find("table", {"class", "wikitable sortable"}).findAllNext("tr")[1:]

        teams_shorts = [["short", "full_name"]]
        for short in shorts:
            teams_shorts.append([x for x in short.text.split("\n") if x != ""])

        return teams_shorts
