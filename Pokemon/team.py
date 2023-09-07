from Pokemon.pokemon import Pokemon

TEAM_SIZE = 6


class Team:
    """
    The Team class manages a player's team in a Pokemon battle.

    Attributes:
        team (list): A list containing the Pokemon on the team.
    """
    def __init__(self):
        """
        Initializes an empty team.
        """
        self.team = []

    def __int__(self, other_team: list[Pokemon]):
        """
        Initializes a team with Pokemon from another team.
        Args:
            other_team (list[Pokemon]): A list of Pokemon to add to the team.
        """
        self.team = []
        for pokemon in other_team:
            self.add(pokemon)

    def add(self, pokemon: Pokemon) -> None:
        """
        Adds a Pokemon to the team if there is room and the type matches.
        Args:
            pokemon (Pokemon): The Pokemon to add to the team.
        Raises:
            RuntimeError: If the team is full.
            ValueError: If the Pokemon's type doesn't match the team's type or if a Pokemon with the same name is
                        already on the team.
        """
        if TEAM_SIZE <= len(self.team):
            raise RuntimeError(f"Failed to add {pokemon.name}. Team can contain up to 6 Pokemons")

        # Check if the team is empty or if the new Pokemon's type matches the existing type
        # This avoids situations of BotPokemon and EnemyPokemon in the same team
        if not self.team or isinstance(self.team[0], type(pokemon)):
            # Check if the team contains a pokemon with the same name, and raise error if so
            for pok in self.team:
                if pok.name == pokemon.name:
                    raise ValueError(
                        f"Failed to add {pokemon.name}. Team can have one instance of a pokemon.")
            self.team.append(pokemon)
        else:
            raise ValueError(f"Failed to add {pokemon.name}. Team can only contain BotPokemons or EnemyPokemons.")

    def adds(self, pokemons: list[Pokemon]) -> None:
        """
        Adds multiple Pokemon to the team.
        Args:
            pokemons (list[Pokemon]): A list of Pokemon to add to the team.
        """
        for pokemon in pokemons:
            self.add(pokemon)

    def get_team_copy(self):
        """
        Get a copy of the team.
        Returns:
            list: A copy of the team's Pokemon.
        """
        return self.team.copy()

    def get_pokemon_by_index(self, index: int) -> Pokemon:
        """
        Retrieves a Pokemon from the team by its index.
        Args:
            index: The index of the Pokemon to retrieve.
        Returns:
            Pokemon: The Pokemon at the specified index.
        """
        return self.team[index]

    def __contains__(self, pokemon_name: str) -> bool:
        """
        Checks if a Pokemon with a specific name is on the team.
        Args:
            pokemon_name (str): The name of the Pokemon to check for.
        Returns:
            bool: True if a Pokemon with the specified name is on the team, otherwise False.
        """
        return any(pokemon.name == pokemon_name for pokemon in self.team)
