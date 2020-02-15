from abc import ABCMeta, abstractmethod

from core_objects.graph_updater import GraphUpdater
from core_objects.graph_updater_base import GraphUpdaterBase
from core_objects.html_parser_base import HtmlParserBase


class StorylineBase(metaclass=ABCMeta):
    def __init__(self, graph_updater: GraphUpdater, html_parser: HtmlParserBase = None):
        self.graph_updater = graph_updater
        self.html_parser = html_parser

    @abstractmethod
    def action(self, driver):
        pass
