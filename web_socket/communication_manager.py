"""This file includes numerous print statements to facilitate thorough project tracking and monitoring during development."""
import os
import time
from constant_variable import BATTLES, BOT_MODE, FORMATS, ACTION, SELECTED_BOT_TYPE, USERNAME, PASSWORD, PLAYER
from web_socket.sender import Sender
from BattleBots.battle_bot import BattleBot
from BattleBots.random_bot import RandomBot
from BattleBots.greedy_bot import GreedyBot
from web_socket.login import log_in
import constant_variable


async def handle_showdown_messages(message: str, bot_mode: BOT_MODE):
    """This function handles all the down messages and sends them to the correct function in the program.
        If the message is about battle, its sends it to handle_showdown_battle_messages
        Specifically connect, start battling and send messages and commands."""
    sender = Sender()
    room, command, *rest = message.split('|')
    print("room: ", room)
    print("command: ", command)
    print("rest: ", rest)

    if command == 'challstr':
        # If we got the challstr, we now can log in.
        await log_in(rest[0], rest[1])

    elif command == 'updateuser':
        if USERNAME in rest[0].lower():
            if bot_mode == BOT_MODE.CHALLENGE_OWNER:
                await sender.challenge_user(PLAYER, FORMATS[0])
                constant_variable.CUR_BATTLES_COUNT += 1
            elif bot_mode == BOT_MODE.ACCEPT_CHALLENGE:
                await sender.accept_challenge(PLAYER)
                constant_variable.CUR_BATTLES_COUNT += 1
            elif bot_mode == BOT_MODE.SEARCH:
                await sender.search_game_in_format(FORMATS[0])
                constant_variable.CUR_BATTLES_COUNT += 1
            else:
                raise ValueError("Illegal mode")

    elif command == 'deinit':
        if bot_mode == BOT_MODE.SEARCH and constant_variable.CUR_BATTLES_COUNT < constant_variable.MAX_BATTLES_COUNT:
            await sender.search_game_in_format(FORMATS[0])

    elif command == 'pm':
        pass

    else:
        print('***: other')

    if "battle" in room:
        await handle_showdown_battle_messages(message)


def create_bot_based_on_type(battle_id, sender):
    if SELECTED_BOT_TYPE == 'random':
        return RandomBot(battle_id, sender)
    elif SELECTED_BOT_TYPE == 'greedy':
        return GreedyBot(battle_id, sender)
    else:
        raise ValueError("Invalid BOT TYPE selected in config.ini")


async def handle_showdown_battle_messages(message: str):
    """This function handles messages about a battle"""
    # Split the message into parts based on newline characters
    message_parts = message.split('\n')

    sender = Sender()
    battle_id = message_parts[0].split('|')[0].split('>')[1]
    battle = get_battle_from_battles(BATTLES, battle_id)  # At the start of each iteration, get ref to the given battle

    for message_part in message_parts:
        splitted_part = message_part.split('|')

        try:
            if len(splitted_part) < 2:
                continue  # Go to the next iteration

            _, command, *rest = splitted_part

            if command == "init":
                # Create an object to the battle and append it to BATTLES list
                battle_id = message_parts[0].split("|")[0].split(">")[1]
                battle = create_bot_based_on_type(battle_id, sender)
                BATTLES.append(battle)

                # Alert that the bot in the battle and start the timer
                await sender.send_message(battle.battle_id, "Hey! The bot has started!")
                await sender.send_message(battle.battle_id, "/timer on")

            elif command == "player":
                if rest[1] == USERNAME.lower():
                    battle.player_id = rest[0]
                    battle.turn = int(rest[0].split('p')[1]) - 1

            elif command == "request":
                if rest[0] != '':
                    if len(rest[0]) == 1:
                        await battle.update_bot_team(rest[1].split('\n')[1])
                    else:
                        await battle.update_bot_team(rest[0])

            elif command == "teampreview":
                print("started teampreview")
                await battle.make_team_order()
                print("end teampreview")

            elif command == "turn":
                if BattleBot.get_lives_count_of_bot_pokemon(battle.bot_team) == 1:
                    # When having 1 left it can't be switched, so move is forced
                    await battle.make_action(sender, ACTION.MOVE)
                elif '"maybeTrapped":true' in rest:
                    await battle.make_action(sender, ACTION.MOVE)
                else:
                    await battle.make_action(sender)

            elif command == "callback":
                if rest[0] == "trapped":
                    await battle.make_action(sender, ACTION.MOVE)

            elif command == "poke":
                if battle.player_id not in rest[0]:
                    await battle.update_enemy_team(*extract_argument_for_update_enemy_method(rest))

            elif command == "win":
                await sender.send_message(battle.battle_id, "GG!")
                await sender.leave(battle.battle_id)
                BATTLES.remove(battle)
                if PLAYER.lower() in rest[-1].lower():
                    result = 'LOST'
                else:
                    result = 'WIN'
                save_battle_res(f'res/{SELECTED_BOT_TYPE}_log.txt', f'{result}, {battle_id}, {USERNAME} vs {PLAYER}')

            elif command == "error":
                # Error doesn't mean necessary a crushed!
                for r in rest:
                    if "The active Pokémon is trapped" in r:
                        # Handle a case were an ability, move or item forced trapped
                        await battle.make_action(sender, ACTION.MOVE)
                        return
                # Other error msgs that can be handled
                else:
                    raise RuntimeError(*rest)

            else:
                await handle_actions(battle, command, rest)

        except Exception as exception:
            await sender.send_message(battle_id, 'The bot has been crushed')
            await sender.forfeit(battle_id)
            time.sleep(2)
            raise exception


async def handle_actions(battle: BattleBot, command, rest):
    if command.startswith('-'):
        await minor_actions(battle, command, rest)
    else:
        await major_actions(battle, command, rest)


async def minor_actions(battle, command, rest):
    pass


async def major_actions(battle, command, rest):
    if command == "switch":
        if battle.player_id not in rest[0]:
            await battle.update_enemy_team(*extract_argument_for_update_enemy_method(rest))
            # update enemy
            pass

    elif command == "move":
        if battle.player_id in rest[0]:
            pass
        else:
            # Get the current enemy_pokemon reference and updates its known moves.
            enemy_pokemon_name = rest[0][5:]
            enemy_pokemon = battle.find_enemy_pokemon_by_name(battle.enemy_team.team, enemy_pokemon_name)
            move_name = rest[1]
            enemy_pokemon.update_enemy_moves(move_name)
        pass

    else:
        pass


def save_battle_res(file_path, line_to_add):
    # Check if the file exists
    if not os.path.exists(file_path):
        # If the file doesn't exist, create it
        with open(file_path, 'w'): pass

    # Open the file in append mode (a+)
    with open(file_path, 'a+') as file:
        # Move the file cursor to the beginning to ensure appending at the end
        file.seek(0)

        # Check if the file is empty, if so, add a newline
        if not file.read(1):
            file.write('\n')

        # Move the file cursor back to the end
        file.seek(0, 2)

        # Add the line to the file
        file.write(line_to_add + '\n')


# ----------- Supportive functions ----------- #

def extract_argument_for_update_enemy_method(rest):
    name = rest[1].split(',')[0].lower()
    level = rest[1].split(',')[1][2:]
    condition = rest[2]
    return name, level, condition


def get_battle_from_battles(battle_list: list[BattleBot], battle_id: str):
    return next((battle for battle in battle_list if battle.battle_id == battle_id), None)
