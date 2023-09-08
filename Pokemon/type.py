from enum import Enum, auto


class Type(Enum):
    FIRE = auto()
    WATER = auto()
    ELECTRIC = auto()
    GRASS = auto()
    ICE = auto()
    FIGHTING = auto()
    POISON = auto()
    GROUND = auto()
    FLYING = auto()
    PSYCHIC = auto()
    BUG = auto()
    ROCK = auto()
    GHOST = auto()
    DRAGON = auto()
    DARK = auto()
    STEEL = auto()
    FAIRY = auto()
    NORMAL = auto()


def string_to_type(type_str):
    """
    Converts a string to a Type Enum.

    Args:
        type_str (str): The type string to convert.

    Returns:
        Type: The corresponding Type Enum value.

    Raises:
        ValueError: If the provided type string is not a valid type.
    """
    type_mapping = {
        "FIRE": Type.FIRE,
        "WATER": Type.WATER,
        "ELECTRIC": Type.ELECTRIC,
        "GRASS": Type.GRASS,
        "ICE": Type.ICE,
        "FIGHTING": Type.FIGHTING,
        "POISON": Type.POISON,
        "GROUND": Type.GROUND,
        "FLYING": Type.FLYING,
        "PSYCHIC": Type.PSYCHIC,
        "BUG": Type.BUG,
        "ROCK": Type.ROCK,
        "GHOST": Type.GHOST,
        "DRAGON": Type.DRAGON,
        "DARK": Type.DARK,
        "STEEL": Type.STEEL,
        "FAIRY": Type.FAIRY,
        "NORMAL": Type.NORMAL,
    }

    # Convert to uppercase for case-insensitivity
    type_enum = type_mapping.get(type_str.upper())

    if type_enum is None:
        raise ValueError(f"Invalid type: {type_str}")

    return type_enum


class TypeChart:
    """
    Class for handling type effectiveness in battles.
    """

    @staticmethod
    def get_weaknesses(given_type: Type) -> list[Type]:
        """
        Get the weaknesses of a given type.

        Args:
            given_type (Type): The type to get weaknesses for.

        Returns:
            list[Type]: A list of types that are weaknesses for the given type.
        """
        weakness = {
            Type.FIRE: [Type.WATER, Type.ROCK, Type.GROUND],
            Type.WATER: [Type.ELECTRIC, Type.GRASS],
            Type.ELECTRIC: [Type.GROUND],
            Type.GRASS: [Type.FIRE, Type.ICE, Type.POISON, Type.FLYING, Type.BUG],
            Type.ICE: [Type.FIRE, Type.FIGHTING, Type.ROCK, Type.STEEL],
            Type.FIGHTING: [Type.FLYING, Type.PSYCHIC, Type.FAIRY],
            Type.POISON: [Type.GROUND, Type.PSYCHIC],
            Type.GROUND: [Type.WATER, Type.GRASS, Type.ICE],
            Type.FLYING: [Type.ELECTRIC, Type.ICE, Type.ROCK],
            Type.PSYCHIC: [Type.BUG, Type.GHOST, Type.DARK],
            Type.BUG: [Type.FIRE, Type.FLYING, Type.ROCK],
            Type.ROCK: [Type.WATER, Type.GRASS, Type.FIGHTING, Type.GROUND, Type.STEEL],
            Type.GHOST: [Type.GHOST, Type.DARK],
            Type.DRAGON: [Type.ICE, Type.DRAGON, Type.FAIRY],
            Type.DARK: [Type.FIGHTING, Type.BUG, Type.FAIRY],
            Type.STEEL: [Type.FIRE, Type.FIGHTING, Type.GROUND],
            Type.FAIRY: [Type.POISON, Type.STEEL],
            Type.NORMAL: [Type.FIGHTING]
        }
        return weakness.get(given_type, [])

    @staticmethod
    def get_resistances(given_type: Type) -> list[Type]:
        """
        Get the resistances of a given type.

        Args:
            given_type (Type): The type to get resistances for.

        Returns:
            list[Type]: A list of types that are resistances for the given type.
        """
        resistance = {
            Type.FIRE: [Type.FIRE, Type.GRASS, Type.ICE, Type.BUG, Type.STEEL, Type.FAIRY],
            Type.WATER: [Type.WATER, Type.FIRE, Type.ICE, Type.STEEL],
            Type.ELECTRIC: [Type.ELECTRIC, Type.FLYING, Type.STEEL],
            Type.GRASS: [Type.WATER, Type.ELECTRIC, Type.GRASS, Type.GROUND],
            Type.ICE: [Type.ICE],
            Type.FIGHTING: [Type.BUG, Type.ROCK, Type.DARK],
            Type.POISON: [Type.GRASS, Type.FIGHTING, Type.POISON, Type.BUG, Type.FAIRY],
            Type.GROUND: [Type.POISON, Type.ROCK],
            Type.FLYING: [Type.GRASS, Type.FIGHTING, Type.BUG],
            Type.PSYCHIC: [Type.FIGHTING, Type.PSYCHIC],
            Type.BUG: [Type.GRASS, Type.FIGHTING, Type.GROUND],
            Type.ROCK: [Type.NORMAL, Type.FIRE, Type.POISON, Type.FLYING],
            Type.GHOST: [Type.POISON, Type.BUG],
            Type.DRAGON: [Type.FIRE, Type.WATER, Type.ELECTRIC, Type.GRASS],
            Type.DARK: [Type.GHOST, Type.PSYCHIC, Type.DARK],
            Type.STEEL: [Type.NORMAL, Type.GRASS, Type.ICE, Type.FLYING, Type.PSYCHIC, Type.BUG, Type.ROCK, Type.DRAGON,
                         Type.STEEL, Type.FAIRY],
            Type.FAIRY: [Type.FIGHTING, Type.BUG, Type.DRAGON],
            Type.NORMAL: []
        }

        return resistance.get(given_type, [])

    @staticmethod
    def get_immunities(given_type: Type) -> list[Type]:
        """
        Get the immunities of a given type.

        Args:
            given_type (Type): The type to get immunities for.

        Returns:
            list[Type]: A list of types that are immunities for the given type.
        """
        immunity = {
            Type.NORMAL: [Type.GHOST],
            Type.GROUND: [Type.ELECTRIC],
            Type.FLYING: [Type.GROUND],
            Type.DARK: [Type.PSYCHIC],
            Type.GHOST: [Type.NORMAL, Type.FIGHTING],
            Type.FAIRY: [Type.DRAGON]
        }

        return immunity.get(given_type, [])

    @staticmethod
    def get_type_effectiveness(attacking_type: Type, defending_type: Type) -> float:
        """
        Get the effectiveness of an attacking type against a defending type.

        Args:
            attacking_type (Type): The type of the attacking move.
            defending_type (Type): The type of the target Pokemon.

        Returns:
            float: The effectiveness of the attack (x0, x0.5, x1, or x2).
        """
        if defending_type == Type.NORMAL:
            return 1.0

        if attacking_type in TypeChart.get_immunities(defending_type):
            return 0.0
        elif attacking_type in TypeChart.get_resistances(defending_type):
            return 0.5
        elif attacking_type in TypeChart.get_weaknesses(defending_type):
            return 2.0
        else:
            return 1.0
