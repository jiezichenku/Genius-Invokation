from genius_invocation.card.action.equipment.talent.import_head import *
from genius_invocation.card.character.characters.Nilou import * 

class TheStarrySkiesTheirFlowersRain(TalentCard):
    id: int = 212081
    name: str = "The Starry Skies Their Flowers Rain"
    name_ch = "星天的花雨"
    is_action = True
    cost = [{'cost_num': 3, 'cost_type': 1}]
    cost_power = 0
    character = Nilou
    def __init__(self) -> None:
        super().__init__()
        