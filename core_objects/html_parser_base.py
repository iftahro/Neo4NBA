from abc import ABCMeta, abstractmethod


class HtmlParserBase(metaclass=ABCMeta):
    @abstractmethod
    def parse(self, html_file):
        pass