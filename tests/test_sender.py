import unittest
from unittest.mock import patch, call
import websockets
from web_socket.sender import Sender


async def create_sender_instance():
    async with websockets.connect('ws://sim.smogon.com:8000/showdown/websocket') as web_socket:
        sender = Sender(web_socket)
        return sender


class TestSender(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.sender = await create_sender_instance()

    @patch.object(Sender, 'send_message')  # Patch the send_message method
    async def test_search_game_in_format(self, mock_send_message):
        # Define the argument for send_move
        battle_format = 'gen9randombattle'

        # Call the send_move method
        await self.sender.search_game_in_format(battle_format)

        # Assert that send_message was called with the expected argument
        mock_send_message.assert_called_once_with('', '/search gen9randombattle')

    @patch.object(Sender, 'send_message')  # Patch the send_message method
    async def test_challenge_user(self, mock_send_message):
        # Define the arguments for send_move
        player_to_challenge = 'someplayer'
        battle_format = 'gen9randombattle'

        # Call the send_move method
        await self.sender.challenge_user(player_to_challenge, battle_format)

        # Assert that send_message was called with the expected argument
        mock_send_message.assert_called_once_with('', '/challenge someplayer, gen9randombattle')

    @patch.object(Sender, 'send_message')  # Patch the send_message method
    async def test_accept_challenge(self, mock_send_message):
        # Define the argument for send_move
        player_to_accept = 'someplayer'

        # Call the send_move method
        await self.sender.accept_challenge(player_to_accept)

        # Assert that send_message was called with the expected argument
        mock_send_message.assert_called_once_with('', '/accept someplayer')

    @patch.object(Sender, 'send_message')  # Patch the send_message method
    async def test_send_move(self, mock_send_message):
        # Define the arguments for send_move
        battle_tag = 'battle123'
        move = 3

        # Call the send_move method
        await self.sender.send_move(battle_tag, move)

        # Assert that send_message was called with the expected arguments
        mock_send_message.assert_called_once_with(battle_tag, '/choose move 3')

    @patch.object(Sender, 'send_message')  # Patch the send_message method
    async def test_send_switch(self, mock_send_message):
        # Define the arguments for send_move
        battle_tag = 'battle123'
        switch = 5

        # Call the send_move method
        await self.sender.send_switch(battle_tag, switch)

        # Assert that send_message was called with the expected arguments
        mock_send_message.assert_called_once_with(battle_tag, '/choose switch 5')

    @patch.object(Sender, 'send_message')  # Patch the send_message method
    async def test_leave(self, mock_send_message):
        # Define the argument for send_move
        battle_tag = 'battle123'

        # Call the send_move method
        await self.sender.leave(battle_tag)

        # Assert that send_message was called with the expected arguments
        mock_send_message.assert_called_once_with('', '/leave battle123')

    @patch.object(Sender, 'send_message')  # Patch the send_message method
    async def test_forfeit_send(self, mock_send_message):
        # Define the argument for send_move
        battle_tag = 'battle123'

        # Call the send_move method
        await self.sender.forfeit(battle_tag)

        # Assert that send_message was called twice (leave & forfeit) with the expected arguments
        mock_send_message.assert_has_calls([call('battle123', '/forfeit'), call('', '/leave battle123')])


if __name__ == '__main__':
    unittest.main()
