from Engine.move import Move, MoveCategory
from Engine.pokemon import Pokemon, BotPokemon, EnemyPokemon, MAX_MOVES
from Engine.type import string_to_type, TypeChart


def evaluate_attacking_move_utility(active_pokemon: Pokemon, optional_moves: list[Move],
                                    enemy_pokemon: Pokemon) -> list[(str, float)]:
    """For each move of the active Pokemon, calculate utility and create a sorted list of (move name, utility)."""

    if active_pokemon is enemy_pokemon:
        raise ValueError("Pokemon can't attack itself")
    if active_pokemon.is_alive() or enemy_pokemon.is_alive():
        raise ValueError("A fainted pokemon can't attack or be attacked")

    move_utilities = []  # Create an empty list to store move name and utility pairs

    for move in optional_moves:
        # The basic utility formula
        utility = move.accu * move.power

        # STAB bonus
        if move.type in active_pokemon.types:
            utility *= 1.2

        # Calculate the effectiveness against the enemy pokemon's types
        for enemy_pokemon_type in enemy_pokemon.types:
            utility *= TypeChart.get_type_effectiveness(string_to_type(move.type),
                                                        string_to_type(enemy_pokemon_type))

        if move.move_category == MoveCategory.PHYSICAL:
            utility *= active_pokemon.stats['atk'] / enemy_pokemon.stats['def']
        elif move.move_category == MoveCategory.SPECIAL:
            utility *= active_pokemon.stats['spa'] / enemy_pokemon.stats['spd']

        # Append a tuple containing move name and utility to the list
        move_utilities.append((move.name, utility))

    # Sort the list of move name and utility pairs in descending order of utility
    sorted_move_utilities = sorted(move_utilities, key=lambda x: x[1], reverse=True)

    return sorted_move_utilities  # Return the sorted list of move name and utility pairs


def evaluate_enemy_move(active_pokemon: BotPokemon, enemy_pokemon: EnemyPokemon) -> list[(str, float)]:
    """Evaluating the move the enemy might use"""

    enemy_moves = enemy_pokemon.known_moves.copy()

    if len(enemy_pokemon.known_moves) < MAX_MOVES - 1:
        # If the given enemy didn't use all of his move yet, assuming he can make an average damage with its own type(s)
        enemy_moves.extend(create_potential_moves(enemy_pokemon))

    sorted_enemy_move_utilities = evaluate_attacking_move_utility(enemy_pokemon, enemy_moves, active_pokemon)
    return sorted_enemy_move_utilities


def create_potential_moves(enemy_pokemon: EnemyPokemon) -> list[Move]:
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


# TODO: Test it
def evaluate_switch_utility(active_pokemon: Pokemon, bot_team: list[Pokemon], predicted_move: Move,
                            enemy_pokemon: Pokemon) -> list[(str, float)]:
    # Calculating the utility of the predicted move of the enemy against each pokemon in the bot's team
    switch_utilities = []

    for bot_pokemon in bot_team:
        if active_pokemon.name == bot_pokemon.name:
            # It can't be switched to itself
            continue

        # Check if the Pokemon is fainted, and if so, skip checking it
        # if bot_pokemon.is_alive():
        #     continue

        utility = -1 * evaluate_attacking_move_utility(enemy_pokemon, [predicted_move], bot_pokemon)
        switch_utilities.append((bot_pokemon.name, utility))

    # Sort the list of (pokemon name, utility) pairs in descending order of utility
    sorted_switch_utilities = sorted(switch_utilities, key=lambda x: x[1], reverse=True)

    return sorted_switch_utilities
