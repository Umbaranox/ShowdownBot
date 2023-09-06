from BattleBots.battle_bot import BattleBot
from web_socket.constant_variable import ACTION


class GreedyBot(BattleBot):
    def __init__(self, battle_id: str, sender):
        super().__init__(battle_id, sender)
        self.enemy_pokemon = None

    async def make_action(self, sender, forced_action=ACTION.NONE):

        pass

    def evaluate_move_utility(self):
        """For each move of the active Pokemon, calculate utility and create a sorted list of (move name, utility)."""

        move_utilities = []  # Create an empty list to store move name and utility pairs

        for move in super().active_moves:
            utility = move.accu * move.power

            if move.type == super().curr_pokemon_ref.type:
                utility *= 1.2

            # more ...

            # Append a tuple containing move name and utility to the list
            move_utilities.append((move.name, utility))

        # Sort the list of move name and utility pairs in descending order of utility
        sorted_move_utilities = sorted(move_utilities, key=lambda x: x[1], reverse=True)

        return sorted_move_utilities  # Return the sorted list of move name and utility pairs

    def evaluate_enemy_move(self):
        pass
