import time
from constant_variable import BATTLES, USERNAME, OWNER, BOT_MODE, FORMATS
from sender import Sender
from BattleBots.battle_bot import BattleBot
from BattleBots.random_bot import RandomBot
import logger
import constant_variable


async def handle_showdown_messages(message: str, bot_mode: BOT_MODE):
    """This function handles all the down messages and sends them to the correct function in the program.
        If the message is about battle, its sends it to handle_showdown_battle_messages
        Specificly connect, start battling and send messages and commands."""
    sender = Sender()
    room, command, *rest = message.split('|')
    print("room: ", room)
    print("command: ", command)
    print("rest: ", rest)

    if command == 'challstr':
        # If we got the challstr, we now can log in.
        print("Lets connect")
        await logger.log_in(rest[0], rest[1])

    elif command == 'updateuser':
        if USERNAME in rest[0]:
            if bot_mode == BOT_MODE.CHALLENGE_OWNER:
                await sender.challenge_user(OWNER, FORMATS[0])
                constant_variable.CUR_BATTLES_COUNT += 1
            elif bot_mode == BOT_MODE.ACCEPT_CHALLENGE:
                await sender.accept_challenge(OWNER)
                constant_variable.CUR_BATTLES_COUNT += 1
            elif bot_mode == BOT_MODE.SEARCH:
                await sender.search_game_in_format(FORMATS[0])
                constant_variable.CUR_BATTLES_COUNT += 1

        print("***: updateuser")

    elif command == 'deinit':
        if bot_mode == BOT_MODE.SEARCH and constant_variable.CUR_BATTLES_COUNT < constant_variable.MAX_BATTLES_COUNT:
            await sender.search_game_in_format(FORMATS[0])
        print("***: deinit")

    elif command == 'pm':
        print('***: pm')

    else:
        print('***: other')

    if "battle" in room:
        await handle_showdown_battle_messages(message)


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
            print("Inner command:", command)

            if command == "init":
                # Create an object to the battle and append it to BATTLES list
                battle_id = message_parts[0].split("|")[0].split(">")[1]
                battle = RandomBot(battle_id, sender)
                BATTLES.append(battle)

                # Alert that the bot in the battle and start the timer
                await sender.send_message(battle.battle_id, "Hey! BattleBot started!")
                await sender.send_message(battle.battle_id, "/timer on")

            elif command == "player":
                if rest[1] == USERNAME:
                    battle.player_id = rest[0]
                    battle.turn = int(rest[0].split('p')[1]) - 1

            elif command == "request":
                if rest[0] != '':
                    if len(rest[0]) == 1:
                        print("###req:1")
                        print(rest[1].split('\n')[1])
                        print("###req:")
                        await battle.update_bot_team(rest[1].split('\n')[1])
                    else:
                        print("###req:2")
                        print(rest[0])
                        print("###req:")
                        await battle.update_bot_team(rest[0])

            elif command == "teampreview":
                print("started teampreview")
                await battle.make_team_order()
                print("end teampreview")

            elif command == "turn":
                print("started turn")
                if battle.get_lives_count_of_bot_pokemon() == 1:
                    # When having 1 left it can't be switched
                    await battle.make_action(sender, BattleBot.ACTION.MOVE)
                elif '"maybeTrapped":true' in rest:
                    await battle.make_action(sender, BattleBot.ACTION.MOVE)
                else:
                    await battle.make_action(sender)
                print("end turn")

            elif command == "callback":
                if rest[0] == "trapped":
                    # await battle.make_move(make_best_move(battle))
                    print("TRAPPED! force to make move")
            elif command == "poke":
                if battle.player_id not in rest[0]:
                    print("Time to update enemy!")
                    await battle.update_enemy_team(*extract_argument_for_update_enemy_method(rest))
                    # print("started poke")

            elif command == "win":
                if battle is None:
                    print("BattleBot is None")
                await sender.send_message(battle.battle_id, "GG!")
                await sender.leave(battle.battle_id)
                BATTLES.remove(battle)
                # win function

            elif command == "error":
                raise RuntimeError(*rest)

            else:
                handle_actions(battle, command, rest)

        except Exception as exception:
            await sender.send_message(battle_id, 'The bot has been crushed')
            await sender.forfeit(battle_id)
            time.sleep(2)
            raise exception


def handle_actions(battle: BattleBot, command, rest):
    if command.startswith('-'):
        minor_actions(battle, command, rest)
    else:
        major_actions(battle, command, rest)


def minor_actions(battle, command, rest):
    pass


def major_actions(battle, command, rest):
    if command == "switch":
        if battle.player_id not in rest[0]:
            battle.update_enemy_team(*extract_argument_for_update_enemy_method(rest))
            # update enemy
            pass

    elif command == "move":
        pass

    else:
        pass


# ----------- Supportive functions ----------- #

def extract_argument_for_update_enemy_method(rest):
    name = rest[1].split(',')[0]
    level = rest[1].split(',')[1][2:]
    condition = rest[2]
    return name, level, condition


def get_battle_from_battles(battle_list: list[BattleBot], battle_id: str):
    return next((battle for battle in battle_list if battle.battle_id == battle_id), None)
