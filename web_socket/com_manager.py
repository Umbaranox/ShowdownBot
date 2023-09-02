from constant_variable import BATTLES, USERNAME, OWNER, BOT_MODE, FORMATS
from sender import Sender
from Battle.showdown_battle import Battle
import logger
import constant_variable


def check_battle(battle_list: list[Battle], battle_id: str):
    return next((battle for battle in battle_list if battle.battle_id == battle_id), None)


async def handle_showdown_messages(message: str, bot_mode: BOT_MODE):
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
                print("I WANT TO CHALLENGE")
                await sender.challenge_user(OWNER, FORMATS[0])
                constant_variable.CUR_BATTLES_COUNT += 1
            elif bot_mode == BOT_MODE.ACCEPT_CHALLENGE:
                print("I WANT TO ACCEPT")
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
    # Split the message into parts based on newline characters
    message_parts = message.split('\n')

    sender = Sender()
    battle_id = message_parts[0].split('|')[0].split('>')[1]
    battle = check_battle(BATTLES, battle_id)

    for message_part in message_parts:
        splitted_part = message_part.split('|')

        if len(splitted_part) < 2:
            continue  # Go to the next iteration

        _, command, *rest = splitted_part

        if command == "init":
            # Create an object to the battle and append it to BATTLES list
            battle_id = message_parts[0].split("|")[0].split(">")[1]
            battle = Battle(battle_id)
            BATTLES.append(battle)

            # Alert that the bot in the battle and start the timer
            await sender.send_message(battle.battle_id, "Hey! Battle started!")
            await sender.send_message(battle.battle_id, "/timer on")

        elif command == "player":
            if rest[1] == USERNAME:
                battle.player_id = rest[0]
                # TODO: battle's turn

        elif command == "request":
            if rest[0] != '':
                if len(rest[0]) == 1:
                    print("###req:")
                    print(rest[1].split('\n')[1])
                    print("###req:")
                    await battle.update_bot_team(rest[1].split('\n')[1])  # TODO: fill it
                else:
                    print("###req:")
                    print(rest[0])
                    print("###req:")
                    await battle.update_bot_team(rest[0])

        elif command == "teampreview":
            await battle.make_team_order()  # TODO: fill it

        elif command == "turn":
            await battle.make_action()

        elif command == "callback":
            if rest[0] == "trapped":
                # await battle.make_move(make_best_move(battle))
                print("TRAPPED! force to make move")
        elif command == "poke":
            if battle.player_id not in rest[0]:
                battle.update_enemy()  # TODO: fill it

        elif command == "win":
            if battle is None:
                print("Battle is None")
            await sender.send_message(battle.battle_id, "GG!")
            await sender.leave(battle.battle_id)
            BATTLES.remove(battle)
            # win function

        elif command == "error":
            raise RuntimeError(*rest)

        else:
            handle_battle(battle, command, rest)


def handle_battle(battle: Battle, command, rest):
    if command.startswith('-'):
        minor_actions(battle, command, rest)
    else:
        major_actions(battle, command, rest)


def minor_actions(battle, command, rest):
    print("minor")


def major_actions(battle, command, rest):
    print("major")

    if command == "switch":
        print("switch")

    elif command == "move":
        pass

    else:
        pass
