from os import listdir

from config import NEO4J_IMPORT_DIRECTORY
from core_objects.graph_updater_base import GraphUpdaterBase
from core_objects.html_parser_base import HtmlParserBase
from core_objects.storyline_base import StorylineBase
from utils.utils import ExtractHtmlFromUrl, SaveMatrixToCsv


class CsvStoryline(StorylineBase):
    def __init__(self, graph_updater: GraphUpdaterBase, html_parser: HtmlParserBase, url):
        super().__init__(graph_updater, html_parser)
        self.url = url

    def action(self, driver):
        import_files = listdir(NEO4J_IMPORT_DIRECTORY)
        if self.graph_updater.file_name not in import_files:
            teams_html = ExtractHtmlFromUrl(self.url)
            parsed_teams = self.html_parser.parse(teams_html)
            SaveMatrixToCsv(parsed_teams, self.graph_updater.file_name)

        self.graph_updater.update_graph(driver)
