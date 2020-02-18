from core_objects.storyline_base import StorylineBase


class BasicStoryline(StorylineBase):
    def action(self, driver):
        for graph_updater in self.graph_updaters:
            graph_updater.update_graph(driver)
