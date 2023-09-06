import json
import configparser
from pathlib import Path
import requests
from web_socket.sender import Sender
from web_socket.constant_variable import USERNAME, PASSWORD


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
