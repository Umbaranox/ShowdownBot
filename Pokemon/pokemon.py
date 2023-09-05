from abc import ABC
import json
import requests

MAX_MOVES_COUNT = 4


class Pokemon(ABC):
    def __init__(self, name, level, condition):
        self.name = name
        self.url = "https://pokeapi.co/api/v2/pokemon/" + name.lower().replace(" ", "-")  # For API data
        self.types = self.set_types()
        self.level = level
        if '/' in condition:
            self.max_health = condition.split('/')[1]
            self.curr_health = condition.split('/')[0]
        else:  # Pokemon has fainted
            self.max_health = 0
            self.curr_health = 0

    def get_field_from_api(self, singular: str, plural: str):
        print("URL: ", self.url)
        # print("JSN: ", requests.get(self.url).json())
        try:
            response = requests.get(self.url).json()
            field_info_json = response.get(plural, [])
            wished_list = [field_info[singular]["name"] for field_info in field_info_json]
            return wished_list
        except ValueError:
            print("There is a problem with the name", self.name)

    def set_types(self) -> list[str]:
        return self.get_field_from_api("type", "types")

    def __str__(self) -> str:
        return f"Name: {self.name}\nLevel: {self.level}\nCondition: {self.curr_health}/{self.max_health}"

    def is_alive(self) -> bool:
        return self.curr_health == 0


class BotPokemon(Pokemon):
    def __init__(self, name, level, condition, active, stats, moves, ability, item, terastall_type):
        super().__init__(name, level, condition)
        self.active = active
        self.stats = stats
        self.moves = moves
        self.ability = ability
        self.item = item
        self.terastall_type = terastall_type

    def __str__(self):
        return f"{super().__str__()}\nActive: {self.active}\nStats: {self.stats}\nMoves: {', '.join(self.moves)}\nAbility: {self.ability}\nItem: {self.item}\nTerastall Type: {self.terastall_type}"

    def get_moves(self):
        return self.moves

    def get_stats(self):
        return self.stats

    def get_ability(self):
        return self.ability

    def get_item(self):
        return self.item

    def get_terastall_type(self):
        return self.terastall_type


def create_pokemon_objects_from_json(json_data) -> list[Pokemon]:
    """This function gets a json and create pokemons"""
    # TODO: Right now, this function create 6 pokemons every turn. It'll be more eff to create only the changed objects.
    pokemon_objects = []

    # Load JSON data
    data = json.loads(json_data.replace("|request|", ""))

    if 'side' in data and 'pokemon' in data['side']:
        for pokemon_info in data['side']['pokemon']:
            name = pokemon_info.get('ident', '')[4:]
            level = pokemon_info.get('details', '').split(',')[1][-2:]
            condition = pokemon_info.get('condition', '')
            active = pokemon_info.get('active', False)
            stats = pokemon_info.get('stats', {})  # Extracted stats data
            moves = pokemon_info.get('moves', [])  # Extracted moves data
            ability = pokemon_info.get('ability', '')  # Extracted ability data
            item = pokemon_info.get('item', '')  # Extracted item data
            terastall_type = pokemon_info.get('teraType', '')  # Extracted terastall_type data

            # Create a BotPokemon object and append it to the list
            bot_pokemon = BotPokemon(name, level, condition, active, stats, moves, ability, item, terastall_type)
            pokemon_objects.append(bot_pokemon)

    return pokemon_objects


class EnemyPokemon(Pokemon):
    def __init__(self, name, level, condition):
        super().__init__(name, level, condition)
        self.active = False  # By default
        self.stats = self.set_stats()
        self.moves = self.set_potential_moves()
        self.abilities = self.set_potential_abilities()

    def set_stats(self):
        response = requests.get(self.url).json()["stats"]

        # Initialize an empty dictionary
        stat_dict = {}

        # Iterate through the list of dictionaries
        for stat_info in response:
            # Extract the "name" and "base_stat" values
            stat_name = stat_info["stat"]["name"]
            base_stat = stat_info["base_stat"]

            # Add the stat to the dictionary
            stat_dict[stat_name] = base_stat

        # return the resulting dictionary
        return stat_dict

    def set_potential_moves(self):
        return super().get_field_from_api("move", "moves")

    def set_potential_abilities(self):
        return super().get_field_from_api("ability", "abilities")
