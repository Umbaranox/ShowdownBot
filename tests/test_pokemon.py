import unittest
from Pokemon.pokemon import create_pokemon_objects_from_json, EnemyPokemon


class TestPokemonCreation(unittest.TestCase):
    def test_bot_pokemon_creation(self):
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
                        "moves": ["moonblast", "reflect", "bodypress", "lightscreen"],
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
                        "moves": ["dragondance", "glaiverush", "iciclecrash", "earthquake"],
                        "ability": "thermalexchange",
                        "item": "heavydutyboots",
                        "teraType": "Ground",
                        "active": false
                    }
                ]
            }
        }"""

        # Call the function to create Pokemon objects
        pokemon_objects = create_pokemon_objects_from_json(json_data)

        # Perform assertions to check if the objects were created correctly
        self.assertEqual(len(pokemon_objects), 2)

        self.assertEqual(pokemon_objects[0].name, "Carbink")
        self.assertEqual(pokemon_objects[0].level, "90")
        self.assertEqual(pokemon_objects[0].max_health, "236")
        self.assertEqual(pokemon_objects[0].curr_health, "236")
        self.assertEqual(pokemon_objects[0].active, True)
        self.assertEqual(pokemon_objects[0].stats, {'atk': 95, 'def': 321, 'spa': 141, 'spd': 321, 'spe': 141})
        self.assertEqual(pokemon_objects[0].moves, ["moonblast", "reflect", "bodypress", "lightscreen"])
        self.assertEqual(pokemon_objects[0].ability, "sturdy")
        self.assertEqual(pokemon_objects[0].item, "lightclay")
        self.assertEqual(pokemon_objects[0].terastall_type, "Water")
        self.assertEqual(pokemon_objects[0].types, ['rock', 'fairy'])

        # Check types on pokemon with one type (Copperajah):
        self.assertEqual(pokemon_objects[1].types, ['steel'])

    def test_enemy_pokemon_creation_abs_fields(self):
        enemy_pokemon = EnemyPokemon("Carbink", "90", "236/236")

        self.assertEqual(enemy_pokemon.name, "Carbink")
        self.assertEqual(enemy_pokemon.level, "90")
        self.assertEqual(enemy_pokemon.max_health, "236")
        self.assertEqual(enemy_pokemon.curr_health, "236")

    def test_enemy_pokemon_creation_moves_abilities(self):
        enemy_pokemon = EnemyPokemon("Carbink", "90", "236/236")

        self.assertEqual(enemy_pokemon.moves,
                         ['tackle', 'body-slam', 'take-down', 'hyper-beam', 'rock-throw', 'toxic', 'psychic',
                          'double-team', 'harden', 'light-screen', 'reflect', 'flash', 'explosion', 'rest',
                          'rock-slide', 'sharpen', 'substitute', 'snore', 'flail', 'protect', 'spikes', 'sandstorm',
                          'endure', 'charm', 'swagger', 'sleep-talk', 'return', 'frustration', 'safeguard',
                          'hidden-power', 'rain-dance', 'sunny-day', 'psych-up', 'ancient-power', 'hail', 'facade',
                          'nature-power', 'magic-coat', 'skill-swap', 'secret-power', 'rock-tomb', 'sand-tomb',
                          'iron-defense', 'covet', 'calm-mind', 'rock-blast', 'gravity', 'gyro-ball', 'guard-swap',
                          'magnet-rise', 'rock-polish', 'power-gem', 'earth-power', 'giga-impact', 'flash-cannon',
                          'trick-room', 'iron-head', 'stone-edge', 'stealth-rock', 'guard-split', 'wonder-room',
                          'telekinesis', 'smack-down', 'heavy-slam', 'after-you', 'round', 'ally-switch',
                          'misty-terrain', 'moonblast', 'confide', 'dazzling-gleam', 'stomping-tantrum', 'body-press',
                          'meteor-beam', 'misty-explosion', 'terrain-pulse', 'tera-blast'])
        self.assertEqual(enemy_pokemon.abilities, ['clear-body', 'sturdy'])

    def test_enemy_pokemon_creation_stats(self):
        enemy_pokemon = EnemyPokemon("Carbink", "90", "236/236")

        expected_dict = {'hp': 50, 'attack': 50, 'defense': 150, 'special-attack': 50, 'special-defense': 150,
                         'speed': 50}
        self.assertEqual(expected_dict, enemy_pokemon.stats)


if __name__ == '__main__':
    unittest.main()
