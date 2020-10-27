import asyncio
import json
import logging
import websockets
import redis 

logging.basicConfig()

STATE = {"value": 0}

USERS = set()

SUBS = set()

def state_event():
    return json.dumps({"type": "state", **STATE})

def users_event():
    return json.dumps({"type": "users", "count": len(USERS)})

def new_user(name):
    return json.dumps({"type": "new", "message": name})

async def welcome_user(name: str):
    #if USERS:
    if SUBS:
        message = new_user(name)
        await asyncio.wait([sub[0].send(message) for sub in SUBS])
        #await asyncio.wait([user.send(message) for user in USERS])

async def notify_state():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = state_event()
        await asyncio.wait([user.send(message) for user in USERS])

async def notify_users():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = users_event()
        await asyncio.wait([user.send(message) for user in USERS])

async def register(websocket):
    USERS.add(websocket)
    await notify_users()

async def unregister(websocket):
    USERS.remove(websocket)
    await notify_users()

async def subscribe(websocket, name):
    SUBS.add((websocket, name))
    await welcome_user(name)

async def counter(websocket, path):
    await register(websocket)
    try:
        await websocket.send(state_event())
        async for message in websocket:
            data = json.loads(message)
            print(data)
            if data["action"] == "minus":
                STATE["value"] -= 1
                await notify_state()
            elif data["action"] == "plus":
                STATE["value"] += 1
                await notify_state()
            elif data["action"] == "subscribe":
                await subscribe(websocket, data["name"])
            else:
                logging.error("unsupported event: {}", data)
    finally:
        await unregister(websocket)

start_server = websockets.serve(counter, "localhost", 6789)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
