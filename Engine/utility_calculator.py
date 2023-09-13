from Engine.move import Move, MoveCategory
from Engine.pokemon import Pokemon, BotPokemon, EnemyPokemon, MAX_MOVES
from Engine.type import string_to_type, TypeChart


def evaluate_attacking_move_utility(attacking_pokemon: Pokemon, optional_moves: list[Move], defending_pokemon: Pokemon) -> list[(int, Move, float)]:
    """
    Calculate the utility for each move of the attacking Pokemon when facing a defending Pokemon,
    and create a sorted list of (index, move name, utility) tuples, where list[0] represents the predicted move.

    Args:
        attacking_pokemon (Pokemon): The Pokemon that is attacking.
        optional_moves (list[Move]): List of moves that the attacking Pokemon can choose from.
        defending_pokemon (Pokemon): The defending Pokemon against which the utility is calculated.

    Returns:
        list[(int, Move, float)]: A sorted list of tuples containing move index, move object, and utility,
        sorted in descending order of utility.
    Raises:
        ValueError: If attacking_pokemon or defending_pokemon is None, or if attacking_pokemon is the same as defending_pokemon.
    """
    if attacking_pokemon is None:
        raise ValueError(f'Active Pokemon is None')
    if defending_pokemon is None:
        raise ValueError(f'Enemy Pokemon is None')
    if attacking_pokemon is defending_pokemon:
        raise ValueError("Pokemon can't attack itself")

    move_utilities = []

    for index, move in enumerate(optional_moves):
        # The basic utility formula
        print("here:")
        print(move)
        print(move.name)
        utility = move.accu * move.power

        # STAB bonus (Same Type Attack Bonus)
        if move.type in attacking_pokemon.types:
            utility *= 1.2

        # Calculate the effectiveness against the enemy Pokemon's types
        print("Enemy:", defending_pokemon)
        print("Types:", defending_pokemon.types)
        print("Types:", defending_pokemon.types[0])
        for enemy_pokemon_type in defending_pokemon.types:
            utility *= TypeChart.get_type_effectiveness(string_to_type(move.type), string_to_type(enemy_pokemon_type))

        # Physical/Special calculation
        if move.move_category == MoveCategory.PHYSICAL:
            utility *= attacking_pokemon.stats['atk'] / defending_pokemon.stats['def']
        elif move.move_category == MoveCategory.SPECIAL:
            utility *= attacking_pokemon.stats['spa'] / defending_pokemon.stats['spd']

        print("Calculated utility:", utility)

        # Append a tuple containing move index, name, and utility to the list
        move_utilities.append((index, move, utility))

        # print("Calculated utility's tuple:", move_utilities[index])

    if 1 < len(move_utilities):
        # Sort the list of move index, name, and utility tuples in descending order of utility
        move_utilities = sorted(move_utilities, key=lambda x: x[2], reverse=True)

    return move_utilities  # Return the sorted list of move index, name, and utility tuples


def evaluate_enemy_move(active_pokemon: BotPokemon, enemy_pokemon: EnemyPokemon) -> list[(int, Move, float)]:
    """
    Evaluate the potential moves that the enemy Pokemon might use against the active Pokemon.

    This function calculates the utility of each move that the enemy Pokemon can use, including its known moves
    and potential moves, and returns a sorted list of tuples containing move index, move object, and utility,
    sorted in descending order of utility.

    Args:
        active_pokemon (BotPokemon): The active Pokemon controlled by the bot.
        enemy_pokemon (EnemyPokemon): The enemy Pokemon for which move utilities are evaluated.

    Returns:
        list[(int, Move, float)]: A sorted list of tuples containing move index, move object, and utility,
        sorted in descending order of utility.
    """

    enemy_moves = enemy_pokemon.known_moves.copy()

    if len(enemy_pokemon.known_moves) < MAX_MOVES - 1:
        # If the given enemy hasn't used all its moves yet, assume it can make an average damage with its own type(s)
        enemy_moves.extend(create_potential_moves(enemy_pokemon))

    sorted_enemy_move_utilities = evaluate_attacking_move_utility(enemy_pokemon, enemy_moves, active_pokemon)
    return sorted_enemy_move_utilities


def create_potential_moves(enemy_pokemon: EnemyPokemon) -> list[Move]:
    """
    Create potential moves for an enemy Pokemon based on its types and stats.

    This function generates potential moves for an enemy Pokemon by creating moves of a fixed power and accuracy
    for each type the enemy Pokemon possesses. The move category (Physical or Special) is determined based on
    the enemy Pokemon's better attacking stat (Attack or Special Attack).

    Args:
        enemy_pokemon (EnemyPokemon): The enemy Pokemon for which potential moves are created.

    Returns:
        list[Move]: A list of potential Move objects for the enemy Pokemon.
    """
    potential_moves = []

    for enemy_type in enemy_pokemon.types:
        potential_move = Move("potential", "10", False, enemy_type, 60, 100, 0, None)
        # Use the enemy's better attacking stat:
        if enemy_pokemon.stats['atk'] < enemy_pokemon.stats['spa']:
            potential_move.move_category = MoveCategory.SPECIAL
        else:
            potential_move.move_category = MoveCategory.PHYSICAL
        potential_moves.append(potential_move)

    return potential_moves


def evaluate_switch_utility(active_pokemon: Pokemon, bot_team: list[Pokemon], predicted_move: Move, enemy_pokemon: Pokemon) -> list[(int, Pokemon, float)]:
    """
    Evaluate the utility of switching each available bot Pokemon against a predicted enemy move.

    This function calculates the utility of switching each available bot Pokemon on the team against a predicted
    enemy move. The utility is determined by evaluating the predicted enemy move's effectiveness against each bot
    Pokemon. The resulting list is sorted in descending order of utility, indicating the best switch options.

    Args:
        active_pokemon (Pokemon): The currently active bot Pokemon.
        bot_team (list[Pokemon]): A list of bot's available Pokemon for switching.
        predicted_move (Move): The predicted enemy move to evaluate against.
        enemy_pokemon (Pokemon): The enemy Pokemon making the predicted move.

    Returns:
        list[(int, Pokemon, float)]: A list of tuples containing the index of the bot Pokemon, the bot Pokemon itself,
        and the calculated utility for switching to that Pokemon.
    """
    switch_utilities = []

    for index, bot_pokemon in enumerate(bot_team):
        if active_pokemon.name == bot_pokemon.name:
            # It can't be switched to itself
            continue

        # Check if the Pokemon is fainted, and if so, skip checking it
        if not bot_pokemon.is_alive():
            continue

        utility = evaluate_attacking_move_utility(enemy_pokemon, [predicted_move[1]], bot_pokemon)[0][2]
        utility = -1 * utility  # Negative utility
        switch_utilities.append((index, bot_pokemon, utility))

    # Sort the list of (pokemon index, pokemon, utility) tuples in descending order of utility
    sorted_switch_utilities = sorted(switch_utilities, key=lambda x: x[2], reverse=True)

    return sorted_switch_utilities
