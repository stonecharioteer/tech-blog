import asyncio
import websockets


async def chat():
    uri = "ws://127.0.0.1:8003/ws"
    async with websockets.connect(uri) as ws:
        await ws.send("Hello Server!")
        response = await ws.recv()
        print(response)


asyncio.run(chat())
