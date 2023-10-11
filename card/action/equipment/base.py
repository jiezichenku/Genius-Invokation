from ..base import ActionCard
from game.game import GeniusGame
from typing import TYPE_CHECKING
from entity.entity import Entity

if TYPE_CHECKING:
    from game.zone import CharacterZone
    from game.player import GeniusPlayer

class Equipment(Entity):
    # 装备
    pass


class EquipmentCard(ActionCard):
    # 装备牌基本类
    player: GeniusPlayer
    character: CharacterZone
    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: GeniusGame) -> None:
        # equipment = 
        pass

    def effect(self, game: GeniusGame) -> None:
        target = game.current_action.target_idx
        self.player = game.players[game.active_player]
        self.character = self.player.active_zone.character_list[target]
