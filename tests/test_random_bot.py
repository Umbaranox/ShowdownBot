import unittest


class TestBattleActions(unittest.TestCase):

    # async def test_make_random_action(self):
    #     random_actions = []
    #     for _ in range(100):
    #         random_actions.append(RandomBot.pick_random_action())
    #
    #     # Check if all generated actions are either MOVE or SWITCH
    #     valid_actions = [action for action in random_actions if action in [ACTION.MOVE, ACTION.SWITCH]]
    #     self.assertEqual(len(valid_actions), len(random_actions))

    def test_make_action(self):
        pass


if __name__ == '__main__':
    unittest.main()
