import unittest
from Engine import utility_calculator
from Engine.pokemon import EnemyPokemon, BotPokemon, create_pokemon_objects_from_json
from Engine.move import Move
from BattleBots.greedy_bot import GreedyBot


class Test(unittest.TestCase):
    def setUp(self):
        # Creating a variable that simulating "known_moves"
        self.move1 = Move("Tackle", "40", False)
        self.move2 = Move("Glare", "35", False)
        self.move3 = Move("Earthquake", "22", False)
        self.move4 = Move("Stone Edge", "30", False)
        self.known_moves = [self.move1, self.move2, self.move3, self.move4]

        # Creating variables that simulating Bot's pokemon and Enemy's pokemon
        self.enemy_pokemon = EnemyPokemon("Charizard", "50", "100/100")
        json_data = """{
            "side": {
                "pokemon": [
                    {
                        "ident": "p2: Carbink",
                        "details": "Carbink, L90",
                        "condition": "236/236",
                        "stats": {
                            "atk": 95,
                            "def": 321,
                            "spa": 141,
                            "spd": 321,
                            "spe": 141
                        },
                        "known_moves": ["moonblast", "reflect", "bodypress", "lightscreen"],
                        "ability": "sturdy",
                        "item": "lightclay",
                        "teraType": "Water",
                        "active": true
                    },
                    {
                        "ident": "p2: Copperajah",
                        "details": "Copperajah, L75, F",
                        "condition": "296/296",
                        "stats": {
                            "atk": 261,
                            "def": 182,
                            "spa": 156,
                            "spd": 173,
                            "spe": 174
                        },
                        "known_moves": ["dragondance", "glaiverush", "iciclecrash", "earthquake"],
                        "ability": "thermalexchange",
                        "item": "heavydutyboots",
                        "teraType": "Ground",
                        "active": false
                    }
                ]
            }
        }"""
        self.bot_pokemon = create_pokemon_objects_from_json(json_data)[0]

    def test_setUp_creation(self):
        # Assert the variables representing the wished objects (Full tested in other files)
        self.assertEqual(self.known_moves[0].name, "Tackle")
        self.assertEqual(self.enemy_pokemon.name, "Charizard")
        self.assertEqual(self.bot_pokemon.name, "Carbink")

    def test_evaluate_attacking_move_utility(self):
        utility_list = utility_calculator.evaluate_attacking_move_utility(self.bot_pokemon, self.known_moves,
                                                                          self.enemy_pokemon)
        self.assertEqual(len(utility_list), 4)

        # Type checking
        index = utility_list[0][0]
        name = utility_list[0][1]
        utility = utility_list[0][2]
        self.assertEqual(type(index), int)
        self.assertEqual(type(name), Move)
        self.assertEqual(type(utility), float)

        # Order is correct
        self.assertLessEqual(utility_list[3][2], utility_list[2][2])
        self.assertLessEqual(utility_list[2][2], utility_list[1][2])
        self.assertLessEqual(utility_list[1][2], utility_list[0][2])

    def test_evaluate_attacking_move_utility_when_enemy_attack(self):
        # Now let the enemy be the attacker:
        utility_list = utility_calculator.evaluate_attacking_move_utility(self.enemy_pokemon, self.known_moves,
                                                                          self.bot_pokemon)
        self.assertEqual(len(utility_list), 4)

    def test_throws_if_pok_attack_itself(self):
        with self.assertRaises(ValueError):
            utility_calculator.evaluate_attacking_move_utility(self.enemy_pokemon, self.known_moves, self.enemy_pokemon)

        with self.assertRaises(ValueError):
            utility_calculator.evaluate_attacking_move_utility(self.bot_pokemon, self.known_moves, self.bot_pokemon)

    def test_throws_if_pokemon_is_fainted(self):
        fainted_pok = EnemyPokemon("Charizard", "50", "100/100")
        fainted_pok.curr_health = 0

        with self.assertRaises(ValueError):
            utility_calculator.evaluate_attacking_move_utility(self.bot_pokemon, self.known_moves, fainted_pok)

    # TODO: tests for evaluate_enemy_move

    def test_create_potential_moves(self):
        # Assert enemy pokemon has no known moves:
        self.assertEqual(len(self.enemy_pokemon.known_moves), 0)

        # Call a function to create potential_moves
        potential_moves = utility_calculator.create_potential_moves(self.enemy_pokemon)

        # Make sure that 2 potential moves created
        self.assertEqual(len(potential_moves), 2)

        # Make sure those moves didn't stay on the object
        self.assertEqual(len(self.enemy_pokemon.known_moves), 0)


if __name__ == '__main__':
    unittest.main()
