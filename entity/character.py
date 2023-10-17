from typing import TYPE_CHECKING, List
from utils import *
from entity.entity import Entity

if TYPE_CHECKING:
    from game.game import GeniusGame
    from game.zone import CharacterZone
    from game.action import Action
    from game.player import GeniusPlayer
    from event.events import ListenerNode
    from card.character import CharacterSkill
    from entity.status import Status

class Character(Entity):
    # 角色基本类
    id: int #Identity document, 卡牌的编号，可能用来喂给state for RL。
    name: str
    element: ElementType
    weapon_type: WeaponType
    country: CountryType
    init_health_point: int
    # health_point: int
    max_health_point: int

    '''
        characacter_skill_list包含的是CharacterSkill类, 初始化时会创建skills, 包含的是CharacterSkill类的实例

        后续调用时请调用skills中的实例
    '''
    # skill_list: List['CharacterSkill'] 这么写怪怪的
    skill_list: List
    power: int
    max_power: int

    # init_state: list() # 初始状态
    def init_state(self, game: 'GeniusGame'):
        '''
            游戏开始时的被动技能触发
        '''
        pass

    def init_skill(self):
        self.skills = []
        for skill in self.skill_list:
            self.skills.append(skill(self))

    def skill(self, skill, game: 'GeniusGame'):
        self.skills[skill].on_call(game)

    def __init__(self, game: 'GeniusGame', character_zone:'CharacterZone', from_player: 'GeniusPlayer', index:int, from_character = None):
        self.character_zone = character_zone
        self.init_skill()
        self.talent: bool = False
        self.is_active: bool = False
        self.is_alive: bool = True
        self.health_point = self.init_health_point
        self.power: int = 0 # 初始充能
        self.elemental_application: List['ElementType'] = []
        self.index: int = index
        super().__init__(game, from_player, from_character)

    def heal(self, heal):
        self.health_point += heal
        if self.hp > self.max_health_point:
            self.hp = self.max_health_point









    # def on_game_start(self):
    #     '''
    #         角色区初始化
    #         讨债人被动 潜行
    #         雷电将军被动 诸愿百眼之轮
    #         无相雷、丘丘等上限修改
    #     '''
    #     return self.power, self.health_point, self.init_state


    # def on_round_start(self, game: GeniusGame):
    #     '''
    #         预留
    #     '''
    #     pass

    # def on_switched(self, game: GeniusGame):
    #     '''
    #         passive skill 被动技能 神里绫华

    #     '''
    #     pass
