import configparser
from enum import Enum
from pathlib import Path

# Explain, from config
config = configparser.ConfigParser()
config.read(Path('..').parent.absolute() / 'config.ini')
USERNAME = config['bot']['username']
PASSWORD = config['bot']['password']
OWNER = config['bot']['owner']


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
