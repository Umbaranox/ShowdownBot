import json
import configparser
from pathlib import Path
import requests
from web_socket.sender import Sender

# Load configuration settings from 'config.ini' file
config = configparser.ConfigParser()
config.read(Path('..').parent.absolute() / 'config.ini')
USERNAME = config['bot']['username']
PASSWORD = config['bot']['password']
OWNER = config['bot']['owner']


async def log_in(challid: str, chall: str):
    """
    Log in to the Pokémon Showdown server.

    This function performs the login process to connect to the Pokémon Showdown server
    using the provided challenge ID and challenge.
    """
    sender = Sender()

    # Send a POST request to log in with the provided credentials
    resp = requests.post(
        'https://play.pokemonshowdown.com/action.php?',
        data={
            'act': 'login',
            'name': USERNAME,
            'pass': PASSWORD,
            'challstr': f'{challid}%7C{chall}'
        }
    )

    # Log in with the generated assertion
    await sender.send_message('', f'/trn {USERNAME},0,{json.loads(resp.text[1:])["assertion"]}')

    # Change the user's avatar (optional)
    await sender.send_message('', '/avatar aaron')
