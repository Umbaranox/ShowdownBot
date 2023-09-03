from Pokemon.pokemon import Pokemon

TEAM_SIZE = 6


class Team:
    def __init__(self):
        self.team = []
        self.isPlaying = False  # add in game -> true

    def __int__(self, other_team: list[Pokemon]):
        self.team = []
        for pokemon in other_team:
            self.add(pokemon)

    def add(self, pokemon: Pokemon):
        if TEAM_SIZE <= len(self.team):
            raise RuntimeError(f"Failed to add {pokemon.name}. Team can contain up to 6 Pokemons")
        self.team.append(pokemon)

    def add(self, pokemons: list[Pokemon]):
        for pokemon in pokemons:
            self.add(pokemon)

    def get_current_pokemon(self):
        if not self.isPlaying:
            raise RuntimeError("Failed to get current pokemon. Team is not playing.")
        # add
        pass

    def get_team_copy(self):
        """Get a copy of a given player's team"""
        return self.team.copy()

    def get_pokemon_by_index(self, index):
        return self.team[index]

    def get_lives(self):
        """BAD FUNCTION"""
        lives = []

        for pokemon in self.get_team_copy():
            if pokemon.is_alive():
                lives.insert(pokemon)
        return lives

    def remove_pok(self, mon):
        if mon in self.team:
            self.team.remove(mon)
        else:
            raise ValueError("Mon not found in the team")

    def __contains__(self, pokemon_name: str) -> bool:
        return any(pokemon.name == pokemon_name for pokemon in self.team)
