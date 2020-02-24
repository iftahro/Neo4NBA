from typing import List

from source.core_objects.storyline import Storyline


class HostedService:
    @property
    def storyline(self) -> List[Storyline]:
        return []

    def run(self, driver):
        for storyline in self.storyline:
            storyline.action(driver)
