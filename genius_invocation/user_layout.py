from rich import box
from rich.align import Align
from rich.console import Console, Group
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax
from rich.table import Table
from typing import TYPE_CHECKING
from genius_invocation.utils import *
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer
from genius_invocation.entity.status import Shield
from loguru import logger
def layout(game: 'GeniusGame'):
    layout = Layout()
    layout.split_column(
        Layout(name="Game", ratio=1),
        Layout(name="player0", ratio=3),
        Layout(name="player1",ratio=3)
    )
    layout['Game'].update(get_game_info(game))
    for i in range(2):
        player = "player" + str(i)
        layout[player].split_row(
            Layout(name="card", ratio=1),
            Layout(name="support", ratio=2),
            Layout(name="character", ratio=5),
            Layout(name="summon", ratio=2),
            Layout(name="dice", ratio=1)
        )

        layout[player]['support'].split_column(Layout(name="12"),Layout(name="34"),)
        layout[player]['support']['12'].split_row(get_support(game.players[i], 0),get_support(game.players[i], 1))
        layout[player]['support']['34'].split_row(get_support(game.players[i], 2),get_support(game.players[i], 3))
        layout[player]['summon'].split_column(Layout(name="12"),Layout(name="34"),)

        layout[player]['summon']['12'].split_row(get_summon(game.players[i], 0),get_summon(game.players[i], 1))
        layout[player]['summon']['34'].split_row(get_summon(game.players[i], 2),get_summon(game.players[i], 3))

        layout[player]['character'].split_row(get_character(game.players[i], 0),
                                                 get_character(game.players[i], 1),
                                                 get_character(game.players[i], 2))

        layout[player]['card'].split_column(
            Layout(name="cards", ratio=1),
            Layout(name="hands", ratio=3),
        )
        layout[player]['card']['cards'].update(get_card(game.players[i]))
        layout[player]['card']['hands'].update(get_hand(game.players[i]))

        layout[player]['dice'].update(get_dice(game.players[i]))
    return layout

def get_game_info(game: 'GeniusGame'):
    sponsor_message = Table.grid()
    sponsor_message.add_column(no_wrap=True)
    sponsor_message.add_row(
        f"Round:{game.round}, Round_Phase:{game.game_phase.value}, Active_player:{game.active_player_index}, First_player:{game.first_player}",
        style='blue',
    )
    message_panel = Panel(
        Align.center(
            Group(" ",Align.center(sponsor_message)),
        ),
        title="Game Information",
    )
    return message_panel

def get_character(player: 'GeniusPlayer', idx: int):
    sponsor_message = Table.grid()
    sponsor_message.add_column(no_wrap=False, justify="medium")
    character_list = player.character_list
    if character_list[idx].is_active:
        color = 'red'
    else:
        color = 'black'
    if character_list[idx].is_alive:
        col = 'rgb(255,255,255)'
        if len(character_list[idx].elemental_application)>0:
            col = Elements_to_color(character_list[idx].elemental_application[0])
        sponsor_message.add_row(
            Elementals_to_str(character_list[idx].elemental_application),
            style=col,
        )
        sponsor_message.add_row(
            character_list[idx].name_ch,
            style=color,
        )
        sponsor_message.add_row(
            character_list[idx].show(),
            style=color,
        )
        sponsor_message.add_row(
            str(character_list[idx].power),
            style=color,
        )

        if character_list[idx].character_zone.weapon_card != None:
            sponsor_message.add_row(
                character_list[idx].character_zone.weapon_card.show(),
                style=color,
            )
        if character_list[idx].character_zone.artifact_card != None:
            sponsor_message.add_row(
                character_list[idx].character_zone.artifact_card.show(),
                style=color,
            )
        if character_list[idx].talent == True:
            sponsor_message.add_row(
                f"Has Talent",
                style=color,
            )
        for status in character_list[idx].character_zone.status_list:
            if isinstance(status, Shield):
                col = 'yellow'
            else:
                col='blue'
            sponsor_message.add_row(
                f"{status.name_ch}: {status.show()}",
                style=col,
            )
        if character_list[idx].is_active:
            for status in player.team_combat_status.shield:
                sponsor_message.add_row(
                    f"{status.name_ch}:{status.show()}",
                    style='yellow',
                )
            for status in player.team_combat_status.space:
                sponsor_message.add_row(
                    f"{status.name_ch}:{status.show()}",
                    style='blue',
                )
    message_panel = Panel(
        Align.center(
            Group(" ",Align.center(sponsor_message)),
            vertical="middle",
        ),
        title="Character"+str(idx),
    )
    return message_panel

def get_card(player: 'GeniusPlayer'):
    sponsor_message = Table.grid()
    sponsor_message.add_column(no_wrap=True)
    sponsor_message.add_row(
        str(player.card_zone.num()),
        style='blue',
    )
    message_panel = Panel(
        Align.center(
            Group(" ",Align.center(sponsor_message)),
        ),
        title="CardZone",
    )
    return message_panel

def get_hand(player: 'GeniusPlayer'):
    sponsor_message = Table.grid()
    sponsor_message.add_column(no_wrap=True)
    if player.hand_zone.num() != 0:
        for card in player.hand_zone.card:
            sponsor_message.add_row(
                card.name_ch,
                style='blue',
            )
    message_panel = Panel(
        Align.center(
            Group(" ",Align.center(sponsor_message)),
        ),
        title="HandCard"+str(player.index),
    )
    return message_panel

def get_summon(player: 'GeniusPlayer', idx):
    sponsor_message = Table.grid()
    sponsor_message.add_column(no_wrap=True)
    if player.summon_zone.num() > idx:
        summon = player.summon_zone.space[idx]
        sponsor_message.add_row(
            summon.name_ch,
            style=Elements_to_color(summon.element),
        )
        sponsor_message.add_row(
            str(summon.show()),
            style=Elements_to_color(summon.element),
        )
    message_panel = Panel(
        Align.center(
            Group(" ",Align.center(sponsor_message)),
        ),
        title="Summon"+str(idx+1),
    )
    return message_panel


def get_support(player: 'GeniusPlayer', idx):
    sponsor_message = Table.grid()
    sponsor_message.add_column(no_wrap=True)
    if player.support_zone.num() > idx:
        support = player.support_zone.space[idx]
        sponsor_message.add_row(
            support.name_ch,
            style='blue',
        )
        sponsor_message.add_row(
            support.show(),
            style='blue',
        )

    message_panel = Panel(
        Align.center(
            Group(" ",Align.center(sponsor_message)),
        ),
        title="Support" + str(idx),
    )
    return message_panel

def get_dice(player: 'GeniusPlayer'):
    sponsor_message = Table.grid()
    sponsor_message.add_column(no_wrap=True)
    if player.dice_zone.show() is not None:
        for dice in player.dice_zone.show():
            sponsor_message.add_row(
                DiceType(dice).name,
                style='blue',
            )

    message_panel = Panel(
        Align.center(
            Group(" ",Align.center(sponsor_message)),
            vertical="middle",
        ),
        title="DiceZone"+str(player.index),
    )
    return message_panel