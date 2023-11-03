from BattleBots.battle_bot import BattleBot
from Engine.utility_calculator import evaluate_attacking_move_utility, evaluate_enemy_move, evaluate_switch_utility, get_utilities
from constant_variable import ACTION


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
        # Call the super()'s method
        await super().update_enemy_team(pokemon_name, level, condition)

        # Get a reference to the current enemy pokemon
        curr_enemy_pokemon = next((pokemon for pokemon in self.enemy_team.team if pokemon.name == pokemon_name), None)

        # If it wasn't found, it means there's a problem with the update method
        if curr_enemy_pokemon is None:
            raise ValueError(f'Enemy pokemon {pokemon_name} is not found, although it is updated. We have only {[pokemon.name for pokemon in self.enemy_team.team]}')

        # Update the self.enemy_pokemon field
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

        # Get the crucial data
        move_utilities, predicted_enemy_move, predicted_enemy_move_utility, switch_utilities = \
            get_utilities(self.curr_pokemon_ref, self.enemy_pokemon, self.active_moves, self.bot_team)

        # Set 2 variables to point on the best move and switch indexes, starting by 0
        best_option_move_index = 0
        best_option_switch_index = 0

        if forced_action == ACTION.SWITCH:
            # If the action must be an switch, use the best that possible
            while True:
                best_switch_index = switch_utilities[best_option_switch_index][0]

                if self.switch_validity(best_switch_index):
                    await super().make_switch(best_switch_index)
                    break
                else:
                    # In case the i-th switch is not valid, use the i+1 switch
                    best_option_switch_index += 1

                if best_option_switch_index == 6:
                    # If all switches are not possible and the program forced to use switch, it means there's a problem
                    raise ValueError("All moves are not available")

        elif forced_action == ACTION.MOVE:
            # If the action must be an switch, use the best that possible
            while True:
                best_move_index = move_utilities[best_option_move_index][0]

                if self.move_validity(best_move_index):
                    await super().make_move(best_move_index)
                    break
                else:
                    # In case the i-th move is not valid, use the i+1 move
                    best_option_move_index += 1

                if best_option_move_index == 4:
                    # If all moves are not possible and the program forced to use move, it means there's a problem
                    raise ValueError("All moves are not available")

        else:
            while True:
                # Calculate the utility of th best move and each switch
                best_move_utility = move_utilities[best_option_move_index][2] - predicted_enemy_move_utility
                best_move_index = move_utilities[best_option_move_index][0]
                best_switch_utility = switch_utilities[best_option_switch_index][2]
                best_switch_index = switch_utilities[best_option_switch_index][0]

                if best_switch_utility <= best_move_utility:
                    # Decide to make move or switch based on their given utility
                    if self.move_validity(best_move_index):
                        await super().make_move(best_move_index)
                        break
                    else:
                        best_option_move_index += 1
                else:
                    if self.switch_validity(best_switch_index):
                        await super().make_switch(best_switch_index)
                        break
                    else:
                        best_option_switch_index += 1

                if best_option_move_index == 4 and best_option_switch_index == 6:
                    # If all moves and switches are not available, it means there's a problem
                    await sender.send_message(super().battle_id, 'The bot has been crushed')
                    await sender.forfeit(super().battle_id)
                    raise ValueError("All switches and moves are not available")
