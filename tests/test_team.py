import unittest
from Engine.pokemon import Pokemon, EnemyPokemon, BotPokemon, create_pokemon_objects_from_json
from Engine.team import Team


class TestTeam(unittest.TestCase):
    def setUp(self):
        # Create some Pokemon objects for testing
        self.enemy_pokemon1 = EnemyPokemon("Pikachu", "50", "100/100")
        self.enemy_pokemon2 = EnemyPokemon("Charizard", "50", "100/100")

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
        # Call a function to create BotPokemon objects
        bot_pokemon_objects = create_pokemon_objects_from_json(json_data)
        self.bot_pokemon1 = bot_pokemon_objects[0]
        self.bot_pokemon2 = bot_pokemon_objects[1]

    def test_add_pokemon(self):
        team = Team()
        team.add(self.enemy_pokemon1)
        self.assertEqual(len(team.team), 1)
        self.assertEqual(team.get_pokemon_by_index(0), self.enemy_pokemon1)

    def test_add_multiple_pokemon(self):
        team = Team()
        pokemons = [self.enemy_pokemon1, self.enemy_pokemon2]
        team.adds(pokemons)
        self.assertEqual(len(team.team), 2)
        self.assertEqual(team.get_pokemon_by_index(1), self.enemy_pokemon2)

    def test_get_team_copy(self):
        team = Team()
        team.adds([self.enemy_pokemon1, self.enemy_pokemon2])
        team_copy = team.get_team_copy()
        self.assertEqual(len(team_copy), 2)
        self.assertEqual(team_copy[0], self.enemy_pokemon1)

    def test_contains(self):
        team = Team()
        team.add(self.enemy_pokemon1)
        self.assertIn("Pikachu", team)
        self.assertNotIn("Charizard", team)

    def test_add_allow_only_bot_or_enemy_pokemon_on_team(self):
        team = Team()
        team.add(self.enemy_pokemon1)

        # Adding a bot pokemon to a team with enemy pokemon(s) should raise an exception
        with self.assertRaises(ValueError):
            team.add(self.bot_pokemon1)

        team = Team()
        team.add(self.bot_pokemon1)

        # Adding an enemy pokemon to a team with bot pokemon(s) should raise an exception
        with self.assertRaises(ValueError):
            team.add(self.enemy_pokemon1)

    def test_add_allow_only_one_instance_of_pokemon(self):
        team = Team()
        team.add(self.enemy_pokemon1)

        self.enemy_pokemon3 = EnemyPokemon("Pikachu", "51", "100/100")  # Another object of Pikachu

        # Adding a 2nd instance of a pokemon that is in the team should raise an exception
        with self.assertRaises(ValueError):
            team.add(self.enemy_pokemon1)  # The object itself
            team.add(self.enemy_pokemon3)  # Another object of the same pokemon


if __name__ == '__main__':
    unittest.main()
