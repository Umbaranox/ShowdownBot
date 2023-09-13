import unittest
from Engine.utility_calculator import evaluate_attacking_move_utility, evaluate_enemy_move, create_potential_moves, \
    evaluate_switch_utility
from Engine.pokemon import EnemyPokemon, BotPokemon, create_pokemon_objects_from_json
from Engine.move import Move, MoveCategory, create_active_moves_list
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
        bot_pokemons = create_pokemon_objects_from_json(json_data)
        self.bot_pokemon = bot_pokemons[0]
        self.bot_pokemon2 = bot_pokemons[1]

    def test_setUp_creation(self):
        # Assert the variables representing the wished objects (Full tested in other files)
        self.assertEqual(self.known_moves[0].name, "Tackle")
        self.assertEqual(self.enemy_pokemon.name, "Charizard")
        self.assertEqual(self.bot_pokemon.name, "Carbink")

    def test_evaluate_attacking_move_utility(self):
        utility_list = evaluate_attacking_move_utility(self.bot_pokemon, self.known_moves, self.enemy_pokemon)
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
        utility_list = evaluate_attacking_move_utility(self.enemy_pokemon, self.known_moves, self.bot_pokemon)
        self.assertEqual(len(utility_list), 4)

    def test_evaluate_attacking_move_throws_if_pok_attack_itself(self):
        with self.assertRaises(ValueError):
            evaluate_attacking_move_utility(self.enemy_pokemon, self.known_moves, self.enemy_pokemon)

        with self.assertRaises(ValueError):
            evaluate_attacking_move_utility(self.bot_pokemon, self.known_moves, self.bot_pokemon)

    def test_evaluate_attacking_move_throws_if_pokemon_is_fainted(self):
        fainted_pok = EnemyPokemon("Charizard", "50", "100/100")
        fainted_pok.curr_health = 0

        with self.assertRaises(ValueError):
            evaluate_attacking_move_utility(self.bot_pokemon, self.known_moves, fainted_pok)

    def test_evaluate_attacking_move_STAB(self):
        # Create an enemy Pokemon for the test
        normal_pokemon = EnemyPokemon("Persian", "90", "300/300")

        # Create identical moves with and without STAB
        move_with_type = Move("RockMove", "10", False, 'rock', 60, 100, 0, MoveCategory.PHYSICAL)
        move_without_type = Move("NormalMove", "10", False, 'normal', 60, 100, 0, MoveCategory.PHYSICAL)

        # Calculate the utility using the utility calculator function
        utility_list = evaluate_attacking_move_utility(self.bot_pokemon, [move_with_type, move_without_type],
                                                       normal_pokemon)

        # Retrieve the utility values for the moves
        utility_of_move_with_type = utility_list[0][2]
        utility_of_move_without_type = utility_list[1][2]

        # Assert that the move with STAB has 1.2 times the utility of the move without STAB
        self.assertEqual(utility_of_move_with_type, utility_of_move_without_type * 1.2)

    def test_evaluate_enemy_move(self):
        # Test with an enemy Pokemon that has one type and no known moves
        enemy_with_one_type = EnemyPokemon("Persian", "90", "300/300")
        sorted_utility = evaluate_enemy_move(self.bot_pokemon, enemy_with_one_type)

        # Ensure that the function takes care of 2 potential moves
        self.assertEqual(len(sorted_utility), 2)

        # Test with an enemy Pokemon that has two types and no known moves (using Charizard as an example)
        enemy_with_two_types = self.enemy_pokemon
        sorted_utility = evaluate_enemy_move(self.bot_pokemon, enemy_with_two_types)

        # Ensure that the function takes care of 1 potential move
        self.assertEqual(len(sorted_utility), 1)

        # Test with an enemy Pokemon that has 4 known moves (no potential moves should be created)
        enemy_with_two_types.known_moves = self.known_moves
        sorted_utility = evaluate_enemy_move(self.bot_pokemon, enemy_with_two_types)

        # Ensure that no potential moves were created, and it evaluates all 4 known moves
        self.assertEqual(len(sorted_utility), 4)

    def test_create_potential_moves(self):
        # Assert enemy pokemon has no known moves:
        self.assertEqual(len(self.enemy_pokemon.known_moves), 0)

        # Call a function to create potential_moves
        potential_moves = create_potential_moves(self.enemy_pokemon)

        # Make sure that 2 potential moves created
        self.assertEqual(len(potential_moves), 2)

        # Make sure those moves didn't stay on the object
        self.assertEqual(len(self.enemy_pokemon.known_moves), 0)

    def test_evaluate_switch_utility(self):
        json = """{"active":[{"moves":[{"move":"Close Combat","id":"closecombat","pp":8,"maxpp":8,"target":"normal","disabled":true},{"move":"Icicle Crash","id":"iciclecrash","pp":16,"maxpp":16,"target":"normal","disabled":true},{"move":"Aqua Jet","id":"aquajet","pp":32,"maxpp":32,"target":"normal","disabled":true},{"move":"Earthquake","id":"earthquake","pp":15,"maxpp":16,"target":"allAdjacent","disabled":false}],"canTerastallize":"Fighting"}],"side":{"name":"joshcoco","id":"p2","pokemon":[{"ident":"p2: Beartic","details":"Beartic, L90, M","condition":"213/317","active":true,"stats":{"atk":285,"def":195,"spa":177,"spd":195,"spe":141},"moves":["closecombat","iciclecrash","aquajet","earthquake"],"baseAbility":"slushrush","item":"choiceband","pokeball":"pokeball","ability":"slushrush","commanding":false,"reviving":false,"teraType":"Fighting","terastallized":""},{"ident":"p2: Zoroark","details":"Zoroark, L78, F","condition":"222/222","active":false,"stats":{"atk":168,"def":139,"spa":232,"spd":139,"spe":209},"moves":["nastyplot","sludgebomb","darkpulse","psychic"],"baseAbility":"illusion","item":"lifeorb","pokeball":"pokeball","ability":"illusion","commanding":false,"reviving":false,"teraType":"Poison","terastallized":""},{"ident":"p2: Tropius","details":"Tropius, L89, M","condition":"320/320","active":false,"stats":{"atk":126,"def":199,"spa":179,"spd":206,"spe":142},"moves":["protect","airslash","leechseed","substitute"],"baseAbility":"harvest","item":"sitrusberry","pokeball":"pokeball","ability":"harvest","commanding":false,"reviving":false,"teraType":"Steel","terastallized":""},{"ident":"p2: Ceruledge","details":"Ceruledge, L78, F","condition":"245/245","active":false,"stats":{"atk":240,"def":170,"spa":139,"spd":201,"spe":178},"moves":["swordsdance","bitterblade","closecombat","shadowsneak"],"baseAbility":"weakarmor","item":"heavydutyboots","pokeball":"pokeball","ability":"weakarmor","commanding":false,"reviving":false,"teraType":"Fire","terastallized":""},{"ident":"p2: Medicham","details":"Medicham, L86, M","condition":"243/243","active":false,"stats":{"atk":152,"def":178,"spa":152,"spd":178,"spe":187},"moves":["icepunch","poisonjab","closecombat","zenheadbutt"],"baseAbility":"purepower","item":"choicescarf","pokeball":"pokeball","ability":"purepower","commanding":false,"reviving":false,"teraType":"Fighting","terastallized":""},{"ident":"p2: Magearna","details":"Magearna, L78","condition":"253/253","active":false,"stats":{"atk":153,"def":224,"spa":248,"spd":224,"spe":146},"moves":["flashcannon","voltswitch","aurasphere","fleurcannon"],"baseAbility":"soulheart","item":"choicespecs","pokeball":"pokeball","ability":"soulheart","commanding":false,"reviving":false,"teraType":"Fairy","terastallized":""}]},"rqid":5}"""
        bot_team = create_pokemon_objects_from_json(json)
        active_pokemon = bot_team[0]

        enemy_pokemon = self.enemy_pokemon
        predicted_move = Move("GenericMove", "10", False, 'fire', 90, 100, 0, MoveCategory.SPECIAL)
        enemy_pokemon.known_moves.append(predicted_move)

        predicted_move = evaluate_enemy_move(active_pokemon, enemy_pokemon)[0]

        print("Dmg to active: ", predicted_move[2])

        switches_utility = evaluate_switch_utility(active_pokemon, bot_team, predicted_move, enemy_pokemon)

        self.assertEqual(len(switches_utility), 5)


if __name__ == '__main__':
    unittest.main()
