from BattleBots.battle_bot import BattleBot
# from Engine.utility_calculator import
from web_socket.constant_variable import ACTION


class GreedyBot(BattleBot):
    def __init__(self, battle_id: str, sender):
        super().__init__(battle_id, sender)
        self.enemy_pokemon = None

    async def make_action(self, sender, forced_action=ACTION.NONE):
        pass

    def evaluate_enemy_move(self):
        pass
