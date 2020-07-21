import asyncio
from nats.aio.client import Client as NATS
from aioconsole import ainput
# https://github.com/nats-io/nats.py updated example

MY_NAME = "he"
PARTHNER_NAME = "me"


async def run(loop):
    nc = NATS()

    await nc.connect("127.0.0.1:4222", loop=loop)

    async def message_handler(msg):
        data = msg.data.decode()
        print("Received a message: " + data)

    # Simple publisher and async subscriber via coroutine.
    sid = await nc.subscribe(MY_NAME, cb=message_handler)
    while True:
        # https://stackoverflow.com/questions/39901813/asyncio-server-and-client-to-handle-input-from-console
        line = await ainput(">>> ")
        if line == "/exit-me":
            break
        if len(line) > 0:
            await nc.publish(PARTHNER_NAME, line.encode())

    await nc.unsubscribe(sid)

    # Terminate connection to NATS.
    await nc.close()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    loop.close()
