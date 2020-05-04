from aio_pika.patterns import RPC

from p2.rpc import get_connection
from p2.schema import execution


async def create_execution(exec: execution.CreateBlueprintExecution):
    connection = await get_connection()
    channel = await connection.channel()

    rpc = await RPC.create(channel)

    bp = await rpc.proxy.get_blueprint(bp_id=exec.blueprint_id)

    print(bp)
