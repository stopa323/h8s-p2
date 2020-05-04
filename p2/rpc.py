from aio_pika import connect_robust
from aio_pika.connection import ConnectionType


CONNECTION = None


async def get_connection() -> ConnectionType:
    global CONNECTION
    if not CONNECTION:
        CONNECTION = await connect_robust(
            url="amqp://guest:guest@127.0.0.1:5672//")
    return CONNECTION
