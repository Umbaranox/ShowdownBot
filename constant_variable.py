from enum import Enum
import configparser

# Load configuration settings from 'config.ini' file
config = configparser.ConfigParser()
config.read('config.ini')
USERNAME = config['bot']['username']
PASSWORD = config['bot']['password']
PLAYER = config['bot']['PLAYER']
URI = config['env']['URI']
SELECTED_BOT_MODE = config['Setting']['BOT_MODE']
SELECTED_BOT_TYPE = config['Setting']['BOT_TYPE']


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


def get_bot_mode():
    if SELECTED_BOT_MODE == 'accept':
        return BOT_MODE.ACCEPT_CHALLENGE
    elif SELECTED_BOT_MODE == 'challenge':
        return BOT_MODE.CHALLENGE_OWNER
    elif SELECTED_BOT_MODE == 'search':
        return BOT_MODE.SEARCH
    else:
        raise ValueError("Invalid BOT MODE in config.ini")
