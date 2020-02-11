from core_objects.storyline_base import StorylineBase


class BasicStoryline(StorylineBase):
    def action(self, driver):
        self.graph_updater.update_graph(driver)
