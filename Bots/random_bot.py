import time
from Battle.showdown_battle import Battle
import random


class RandomBot(Battle):
    """This is a test class for Battle class"""

    def __init__(self, battle_id: str, sender):
        super().__init__(battle_id, sender)

    async def make_action(self, sender, forced_action=Battle.ACTION.NONE):

        if forced_action is Battle.ACTION.NONE:
            # Generate a random number 1 (move) or 2 (switch)
            random_number = random.randint(1, 2)

            if random_number == 1:
                forced_action = Battle.ACTION.MOVE
            else:
                forced_action = Battle.ACTION.SWITCH

        if forced_action == Battle.ACTION.MOVE:
            print("CHOSE: MOVE")
        # move
            random_number = random.randint(1, 4)
            await sender.send_message(self.battle_id, "I picked a move")
            await super().make_move(random_number)
        else:
            print("CHOSE: SWITCH")
            # switch
            random_number = random.randint(1, 6)
            await sender.send_message(self.battle_id, "I picked a switch")
            await super().make_switch(random_number)
