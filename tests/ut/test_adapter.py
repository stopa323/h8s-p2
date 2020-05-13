import unittest

from p2.graph import adapters, computation, drawing


class ParsingTestCase(unittest.TestCase):

    def setUp(self):
        super(ParsingTestCase, self).setUp()

        self.blueprint = {
            "id": "00000000-0000-0000-0000-000000000001",
            "meta": {},
            "sheet": {
                "nodes": [
                    {"id": "node-0",
                     "name": "Blueprint Entry",
                     "automoton": "_CORE",
                     "kind": "entry",
                     "ingressPorts": [],
                     "egressPorts": [
                         {"id": "port-0",
                          "name": "Entry",
                          "kind": "exec",
                          "mandatory": True}
                     ]},
                    {"id": "node-1",
                     "name": "Blueprint Exit",
                     "automoton": "_CORE",
                     "kind": "exit",
                     "ingressPorts": [
                         {"id": "port-1",
                          "name": "Exit",
                          "kind": "exec",
                          "mandatory": True}
                     ],
                     "egressPorts": []},
                    {"id": "node-2",
                     "name": "Create VPC",
                     "automoton": "TERRAFORM",
                     "kind": "aws_vpc",
                     "ingressPorts": [
                         {"id": "port-2",
                          "name": "Entry",
                          "kind": "exec",
                          "mandatory": True},
                         {"id": "port-3",
                          "name": "Name",
                          "kind": "string",
                          "mandatory": True,
                          "value": "MyFirstVPC"},
                         {"id": "port-4",
                          "name": "CIDR",
                          "kind": "string",
                          "mandatory": True,
                          "value": "10.10.0.0/16"}
                     ],
                     "egressPorts": [
                         {"id": "port-5",
                          "name": "Exit",
                          "kind": "exec",
                          "mandatory": True},
                         {"id": "port-6",
                          "name": "VPC",
                          "kind": "object",
                          "mandatory": True}
                     ]},
                    {"id": "node-3",
                     "name": "Create Subnet",
                     "automoton": "TERRAFORM",
                     "kind": "aws_subnet",
                     "ingressPorts": [
                         {"id": "port-7",
                          "name": "Entry",
                          "kind": "exec",
                          "mandatory": True},
                         {"id": "port-8",
                          "name": "VPC",
                          "kind": "object",
                          "mandatory": True},
                         {"id": "port-9",
                          "name": "CIDR",
                          "kind": "string",
                          "mandatory": True,
                          "value": "10.10.10.0/24"}
                     ],
                     "egressPorts": [
                         {"id": "port-10",
                          "name": "Exit",
                          "kind": "exec",
                          "mandatory": True},
                         {"id": "port-11",
                          "name": "Subnet",
                          "kind": "object",
                          "mandatory": True}
                     ]}
                ],
                "links": [
                    {"id": "link-0",
                     "type": "EXECUTION",
                     "source": {"nodeId": "node-0", "portId": "port-0"},
                     "sink": {"nodeId": "node-2", "portId": "port-2"}},
                    {"id": "link-1",
                     "type": "EXECUTION",
                     "source": {"nodeId": "node-2", "portId": "port-5"},
                     "sink": {"nodeId": "node-3", "portId": "port-7"}},
                    {"id": "link-2",
                     "type": "DATA",
                     "source": {"nodeId": "node-2", "portId": "port-6"},
                     "sink": {"nodeId": "node-3", "portId": "port-8"}},
                    {"id": "link-3",
                     "type": "EXECUTION",
                     "source": {"nodeId": "node-3", "portId": "port-10"},
                     "sink": {"nodeId": "node-1", "portId": "port-1"}}
                ]
            }
        }

    def test_(self):
        adapter = adapters.BlueprintAdapter(self.blueprint)

        execution = computation.Execution(adapter.graph)

        execution.build_exec_path()
        execution.exec_path.validate()

        execution.build_action_path()

        print(execution.evaluate_link_value("node-3", "port-8"))
        # execution.build_action_graph()
        # painter = drawing.GraphPainter(adapter.graph)
        # painter.draw()
