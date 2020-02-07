import json

from constants import ScoreSettings


class PlayerManagement:
    player = None
    _ranged_enemy_kill: int = 0
    _heavy_enemy_kill: int = 0
    _hth_enemy_kill: int = 0
    _player_high_scores: [int] = []

    @classmethod
    def init(cls, player):
        cls.player = player
        cls._player_high_scores = cls.load()

    @classmethod
    def get_score(cls) -> int:
        range_enemy_kill_points = cls._ranged_enemy_kill * ScoreSettings.RANGE_ENEMY_KILL
        heavy_enemy_kill_points = cls._heavy_enemy_kill * ScoreSettings.HEAVY_ENEMY_KILL
        hth_enemy_kill_points = cls._hth_enemy_kill * ScoreSettings.HTH_ENEMY_KILL
        abilities_level_points = (
                                         cls.player.ability_tornado_jump.level + cls.player.ability_slam.level + cls.player.ability_gust.level) \
                                 * ScoreSettings.ABILITY_POINTS_LEVEL
        return range_enemy_kill_points + heavy_enemy_kill_points + hth_enemy_kill_points + abilities_level_points

    @classmethod
    def add_score(cls, score):
        cls._player_high_scores.append(score)

    @classmethod
    def get_top_5_score(cls) -> [int]:
        return cls._player_high_scores.sort(reversed=True)[0:4]

    @classmethod
    def save(cls):
        scores_dict = {"high-score": cls._player_high_scores}
        with open('High-scores.json', 'w') as file:
            json.dump(scores_dict, file)

    @classmethod
    def load(cls) -> [int]:
        try:
            with open('High-scores.json', 'r') as file:
                scores_dict = json.load(file)
            return list(scores_dict.values())
        except FileNotFoundError:
            return []
