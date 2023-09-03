from datetime import datetime


class Sender:
    def __new__(cls, _=None):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Sender, cls).__new__(cls)
        return cls.instance

    def __init__(self, websocket=None):
        if not hasattr(self, 'websocket'):
            self.websocket = websocket
        if not self.websocket:
            raise ValueError('Field "websocket" needs to be initialised at least one time.')

    async def send_message(self, room: str, *messages: str):
        """
        Default websocket sender. Format message, log and send websocket.
        :param room: Room name.
        :param messages: List of messages to send.
        """
        string = f'{room}|{"|".join(messages)}'
        print(f'[{datetime.now().replace(microsecond=0).isoformat()}] >> {string}')
        await self.websocket.send(string)

    async def search_game_in_format(self, battle_format: str):
        message = f'/search {battle_format}'
        await self.send_message('', message)

    async def challenge_user(self, player: str, battle_format: str):
        message = f'/challenge {player}, {battle_format}'
        await self.send_message('', message)

    async def accept_challenge(self, player: str):
        message = f'/accept {player}'
        await self.send_message('', message)

    async def send_move(self, battle_tag: str, move: int):
        message = f'/choose move {move}'
        await self.send_message(battle_tag, message)

    async def send_switch(self, battle_tag: str, pokemon: int, turn: int):
        message = f'/choose switch {pokemon}'
        await self.send_message(battle_tag, message, str(turn))

    async def leave(self, battle_tag: str):
        await self.send_message('', f'/leave {battle_tag}')

    async def forfeit(self, battle_tag: str):
        await self.send_message(battle_tag, '/forfeit')
        await self.leave(battle_tag)

    @classmethod
    def get_instance(cls):
        return cls.instance
