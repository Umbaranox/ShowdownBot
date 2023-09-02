import json
import configparser
from pathlib import Path
import requests
from sender import Sender

config = configparser.ConfigParser()
config.read(Path('..').parent.absolute() / 'config.ini')
USERNAME = config['bot']['username']
PASSWORD = config['bot']['password']
OWNER = config['bot']['owner']


async def log_in(challid: str, chall: str):
    sender = Sender()
    resp = requests.post(
        'https://play.pokemonshowdown.com/action.php?',
        data={
            'act': 'login',
            'name': USERNAME,
            'pass': PASSWORD,
            'challstr': f'{challid}%7C{chall}'
        }
    )
    await sender.send_message('', f'/trn {USERNAME},0,{json.loads(resp.text[1:])["assertion"]}')
    await sender.send_message('', '/avatar aaron')
