from BattleBots.battle_bot import BattleBot
from Engine.utility_calculator import evaluate_attacking_move_utility, evaluate_enemy_move, evaluate_switch_utility
from web_socket.constant_variable import ACTION


class GreedyBot(BattleBot):
    """
    A battle bot that makes decisions based on a greedy strategy.

    This bot evaluates the utility of available moves and switching options to make decisions during a battle.
    It aims to maximize its utility by considering move effectiveness and predicted enemy moves.
    """
    def __init__(self, battle_id: str, sender):
        super().__init__(battle_id, sender)
        self.enemy_pokemon = None

    async def update_enemy_team(self, pokemon_name: str, level: str, condition: str) -> None:
        """
        Overrides the parent class's method to update the enemy team with the given enemy Pokemon.

        Args:
            pokemon_name (str): The name of the enemy Pokemon.
            level (str): The level of the enemy Pokemon.
            condition (str): The condition or status of the enemy Pokemon.

        Raises:
            ValueError: If the enemy Pokemon is not found after updating the team.
        """
        await super().update_enemy_team(pokemon_name, level, condition)
        curr_enemy_pokemon = next((pokemon for pokemon in self.enemy_team.team if pokemon.name == pokemon_name), None)

        if curr_enemy_pokemon is None:
            raise ValueError("Enemy pokemon is not found, although it is updated.")
        self.enemy_pokemon = curr_enemy_pokemon

    async def make_action(self, sender, forced_action=ACTION.NONE):
        """
        Make a battle action based on a greedy strategy, considering moves and switching options.

        Args:
            sender (Sender): The sender object for communicating with the Pokemon Showdown server.
            forced_action (ACTION): A forced action to take, if any (e.g., ACTION.SWITCH, ACTION.MOVE).

        Raises:
            ValueError: If all moves or switches are not available.
        """
        move_utilities = evaluate_attacking_move_utility(self.curr_pokemon_ref, self.active_moves, self.enemy_pokemon)
        predicted_enemy_move = evaluate_enemy_move(self.curr_pokemon_ref, self.enemy_pokemon)[0]
        predicted_enemy_move_utility = predicted_enemy_move[2]
        switch_utilities = evaluate_switch_utility(self.curr_pokemon_ref, self.bot_team, predicted_enemy_move, self.enemy_pokemon)

        best_option_move_index = 0
        best_option_switch_index = 0

        if forced_action == ACTION.SWITCH:
            while True:
                best_switch_index = switch_utilities[best_option_switch_index][0]

                if self.switch_validity(best_switch_index):
                    await super().make_switch(best_switch_index)
                    break
                else:
                    best_option_switch_index += 1

                if best_option_switch_index == 6:
                    raise ValueError("All moves are not available")

        elif forced_action == ACTION.MOVE:
            while True:
                best_move_index = move_utilities[best_option_move_index][0]

                if self.move_validity(best_move_index):
                    await super().make_move(best_move_index)
                    break
                else:
                    best_option_move_index += 1

                if best_option_move_index == 4:
                    raise ValueError("All moves are not available")

        else:
            while True:
                print("switch_utilities:")
                print(switch_utilities)
                print("move_utilities:")
                print(move_utilities)
                # The first [] means the action, when [0] is the best action
                # The second [] means: [0] for index, [1] for Move, [2] for utility
                best_move_utility = move_utilities[best_option_move_index][2] - predicted_enemy_move_utility
                best_move_index = move_utilities[best_option_move_index][0]
                best_switch_utility = switch_utilities[best_option_switch_index][2]
                best_switch_index = switch_utilities[best_option_switch_index][0]

                if best_switch_utility <= best_move_utility:
                    print("Better move...")
                    if self.move_validity(best_move_index):
                        await super().make_move(best_move_index)
                        print(f'i wanted to use {best_move_index} which is {move_utilities[best_option_switch_index][1].name}')
                        break
                    else:
                        print(f'Couldnt use {move_utilities[best_option_switch_index][1].name}')
                        best_option_move_index += 1
                else:
                    print("Better switch...")
                    if self.switch_validity(best_switch_index):
                        await super().make_switch(best_switch_index)
                        break
                    else:
                        best_option_switch_index += 1

                if best_option_move_index == 4 and best_option_switch_index == 6:
                    await sender.send_message(super().battle_id, 'The bot has been crushed')
                    await sender.forfeit(super().battle_id)
                    raise ValueError("All switches and moves are not available")
