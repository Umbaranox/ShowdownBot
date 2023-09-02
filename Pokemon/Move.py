class Move:
    def __init__(self, name, move_type):
        self.name = name
        self.type = move_type
        self.accu = 1
        self.pp = 10
        self.priority = 0
        self.disabled = False

    def is_move_disabled(self):
        return self.disabled

    def disable_move(self):
        self.disabled = True

    def enable_move(self):
        self.disabled = False

    def is_possible(self):
        return self.disabled is False and self.pp > 0


class AttackMove(Move):
    def __init__(self, name, move_type, atk_or_spa, dmg):
        Move.__init__(self, name, move_type)
        self.atk_or_spa = atk_or_spa  # 0 - atk, 1 - spa
        self.dmg = dmg

    def get_move_utility(self):
        """Let utility(attack) = attack.dmg * attack.accu"""
        return self.dmg * self.accu


# class StatusMove(Move):
#     def __init__(self, name, dmg):
#         Move.__init__(self)
#         self.effect
#
#     def get_move_utility(self):
#         return self.dmg

