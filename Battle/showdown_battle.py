from abc import ABC, abstractmethod
from enum import Enum
from Pokemon.team import Team
import json
from Pokemon.pokemon import create_pokemon_objects_from_json, EnemyPokemon
from Pokemon.move import create_active_moves_list


class Battle(ABC):
    def __init__(self, battle_id: str, sender):
        self.battle_id = battle_id
        self.player_id = None
        self.sender = sender
        self.bot_team = Team()
        self.enemy_team = Team()
        self.curr_pokemon_data = None
        self.curr_pokemon_ref = None
        self.active_moves = None
        # Data:
        self.turn = 0

    def get_bot_team(self):
        return self.bot_team

    def get_enemy_team(self):
        return self.enemy_team

    def get_lives_count_of_bot_pokemon(self) -> int:
        return sum(1 for pokemon in self.bot_team if not pokemon.is_alive())

    # getters...

    async def update_bot_team(self, request: str):
        """
        Parse and translate json send by server. Reload bot team and the current pokemon's moves. Called each turn.
        :param request: json sent by server.
        """

        try:
            updated_team = create_pokemon_objects_from_json(request)
            self.bot_team = updated_team

        except RuntimeError:
            print("Error in update team")

        json_data = json.loads(request)
        self.turn += 1  # 2?

        if 'forceSwitch' in json_data.keys():
            await self.make_action(self.sender, Battle.ACTION.SWITCH)

        elif 'active' in json_data.keys():
            self.curr_pokemon_data = json_data['active']

            try:
                active_moves = create_active_moves_list(request)
                self.active_moves = active_moves
            except RuntimeError:
                print("Error in update active moves")

        for pokemon in self.bot_team:
            if pokemon.active:
                self.curr_pokemon_ref = pokemon



    async def update_enemy_team(self, pokemon_name: str, level: str, condition: str):
        """
        Called in the first turn and anytime the enemy is switching pokemon.
        The enemy team objects contain the pokemon that were shown in the field.

        :param pokemon_name: The name of the enemy Pokémon.
        :param level: The level of the enemy Pokémon.
        :param condition: The condition of the enemy Pokémon in the format "current_health/max_health".
        """
        for enemy_pokemon in self.enemy_team.team:
            enemy_pokemon.active = False

        # Get the object of the given Pokemon
        found_pokemon = next((pokemon for pokemon in self.enemy_team.team if pokemon.name == pokemon_name), None)

        if found_pokemon is not None:
            # If the Pokemon is known, updates its data
            found_pokemon.active = True
            found_pokemon.max_health = condition.split('/')[1]
            found_pokemon.curr_health = condition.split('/')[0]
        else:
            # If the Pokemon is not known yet, create an object and add it to the enemy team
            new_enemy_pokemon = EnemyPokemon(pokemon_name, level, condition)
            new_enemy_pokemon.active = True
            self.enemy_team.add(new_enemy_pokemon)

    async def make_team_order(self):
        """
        Call function to correctly choose the first pokemon to send.
        :param websocket: Websocket stream.
        """
        order = ''.join([str(x[0]) for x in self.bot_team.team])
        await self.sender.send(self.battle_id, f'/team {order}', str(self.turn))

    class ACTION(Enum):
        NONE = "none"
        MOVE = "move"
        SWITCH = "switch"

    @abstractmethod
    async def make_action(self, sender, forced_action=ACTION.NONE):
        pass

    async def make_move(self, value: int):
        # TODO: handle error
        await self.sender.send_move(self.battle_id, value)

    def move_validity(self, value: int) -> bool:
        print("Check move validity:", self.active_moves[value - 1].is_possible())
        # Can't make a move with no pp or which is disabled
        return self.active_moves[value - 1].is_possible()

    async def make_switch(self, value: int):
        # TODO: handle error
        await self.sender.send_switch(self.battle_id, value)

    def switch_validity(self, value: int) -> bool:
        chosen_pokemon = self.bot_team[value - 1]

        # Can't switch to a fainted pokemon
        if chosen_pokemon.curr_health == 0:
            print("Rechoose switch")
            return False

        # Can't switch to the active pokemon
        if chosen_pokemon.active:
            print("Rechoose switch")
            return False

        return True
