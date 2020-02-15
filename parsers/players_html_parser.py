from bs4 import BeautifulSoup

from config import BEAUTIFUL_SOUP_FEATURE
from core_objects.html_parser_base import HtmlParserBase
from utils.utils import ExtractHtmlFromUrl, SaveMatrixToCsv


class PlayersHtmlParser:
    def parse(self, html_file, year):
        soup = BeautifulSoup(html_file, features=BEAUTIFUL_SOUP_FEATURE)
        award_table = soup.findAll(attrs={"class": "full_table"})
        award_table += soup.findAll(attrs={"class": "italic_text partial_table"})
        a = [
            ["Year", "Player", "Pos", "Age", "Tm", "G", "GS", "MP", "FG", "FGA", "FG%", "3P", "3PA", "3P%", "2P", "2PA",
             "2P%", "eFG%", "FT", "FTA", "FT%", "ORB", "DRB", "TRB", "AST", "STL", "BLK", "TOV", "PF", "PTS"]]
        for award in award_table:
            b = [year]
            b += [x.string for x in award.contents[1:]]
            a.append(b)
        return a


b = ExtractHtmlFromUrl("https://www.basketball-reference.com/leagues/NBA_2019_per_game.html")
a = PlayersHtmlParser()
m = a.parse(b, "2019")
SaveMatrixToCsv(m, "2019_players.csv")
