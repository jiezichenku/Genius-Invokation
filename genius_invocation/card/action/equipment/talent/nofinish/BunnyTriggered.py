from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Ambor import * 

class BunnyTriggered(TalentCard):
    id: int = 213041
    name: str = "Bunny Triggered"
    name_ch = "一触即发"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 2}]
    cost_power = 0
    character = Ambor
    def __init__(self) -> None:
        super().__init__()
        