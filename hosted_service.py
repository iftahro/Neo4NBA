from typing import List

from core_objects.storyline_base import StorylineBase


class HostedService:
    def __init__(self, storylines: List[StorylineBase]):
        self.storylines = storylines

    def run(self, driver):
        for storyline in self.storylines:
            storyline.action(driver)
