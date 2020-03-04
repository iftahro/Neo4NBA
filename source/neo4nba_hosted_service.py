from typing import List

from source.core_objects.storyline import Storyline
from source.core_objects.hosted_service import HostedService

from source.graph_updaters.awards.award_properties_graph_updater import award_properties_graph_updater
from source.graph_updaters.awards.awards_graph_updater import awards_graph_updater
from source.graph_updaters.draft.draft_graph_updater import draft_graph_updater
from source.graph_updaters.draft.draft_properties_graph_updater import draft_properties_graph_updater
from source.graph_updaters.draft.rookie_graph_updater import rookie_graph_updater
from source.graph_updaters.games.game_properties_graph_updater import game_properties_graph_updater
from source.graph_updaters.games.regular_season_game_graph_updater import regular_season_game_graph_updater
from source.graph_updaters.initial.coach_graph_updater import coaches_graph_updater
from source.graph_updaters.initial.initial_properties_graph_updater import initial_properties_graph_updater
from source.graph_updaters.initial.player_graph_updater import player_graph_updater
from source.graph_updaters.initial.team_graph_updater import team_graph_updater
from source.graph_updaters.playoffs.champions_graph_updater import champions_graph_updater
from source.graph_updaters.playoffs.playoff_series_graph_updater import playoff_series_graph_updater


class Neo4NBAHostedService(HostedService):
    @property
    def storyline(self) -> List[Storyline]:
        initial_storyline = Storyline([
            team_graph_updater,
            player_graph_updater,
            coaches_graph_updater,
            initial_properties_graph_updater
        ])

        playoffs_storyline = Storyline([
            playoff_series_graph_updater,
            champions_graph_updater
        ])

        award_storyline = Storyline([
            awards_graph_updater,
            award_properties_graph_updater
        ])

        draft_storyline = Storyline([
            draft_graph_updater,
            draft_properties_graph_updater,
            rookie_graph_updater
        ])

        games_storyline = Storyline([
            regular_season_game_graph_updater,
            game_properties_graph_updater
        ])

        return [
            initial_storyline,
            playoffs_storyline,
            award_storyline,
            draft_storyline,
            games_storyline
        ]
