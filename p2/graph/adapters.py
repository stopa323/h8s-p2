import networkx as nx


class AdapterError(Exception):
    pass


class BlueprintAdapter(object):

    def __init__(self, blueprint: dict):
        self._bp = blueprint
        self.graph = nx.MultiDiGraph(name="ActionGraph")

        self.build_graph()

    def parse_nodes(self):
        for node in self._bp["sheet"]["nodes"]:
            ports = self.parse_node_ports(node["ingressPorts"])
            self.graph.add_node(node["id"], name=node["name"], kind=node["kind"],
                                automoton=node["automoton"], ports=ports)

    def parse_node_ports(self, node_ports):
        ports = dict()
        for p in node_ports:
            if p["kind"] == "exec":
                continue
            ports[p["id"]] = {"name": p["name"], "value": p.get("value", "@link")}
        return ports

    def parse_links(self):
        for link in self._bp["sheet"]["links"]:
            u_node_id = link["source"]["nodeId"]
            v_node_id = link["sink"]["nodeId"]
            self.graph.add_edge(u_node_id, v_node_id, type=link["type"],
                                uport=link["source"]["portId"],
                                vport=link["sink"]["portId"])

    def build_graph(self):
        try:
            self.parse_nodes()
            self.parse_links()
        except KeyError as err:
            raise AdapterError(
                "Incorrect Blueprint format. Missing %s section" % err)
