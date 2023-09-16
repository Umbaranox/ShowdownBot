import unittest
from unittest.mock import patch
from Engine.pokemon import create_pokemon_objects_from_json
from BattleBots.battle_bot import BattleBot


class Test(unittest.TestCase):
    def setUp(self) -> None:
        # Create a bot
        self.bot_instance = BattleBot()
        # Create a team
        json_data = """{"active":[{"moves":[{"move":"Close Combat","id":"closecombat","pp":8,"maxpp":8,"target":"normal","disabled":true},{"move":"Icicle Crash","id":"iciclecrash","pp":16,"maxpp":16,"target":"normal","disabled":true},{"move":"Aqua Jet","id":"aquajet","pp":32,"maxpp":32,"target":"normal","disabled":true},{"move":"Earthquake","id":"earthquake","pp":15,"maxpp":16,"target":"allAdjacent","disabled":false}],"canTerastallize":"Fighting"}],"side":{"name":"joshcoco","id":"p2","pokemon":[{"ident":"p2: Beartic","details":"Beartic, L90, M","condition":"213/317","active":true,"stats":{"atk":285,"def":195,"spa":177,"spd":195,"spe":141},"moves":["closecombat","iciclecrash","aquajet","earthquake"],"baseAbility":"slushrush","item":"choiceband","pokeball":"pokeball","ability":"slushrush","commanding":false,"reviving":false,"teraType":"Fighting","terastallized":""},{"ident":"p2: Zoroark","details":"Zoroark, L78, F","condition":"222/222","active":false,"stats":{"atk":168,"def":139,"spa":232,"spd":139,"spe":209},"moves":["nastyplot","sludgebomb","darkpulse","psychic"],"baseAbility":"illusion","item":"lifeorb","pokeball":"pokeball","ability":"illusion","commanding":false,"reviving":false,"teraType":"Poison","terastallized":""},{"ident":"p2: Tropius","details":"Tropius, L89, M","condition":"320/320","active":false,"stats":{"atk":126,"def":199,"spa":179,"spd":206,"spe":142},"moves":["protect","airslash","leechseed","substitute"],"baseAbility":"harvest","item":"sitrusberry","pokeball":"pokeball","ability":"harvest","commanding":false,"reviving":false,"teraType":"Steel","terastallized":""},{"ident":"p2: Ceruledge","details":"Ceruledge, L78, F","condition":"245/245","active":false,"stats":{"atk":240,"def":170,"spa":139,"spd":201,"spe":178},"moves":["swordsdance","bitterblade","closecombat","shadowsneak"],"baseAbility":"weakarmor","item":"heavydutyboots","pokeball":"pokeball","ability":"weakarmor","commanding":false,"reviving":false,"teraType":"Fire","terastallized":""},{"ident":"p2: Medicham","details":"Medicham, L86, M","condition":"243/243","active":false,"stats":{"atk":152,"def":178,"spa":152,"spd":178,"spe":187},"moves":["icepunch","poisonjab","closecombat","zenheadbutt"],"baseAbility":"purepower","item":"choicescarf","pokeball":"pokeball","ability":"purepower","commanding":false,"reviving":false,"teraType":"Fighting","terastallized":""},{"ident":"p2: Magearna","details":"Magearna, L78","condition":"0 fnt","active":false,"stats":{"atk":153,"def":224,"spa":248,"spd":224,"spe":146},"moves":["flashcannon","voltswitch","aurasphere","fleurcannon"],"baseAbility":"soulheart","item":"choicespecs","pokeball":"pokeball","ability":"soulheart","commanding":false,"reviving":false,"teraType":"Fairy","terastallized":""}]},"rqid":5}"""
        self.bot_team = create_pokemon_objects_from_json(json_data)

    def test_get_lives_count(self):
        # Assert that the given team has 5 alive
        self.assertEqual(BattleBot.get_lives_count_of_bot_pokemon(self.bot_team), 5)

        # Get a request copy where 1 Pokemon is alive
        json_data = """{"active":[{"moves":[{"move":"Close Combat","id":"closecombat","pp":8,"maxpp":8,"target":"normal","disabled":true},{"move":"Icicle Crash","id":"iciclecrash","pp":16,"maxpp":16,"target":"normal","disabled":true},{"move":"Aqua Jet","id":"aquajet","pp":32,"maxpp":32,"target":"normal","disabled":true},{"move":"Earthquake","id":"earthquake","pp":15,"maxpp":16,"target":"allAdjacent","disabled":false}],"canTerastallize":"Fighting"}],"side":{"name":"joshcoco","id":"p2","pokemon":[{"ident":"p2: Beartic","details":"Beartic, L90, M","condition":"0 fnt","active":true,"stats":{"atk":285,"def":195,"spa":177,"spd":195,"spe":141},"moves":["closecombat","iciclecrash","aquajet","earthquake"],"baseAbility":"slushrush","item":"choiceband","pokeball":"pokeball","ability":"slushrush","commanding":false,"reviving":false,"teraType":"Fighting","terastallized":""},{"ident":"p2: Zoroark","details":"Zoroark, L78, F","condition":"0 fnt","active":false,"stats":{"atk":168,"def":139,"spa":232,"spd":139,"spe":209},"moves":["nastyplot","sludgebomb","darkpulse","psychic"],"baseAbility":"illusion","item":"lifeorb","pokeball":"pokeball","ability":"illusion","commanding":false,"reviving":false,"teraType":"Poison","terastallized":""},{"ident":"p2: Tropius","details":"Tropius, L89, M","condition":"0 fnt","active":false,"stats":{"atk":126,"def":199,"spa":179,"spd":206,"spe":142},"moves":["protect","airslash","leechseed","substitute"],"baseAbility":"harvest","item":"sitrusberry","pokeball":"pokeball","ability":"harvest","commanding":false,"reviving":false,"teraType":"Steel","terastallized":""},{"ident":"p2: Ceruledge","details":"Ceruledge, L78, F","condition":"0 fnt","active":false,"stats":{"atk":240,"def":170,"spa":139,"spd":201,"spe":178},"moves":["swordsdance","bitterblade","closecombat","shadowsneak"],"baseAbility":"weakarmor","item":"heavydutyboots","pokeball":"pokeball","ability":"weakarmor","commanding":false,"reviving":false,"teraType":"Fire","terastallized":""},{"ident":"p2: Medicham","details":"Medicham, L86, M","condition":"0 fnt","active":false,"stats":{"atk":152,"def":178,"spa":152,"spd":178,"spe":187},"moves":["icepunch","poisonjab","closecombat","zenheadbutt"],"baseAbility":"purepower","item":"choicescarf","pokeball":"pokeball","ability":"purepower","commanding":false,"reviving":false,"teraType":"Fighting","terastallized":""},{"ident":"p2: Magearna","details":"Magearna, L78","condition":"253/253","active":false,"stats":{"atk":153,"def":224,"spa":248,"spd":224,"spe":146},"moves":["flashcannon","voltswitch","aurasphere","fleurcannon"],"baseAbility":"soulheart","item":"choicespecs","pokeball":"pokeball","ability":"soulheart","commanding":false,"reviving":false,"teraType":"Fairy","terastallized":""}]},"rqid":5}"""
        another_team = create_pokemon_objects_from_json(json_data)

        self.assertEqual(BattleBot.get_lives_count_of_bot_pokemon(another_team), 1)

    def test_find_enemy_pokemon_by_name_finds(self):
        # Define the Pokemon name to search for
        pokemon_name = 'Zoroark'

        # Call the find_enemy_pokemon_by_name method
        pokemon_pointer_by_name = BattleBot.find_enemy_pokemon_by_name(self.bot_team, pokemon_name)

        # Define the expected Pokemon object
        expected_pokemon = self.bot_team[1]

        # Assert that the found Pokemon's name matches the expected name
        self.assertEqual(expected_pokemon.name, 'Zoroark')

        # Assert that the found Pokemon object is the same as the expected object
        self.assertIs(pokemon_pointer_by_name, expected_pokemon)

    def test_find_enemy_pokemon_by_name_throws(self):
        # Define an invalid Pokemon name
        pokemon_name = 'bADnAmE'

        # Use a context manager to catch the expected ValueError
        with self.assertRaises(ValueError):
            # Call the find_enemy_pokemon_by_name method with the invalid name
            BattleBot.find_enemy_pokemon_by_name(self.bot_team, pokemon_name)

    def test_find_enemy_pokemon_by_name_fainted_warning(self):
        # Define the name of a fainted Pokemon
        pokemon_name = 'Magearna'

        # Use a context manager to capture printed output
        with patch('builtins.print') as mock_print:
            # Call the find_enemy_pokemon_by_name method
            BattleBot.find_enemy_pokemon_by_name(self.bot_team, pokemon_name)

        # Check if the warning message is printed as expected
        mock_print.assert_called_once_with(f'Warning! {pokemon_name} found but he is fainted')




if __name__ == '__main__':
    unittest.main()
