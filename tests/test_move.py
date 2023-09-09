import unittest
from Engine.move import Move, create_active_moves_list


class TestMove(unittest.TestCase):
    def test_move_creation(self):
        move = Move("Shadow Sneak", "48", False)

        self.assertEqual(move.name, "Shadow Sneak")
        self.assertEqual(move.pp, "48")
        self.assertEqual(move.disabled, False)
        self.assertEqual(type(move.disabled), bool)

        move = Move("Armor Cannon", "8", True)

        self.assertEqual(move.name, "Armor Cannon")
        self.assertEqual(move.pp, "8")
        print("dis?", move.disabled)
        self.assertEqual(move.disabled, True)

    def test_move_creation_data_field(self):
        move = Move("Shadow Sneak", "48", False)

        self.assertEqual(move.type, "ghost")
        self.assertEqual(type(move.type), str)
        self.assertEqual(move.power, 40)
        self.assertEqual(type(move.power), int or None)
        self.assertEqual(move.accu, 1.0)
        self.assertEqual(type(move.accu), float or None)
        self.assertEqual(move.priority, 1)
        self.assertEqual(type(move.priority), int)

    def test_create_active_moves_list(self):
        json_data = """|request|{"active":[{"known_moves":[{"move":"Coil","id":"coil","pp":32,"maxpp":32,"target":"self","disabled":false},{"move":"Glare","id":"glare","pp":48,"maxpp":48,"target":"normal","disabled":false},{"move":"Earthquake","id":"earthquake","pp":16,"maxpp":16,"target":"allAdjacent","disabled":false},{"move":"Stone Edge","id":"stoneedge","pp":8,"maxpp":8,"target":"normal","disabled":false}],"canTerastallize":"Steel"}],"side":{"name":"joshcoco","id":"p2","pokemon":[{"ident":"p2: Sandaconda","details":"Sandaconda, L84, M","condition":"258/258","active":true,"stats":{"atk":228,"def":258,"spa":157,"spd":166,"spe":167},"known_moves":["coil","glare","earthquake","stoneedge"],"baseAbility":"shedskin","item":"leftovers","pokeball":"pokeball","ability":"shedskin","commanding":false,"reviving":false,"teraType":"Steel","terastallized":""},{"ident":"p2: Pyroar","details":"Pyroar, L88, F","condition":"295/295","active":false,"stats":{"atk":124,"def":177,"spa":242,"spd":166,"spe":237},"known_moves":["workup","fireblast","hypervoice","willowisp"],"baseAbility":"unnerve","item":"heavydutyboots","pokeball":"pokeball","ability":"unnerve","commanding":false,"reviving":false,"teraType":"Fire","terastallized":""},{"ident":"p2: Gumshoos","details":"Gumshoos, L95, M","condition":"321/321","active":false,"stats":{"atk":263,"def":168,"spa":158,"spd":168,"spe":139},"known_moves":["psychicfangs","bodyslam","crunch","earthquake"],"baseAbility":"stakeout","item":"choiceband","pokeball":"pokeball","ability":"stakeout","commanding":false,"reviving":false,"teraType":"Ground","terastallized":""},{"ident":"p2: Crabominable","details":"Crabominable, L90, F","condition":"321/321","active":false,"stats":{"atk":289,"def":190,"spa":163,"spd":172,"spe":129},"known_moves":["earthquake","gunkshot","drainpunch","icehammer"],"baseAbility":"ironfist","item":"choiceband","pokeball":"pokeball","ability":"ironfist","commanding":false,"reviving":false,"teraType":"Ground","terastallized":""},{"ident":"p2: Ceruledge","details":"Ceruledge, L78, F","condition":"245/245","active":false,"stats":{"atk":240,"def":170,"spa":139,"spd":201,"spe":178},"known_moves":["swordsdance","bitterblade","closecombat","shadowsneak"],"baseAbility":"weakarmor","item":"heavydutyboots","pokeball":"pokeball","ability":"weakarmor","commanding":false,"reviving":false,"teraType":"Fire","terastallized":""},{"ident":"p2: Cresselia","details":"Cresselia, L79, F","condition":"319/319","active":false,"stats":{"atk":115,"def":219,"spa":164,"spd":235,"spe":180},"known_moves":["psyshock","moonblast","calmmind","moonlight"],"baseAbility":"levitate","item":"leftovers","pokeball":"pokeball","ability":"levitate","commanding":false,"reviving":false,"teraType":"Poison","terastallized":""}]},"rqid":3}"""

        move_list = create_active_moves_list(json_data)

        self.assertEqual(len(move_list), 4)

        self.assertEqual(move_list[0].name, "Coil")
        self.assertEqual(move_list[1].name, "Glare")
        self.assertEqual(move_list[2].name, "Earthquake")
        self.assertEqual(move_list[3].name, "Stone Edge")

    def test_is_possible(self):
        move1 = Move("Shadow Sneak", "48", False)
        move2 = Move("Armor Cannon", "8", True)
        move3 = Move("Shadow Sneak", "0", False)
        move4 = Move("Armor Cannon", "0", True)

        self.assertEqual(type(move1.is_possible()), bool)

        self.assertEqual(move1.is_possible(), True)
        self.assertEqual(move2.is_possible(), False)
        self.assertEqual(move3.is_possible(), False)
        self.assertEqual(move4.is_possible(), False)


if __name__ == '__main__':
    unittest.main()
