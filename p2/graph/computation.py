import networkx as nx

from typing import Tuple


class ExecutionPath(nx.DiGraph):

    @property
    def entry_node(self) -> Tuple[str, dict]:
        for nid, attrs in self.nodes(data=True):
            if "entry" == attrs["kind"]:
                return nid, attrs

    @property
    def exit_node(self) -> Tuple[str, dict]:
        for nid, attrs in self.nodes(data=True):
            if "exit" == attrs["kind"]:
                return nid, attrs

    def validate(self):
        entry_id, _ = self.entry_node
        exit_id, _ = self.exit_node
        if not nx.has_path(self, entry_id, exit_id):
            raise RuntimeError(f"Path between entry ({entry_id}) and "
                               f"exit ({exit_id}) does not exist")

    def yield_topo_order(self) -> Tuple[str, dict]:
        for nid in nx.topological_sort(self):
            yield nid, self.nodes[nid]


class Execution(object):

    def __init__(self, bp_graph: nx.MultiDiGraph):
        self.core_graph = nx.MultiDiGraph(bp_graph, name="CoreGraph")

        self.exec_path = ExecutionPath(name="ExecutionPath")
        self.action_path = nx.DiGraph(name="ActionPath")

    def build_exec_path(self):
        exec_edges = self.filter_edges_by_attr(self.core_graph.edges(data=True),
                                               type="EXECUTION")

        self.exec_path.add_nodes_from(self.core_graph.nodes(data=True))
        self.exec_path.add_edges_from(exec_edges)

    def filter_edges_by_attr(self, edges: list, **kwargs):
        matchin_edges = []

        for e in edges:
            if all([e[2][field] == value for field, value in kwargs.items()]):
                matchin_edges.append(e)
        return matchin_edges

    def build_action_path(self):
        self.action_path.add_node(0)
        section_idx = 0
        current_section = None
        for nid, attrs in self.exec_path.yield_topo_order():
            if attrs["automoton"] != current_section:
                self.action_path.add_node(section_idx+1,
                                          automoton=attrs["automoton"],
                                          nids=[nid])
                self.action_path.add_edge(section_idx, section_idx+1)

                current_section = attrs["automoton"]
                section_idx += 1
            else:
                self.action_path.nodes(data=True)[section_idx]["nids"].append(nid)

    def evaluate_link_value(self, nid, pid):
        for pred_id, edges in self.core_graph.pred[nid].items():
            for eid, e_attrs in edges.items():
                if e_attrs["vport"] == pid:
                    return f"@{pred_id}"
