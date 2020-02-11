from abc import ABCMeta, abstractmethod, ABC


class GraphUpdaterBase(metaclass=ABCMeta):
    @abstractmethod
    def update_graph(self, driver):
        pass


class CsvGraphUpdater(GraphUpdaterBase, ABC, metaclass=ABCMeta):
    def __init__(self, file_name):
        self.file_name = file_name
