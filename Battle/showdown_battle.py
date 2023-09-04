from abc import ABC, abstractmethod
from enum import Enum

from web_socket.sender import Sender
from Pokemon.team import Team
import json
from Pokemon.pokemon import create_pokemon_objects_from_json, EnemyPokemon


class Battle(ABC):
    def __init__(self, battle_id: str, sender):
        self.battle_id = battle_id
        self.player_id = None
        self.sender = sender
        self.bot_team = Team()
        self.enemy_team = Team()
        self.curr_pokemon = None
        # Data:
        self.turn = 0

    def get_bot_team(self):
        return self.bot_team

    def get_enemy_team(self):
        return self.enemy_team

    # getters...

    async def update_bot_team(self, request: str):
        """
        Parse and translate json send by server. Reload bot team. Called each turn.
        :param request: json sent by server.
        """
        json_data = json.loads(request)
        self.turn += 1  # 2?

        try:
            updated_team = create_pokemon_objects_from_json(request)
            self.bot_team = updated_team
        except RuntimeError:
            print("Error in update team")

        if 'forceSwitch' in json_data.keys():
            await self.make_action(self.sender, Battle.ACTION.SWITCH)

        elif 'active' in json_data.keys():
            self.curr_pokemon = json_data['active']


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

    async def make_switch(self, value: int):
        # TODO: handle error
        await self.sender.send_switch(self.battle_id, value)
