import asyncio
from datetime import datetime
from web_socket.sender import Sender
import websockets
from web_socket.communication_manager import handle_showdown_messages
from web_socket.constant_variable import BOT_MODE


async def main():
    """
    Loading function. Connect websocket then launch bot.
    """
    print("get here")
    async with websockets.connect('ws://sim.smogon.com:8000/showdown/websocket') as web_socket:
        Sender(web_socket)
        while True:
            message = await web_socket.recv()
            print(f'[{datetime.now().replace(microsecond=0).isoformat()}] << {message}')
            await handle_showdown_messages(message, bot_mode=BOT_MODE.ACCEPT_CHALLENGE)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
        asyncio.set_event_loop(None)
