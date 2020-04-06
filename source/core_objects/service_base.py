import logging
from typing import List

from source.core_objects.storyline import Storyline


class ServiceBase:
    def __init__(self, storyline=None):
        self.storyline = self._initialize_storyline() if storyline is None else storyline

    def run(self, driver):
        logging.info("Started updating the graph!")
        for storyline in self.storyline:
            storyline.action(driver)
        logging.info("Finished updating the graph!")

    def _initialize_storyline(self) -> List[Storyline]:
        pass
