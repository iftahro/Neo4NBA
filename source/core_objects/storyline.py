import logging


class Storyline:
    def __init__(self, graph_updaters):
        self.graph_updaters = graph_updaters

    def action(self, driver):
        for graph_updater in self.graph_updaters:
            logging.debug(f"Started updating {graph_updater.name}")
            graph_updater.update_graph(driver)
            logging.debug(f"Finished updating {graph_updater.name}")

