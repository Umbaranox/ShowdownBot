import json
from abc import ABC, abstractmethod
from Pokemon.team import Team
from Pokemon.pokemon import create_pokemon_objects_from_json, EnemyPokemon
from Pokemon.move import create_active_moves_list
from web_socket.constant_variable import ACTION


class BattleBot(ABC):
    """
    Abstract base class representing a bot designed for battling in a game.

    This abstract base class defines the common attributes and methods that a battling bot should have.

    Attributes:
        battle_id (str): The identifier for the current battle.
        player_id (NoneType): The identifier for the player controlled by the bot.
        sender: A tool for sending messages and commands in the battle.
        bot_team (Team): The team of the bot's Pokemon.
        enemy_team (Team): The team of the enemy's Pokemon.
        curr_pokemon_data (dict): The data of the current Pokemon in battle.
        curr_pokemon_ref: The reference to the current Pokemon in battle.
        active_moves: The move list of the active pokemon's.
        turn (int): The current turn number in the battle.

    Note:
        This class serves as a foundation for implementing specific bots that participate in battles.
    """
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
        """
        Get the count of bot's Pokemon that are not alive.

        Returns:
            int: The count of bot's Pokemon that are not alive.
        """
        return sum(1 for pokemon in self.bot_team if not pokemon.is_alive())

    def find_enemy_pokemon_by_name(self, pokemon_name):
        found_pokemon = next((pokemon for pokemon in self.enemy_team.team if pokemon.name == pokemon_name), None)
        if found_pokemon is None:
            raise RuntimeError("Error in looking for an enemy pokemon")
        return found_pokemon

    # getters...

    async def update_bot_team(self, request: str) -> None:
        """
        Updates the bot team's status and actions based on the provided JSON request.

        This function processes a JSON request containing information about the bot's team and battle state. It creates updated
        Pokemon objects and sets them as the new bot team. It also checks if a switch is forced or if there are active known_moves
        for the current Pokemon. Additionally, it updates the current turn and the reference to the currently active Pokemon.

        Args:
            request (str): A JSON-formatted string containing information about the bot's team and battle state.

        Returns:
            None
        """

        # To update the bot team, create updated objects and set them as the new team
        try:
            updated_team = create_pokemon_objects_from_json(request)
            self.bot_team = updated_team

        except RuntimeError:
            print("Error in update team")

        # Parse the JSON data from the request
        json_data = json.loads(request)

        # Increment the turn counter
        self.turn += 1

        # Checks if a switch is forced
        if 'forceSwitch' in json_data.keys():
            await self.make_action(self.sender, ACTION.SWITCH)

        # Check if the current pokemon is the active
        elif 'active' in json_data.keys():
            self.curr_pokemon_data = json_data['active']

            # Gets its optional known_moves
            try:
                active_moves = create_active_moves_list(request)
                self.active_moves = active_moves
                # print("Active known_moves:")
                # for move in self.active_moves:
                #     print(move.name + ": ", str(move.power), " / ", str(move.accu))
                # print("/Active known_moves:")
            except RuntimeError:
                print("Error in updating active known_moves")

        # Update the reference to the currently active Pokemon
        for pokemon in self.bot_team:
            if pokemon.active:
                self.curr_pokemon_ref = pokemon

    async def update_enemy_team(self, pokemon_name: str, level: str, condition: str) -> None:
        """
        Updates the enemy team with the given Pokemon's information.

        This function sets all enemy Pokemon to be inactive and then updates the data of the specified Pokemon. If the
        specified Pokemon is not known, it creates a new object and adds it to the enemy team.

        Args:
            pokemon_name (str): The name of the Pokemon.
            level (str): The level of the Pokemon.
            condition (str): The condition in a format "current_health/max_health".

        Returns:
            None
        """
        # Make every enemy Pokemon not active
        for enemy_pokemon in self.enemy_team.team:
            enemy_pokemon.active = False

        # Get the object of the given Pokemon
        found_pokemon = next((pokemon for pokemon in self.enemy_team.team if pokemon.name == pokemon_name), None)

        if found_pokemon is not None:
            # If the Pokemon is known, updates its data
            found_pokemon.active = True
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

    @abstractmethod
    async def make_action(self, sender, forced_action=ACTION.NONE):
        """
        Perform a battle action in response to a game event.

        This abstract method should be implemented in bots subclasses to define the behavior of making a battle
        action in response to a game event.

        Args:
            sender:  A  tool for sending messages and commands.
            forced_action (ACTION, optional): A forced action to be performed. Defaults to `ACTION.NONE`.

        Returns:
            None
        """
        pass

    async def make_move(self, value: int):
        # TODO: handle error
        await self.sender.send_move(self.battle_id, value)

    def move_validity(self, value: int) -> bool:
        # print("Check move validity:", self.active_moves[value - 1].is_possible())
        # Can't make a move with no pp or which is disabled
        return self.active_moves[value - 1].is_possible()

    async def make_switch(self, value: int):
        # TODO: handle error
        await self.sender.send_switch(self.battle_id, value)

    def switch_validity(self, value: int) -> bool:
        chosen_pokemon = self.bot_team[value - 1]

        # Can't switch to a fainted pokemon
        if chosen_pokemon.curr_health == 0:
            return False

        # Can't switch to the active pokemon
        if chosen_pokemon.active:
            return False

        return True
