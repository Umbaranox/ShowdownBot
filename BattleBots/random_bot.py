from BattleBots.battle_bot import BattleBot
import random


class RandomBot(BattleBot):
    """
    A test class for BattleBot that makes random battle actions.

    This class extends the functionality of the BattleBot class to make random battle actions, such as selecting
    random moves or switching Pokemon.
    """

    def __init__(self, battle_id: str, sender):
        super().__init__(battle_id, sender)

    async def make_action(self, sender, forced_action=BattleBot.ACTION.NONE):
        """
        Perform a battle action in response to a game event.

        This method makes random battle actions based on a forced action or a random choice between move and switch.
        """
        if forced_action is BattleBot.ACTION.NONE:
            # Generate a random number 1 (move) or 2 (switch)
            random_number = random.randint(1, 2)

            if random_number == 1:
                forced_action = BattleBot.ACTION.MOVE
            else:
                forced_action = BattleBot.ACTION.SWITCH

        if forced_action == BattleBot.ACTION.MOVE:
            # move
            while True:
                random_number = random.randint(1, 4)
                if self.move_validity(random_number):
                    # Exit the loop when a valid pick is found
                    break
            # await sender.send_message(self.battle_id, "I picked a move")
            await super().make_move(random_number)
        else:
            # switch
            while True:
                random_number = random.randint(1, 6)
                if self.switch_validity(random_number):
                    # Exit the loop when a valid pick is found
                    break
            # await sender.send_message(self.battle_id, "I picked a switch")
            await super().make_switch(random_number)
