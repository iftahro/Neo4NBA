from bs4 import BeautifulSoup

from config import BEAUTIFUL_SOUP_FEATURE
from core_objects.html_parser_base import HtmlParserBase


class RosterHtmlParser(HtmlParserBase):
    TABLE_HEADERS = ["number", "name", "position", "height", "weight", "birth_date", "birth_country", "experience",
                     "college"]

    def parse(self, html_file):
        soup = BeautifulSoup(html_file, features=BEAUTIFUL_SOUP_FEATURE)
        roster_table = soup.find(id="roster")

        table_body = roster_table.findAllNext("tbody")[0]
        parsed_table = self.parse_body(table_body)
        parsed_table.insert(0, self.TABLE_HEADERS)
        return parsed_table

    def parse_body(self, body):
        parsed_body = []
        rows = body.findAllNext("tr")
        for row in rows:
            player_properties = ["None" if row.findNext(attrs={"scope": "row"}).string is None else row.findNext(
                attrs={"scope": "row"}).string]
            properties = row.findAllNext("td")[0:8]

            for prop in properties:
                contents = prop.contents
                if len(contents) == 0:
                    player_properties.append("None")
                elif len(contents) >= 3:
                    player_properties.append("".join(
                        [content.string if not content.string.startswith("(") and content.string != "\xa0\xa0" else ""
                         for content in contents]))
                else:
                    player_properties.append(prop.string)
            parsed_body.append(player_properties)

        return parsed_body
