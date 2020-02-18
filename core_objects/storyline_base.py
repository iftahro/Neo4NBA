from abc import ABCMeta, abstractmethod
from core_objects.graph_updater import GraphUpdater


class StorylineBase(metaclass=ABCMeta):
    def __init__(self, graph_updaters):
        self.graph_updaters = graph_updaters

    @abstractmethod
    def action(self, driver):
        pass
