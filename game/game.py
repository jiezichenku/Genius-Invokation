from typing import List
from player import GeniusPlayer
from game.action import Action
import numpy as np
from utils import *

class GeniusGame:
    '''
    主游戏
    '''
    def __init__(self, seed, player0_deck, player1_deck) -> None:
        self.num_players = 3
        self.seed = seed
        np.random.seed(seed)
        self.first_player: int
        self.active_player: int
        player0 = GeniusPlayer(player0_deck)
        player1 = GeniusPlayer(player1_deck)
        self.players = [player0, player1]
        self.game_phase: GamePhase
        self.round: int
    
    def reset(self):
        pass

    def init_game(self):
        '''
        初始化阶段,包括选择起始手牌,选择出战角色
        '''
        # 决定谁方先手
        first = np.random.choice([0, 1], 1)[0]
        self.first_player = first
        # 进入选择起始手牌阶段
        self.game_phase = GamePhase.SET_CARD
        self.active_player = first

    def resolve_action(self, action: Action):
        if action.choice_type == ActionChoice.HAND_CARD:
            pass
        elif action.choice_type == ActionChoice.CHARACTER_SKILL:
            pass
        elif action.choice_type == ActionChoice.CHANGE_CHARACTER:
            pass

    def step(self, action: Action):
        '''
        回合轮次
        '''
        match self.game_phase:
            case GamePhase.SET_CARD:
                self.set_hand_card()
            case GamePhase.SET_CHARACTER:
                self.set_active_character()
            case GamePhase.ROLL_PHASE:
                self.set_reroll_dice()
            case GamePhase.ACTION_PHASE:
                self.resolve_action(action)
        
    def set_hand_card(self, action):
        '''
        选择手牌部分
        action: [5,1] 0/1
        '''
        active = self.active_player
        self.players[active].choose_card(action)
        if self.active_player == self.first_player:
            self.active_player = not active
        else:
            self.game_phase = GamePhase.SET_CHARACTER
            self.active_player = self.first_player

    def set_active_character(self, action):
        '''
        选择出战角色
        action: [3,1] one-hot
        '''
        active = self.active_player
        self.players[active].choose_character(action)
        if self.active_player == self.first_player:
            self.active_player = not active
        else:
            self.roll_phase()
            self.active_player = self.first_player

    def set_reroll_dice(self, action):
        '''
        选择重新投掷的骰子
        action: [num_dice, 1] 0/1
        '''
        active = self.active_player
        self.players[active].choose_dice(action)
        if self.active_player == self.first_player:
            self.active_player = not active
        else:
            self.action_phase()
            self.active_player = self.first_player
    
    def roll_phase(self):
        '''
        进入投掷骰子的阶段
        '''
        self.game_phase = GamePhase.ROLL_PHASE
        for player in self.players:
            player.dice_zone = player.roll_dice()
    
    def action_phase(self):
        self.game_phase = GamePhase.ACTION_PHASE
