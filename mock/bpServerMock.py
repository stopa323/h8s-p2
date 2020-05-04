import asyncio

from aio_pika import connect_robust
from aio_pika.patterns import RPC


async def get_blueprint(bp_id):
    print(f"GET {bp_id}")

    bp_mock = {
        "id": bp_id,
        "meta": {},
        "sheet": {
            "nodes": [
                {"id": "node-0",
                 "name": "Blueprint Entry",
                 "automoton": "_core",
                 "kind": "entry",
                 "ingressPorts": [],
                 "egressPorts": [
                     {"id": "port-0",
                      "name": "Entry",
                      "kind": "exec",
                      "dataType": "ExecutionFlow",
                      "mandatory": True}
                 ]},
                {"id": "node-1",
                 "name": "Blueprint Exit",
                 "automoton": "_core",
                 "kind": "exit",
                 "ingressPorts": [
                     {"id": "port-1",
                      "name": "Exit",
                      "kind": "exec",
                      "dataType": "ExecutionFlow",
                      "mandatory": True}
                 ],
                 "egressPorts": []},
                {"id": "node-2",
                 "name": "Create VPC",
                 "automoton": "terraform",
                 "kind": "aws_vpc",
                 "ingressPorts": [
                     {"id": "port-2",
                      "name": "Entry",
                      "kind": "exec",
                      "dataType": "ExecutionFlow",
                      "mandatory": True},
                     {"id": "port-3",
                      "name": "Name",
                      "kind": "string",
                      "dataType": "String",
                      "mandatory": True,
                      "value": "MyFirstVPC"},
                     {"id": "port-4",
                      "name": "CIDR",
                      "kind": "string",
                      "dataType": "Core.IPv4_CIDR",
                      "mandatory": True,
                      "value": "10.10.0.0/16"}
                 ],
                 "egressPorts": [
                     {"id": "port-5",
                      "name": "Exit",
                      "kind": "exec",
                      "dataType": "ExecutionFlow",
                      "mandatory": True},
                     {"id": "port-6",
                      "name": "VPC",
                      "kind": "object",
                      "dataType": "Terraform.AWS_VPC",
                      "mandatory": True}
                 ]},
                {"id": "node-3",
                 "name": "Create Subnet",
                 "automoton": "terraform",
                 "kind": "aws_subnet",
                 "ingressPorts": [
                     {"id": "port-7",
                      "name": "Entry",
                      "kind": "exec",
                      "dataType": "ExecutionFlow",
                      "mandatory": True},
                     {"id": "port-8",
                      "name": "VPC",
                      "kind": "object",
                      "dataType": "Terraform.AWS_VPC",
                      "mandatory": True,
                      "value": None}, # Explicite None -> compute from link
                     {"id": "port-9",
                      "name": "CIDR",
                      "kind": "string",
                      "dataType": "Core.IPv4_CIDR",
                      "mandatory": True,
                      "value": "10.10.10.0/24"}
                 ],
                 "egressPorts": [
                     {"id": "port-10",
                      "name": "Exit",
                      "kind": "exec",
                      "dataType": "ExecutionFlow",
                      "mandatory": True},
                     {"id": "port-11",
                      "name": "Subnet",
                      "kind": "object",
                      "dataType": "Terraform.AWS_Subnet",
                      "mandatory": True}
                 ]}
            ],
            "links": [
                {"id": "link-0",
                 "source": {"nodeId": "node-0", "portId": "port-0"},
                 "sink": {"nodeId": "node-2", "portId": "port-2"}},
                {"id": "link-1",
                 "source": {"nodeId": "node-2", "portId": "port-5"},
                 "sink": {"nodeId": "node-3", "portId": "port-7"}},
                {"id": "link-2",
                 "source": {"nodeId": "node-2", "portId": "port-6"},
                 "sink": {"nodeId": "node-3", "portId": "port-8"}},
                {"id": "link-3",
                 "source": {"nodeId": "node-3", "portId": "port-10"},
                 "sink": {"nodeId": "node-1", "portId": "port-1"}}
            ]
        }
    }

    return bp_mock


async def main():
    connection = await connect_robust("amqp://guest:guest@127.0.0.1:5672//")
    channel = await connection.channel()

    rpc = await RPC.create(channel)
    await rpc.register("get_blueprint", get_blueprint, auto_delete=True)

    return connection


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    connection = loop.run_until_complete(main())

    try:
        print("Up and ready")
        loop.run_forever()
    finally:
        loop.run_until_complete(connection.close())
        loop.shutdown_asyncgens()
