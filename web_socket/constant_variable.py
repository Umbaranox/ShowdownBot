from enum import Enum


class BOT_MODE(Enum):
    STANDBY = 0  # Wait to a command
    CHALLENGE_OWNER = 1  # Send challenge req to owner
    ACCEPT_CHALLENGE = 2  # Expect to challenge req from owner and accept it
    SEARCH = 3  # Search a fight in a given mode


# List of available formats to play
FORMATS = [
    "gen9randombattle"
]

BATTLES = []  # A list of all current fights
MAX_BATTLES_COUNT = 1
CUR_BATTLES_COUNT = 0

URL_API = 'https://pokeapi.co/api/v2/'


class ACTION(Enum):
    NONE = "none"
    MOVE = "move"
    SWITCH = "switch"

    def __str__(self):
        return self.name.lower()

