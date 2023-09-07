"""
sender.py - Showdown Sender Module

This module provides a class for sending messages and commands to the Pokemon Showdown server.

Example:
    To use the Sender class to send a challenge to another user:
    ```
    sender = Sender()  # Initialize the Sender instance
    await sender.challenge_user("opponent_username", "gen9ou")  # Challenge the user to a Gen 9 OU battle
    ```
"""
from datetime import datetime


class Sender:
    def __new__(cls, _=None):
        """
        Initialize a new Sender instance if it doesn't already exist.

        Args:
            cls: The Sender class.
            _: Placeholder argument for class instantiation.

        Returns:
            Sender: A Sender instance.
        """
        if not hasattr(cls, 'instance'):
            cls.instance = super(Sender, cls).__new__(cls)
        return cls.instance

    def __init__(self, web_socket=None):
        """
        Initialize the Sender instance with an optional WebSocket.

        Args:
            self: The Sender instance.
            web_socket (optional): A WebSocket connection.

        Raises:
            ValueError: If the 'web_socket' field is not initialized.
        """
        if not hasattr(self, 'web_socket'):
            self.web_socket = web_socket
        if not self.web_socket:
            raise ValueError('Field "web_socket" needs to be initialized at least one time.')

    async def send_message(self, room: str, *messages: str):
        """
        Send a message to a specified room.

        Args:
            self: The Sender instance.
            room (str): The room to send the message to.
            *messages (str): Variable number of message strings to send.
        """
        string = f'{room}|{"|".join(messages)}'
        print(f'[{datetime.now().replace(microsecond=0).isoformat()}] >> {string}')
        await self.web_socket.send(string)

    async def search_game_in_format(self, battle_format: str):
        """
        Search for a game in the specified battle format.

        Args:
            self: The Sender instance.
            battle_format (str): The desired battle format to search for.
        """
        message = f'/search {battle_format}'
        await self.send_message('', message)

    async def challenge_user(self, player: str, battle_format: str):
        """
        Challenge another user to a battle in the specified format.

        Args:
            self: The Sender instance.
            player (str): The username of the opponent to challenge.
            battle_format (str): The desired battle format.
        """
        message = f'/challenge {player}, {battle_format}'
        await self.send_message('', message)

    async def accept_challenge(self, player: str):
        """
        Accept a challenge from another user.

        Args:
            self: The Sender instance.
            player (str): The username of the opponent whose challenge to accept.
        """
        message = f'/accept {player}'
        await self.send_message('', message)

    async def send_move(self, battle_tag: str, move: int):
        """
        Send a move command during a battle.

        Args:
            self: The Sender instance.
            battle_tag (str): The tag of the battle where the move is sent.
            move (int): The move to be used.
        """
        message = f'/choose move {move}'
        await self.send_message(battle_tag, message)

    async def send_switch(self, battle_tag: str, pokemon: int):
        """
        Send a switch command during a battle.

        Args:
            self: The Sender instance.
            battle_tag (str): The tag of the battle where the switch is made.
            pokemon (int): The Pokémon to switch to.
        """
        message = f'/choose switch {pokemon}'
        await self.send_message(battle_tag, message)

    async def leave(self, battle_tag: str):
        """
        Leave a battle.

        Args:
            self: The Sender instance.
            battle_tag (str): The tag of the battle to leave.
        """
        await self.send_message('', f'/leave {battle_tag}')

    async def forfeit(self, battle_tag: str):
        """
        Forfeit a battle.

        Args:
            self: The Sender instance.
            battle_tag (str): The tag of the battle to forfeit.
        """
        await self.send_message(battle_tag, '/forfeit')
        await self.leave(battle_tag)

    @classmethod
    def get_instance(cls):
        """
        Get the singleton instance of the Sender class.

        Args:
            cls: The Sender class.

        Returns:
            Sender: The Sender instance.
        """
        return cls.instance

