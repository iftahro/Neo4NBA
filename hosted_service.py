from typing import List

from source.core_objects.storyline import Storyline


class HostedService:
    def __init__(self, storyline: List[Storyline]):
        self.storyline = storyline

    def run(self, driver):
        for storyline in self.storyline:
            storyline.action(driver)
