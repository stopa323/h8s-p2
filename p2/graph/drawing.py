import matplotlib.pyplot as plt
import networkx as nx


class GraphPainter(object):

    ENTRY_NODE_COLOR = "red"
    EXIT_NODE_COLOR = "green"
    ACTION_NODE_COLOR = "grey"

    EXECUTION_EDGE_COLOR = "grey"
    DATA_EDGE_COLOR = "blue"

    def __init__(self, graph: nx.MultiDiGraph):
        self.graph = graph

    @property
    def entry_nodes(self):
        return self._nodes_by_attr(kind="entry")

    @property
    def exit_nodes(self):
        return self._nodes_by_attr(kind="exit")

    @property
    def action_nodes(self):
        nodes = []
        for nid, attrs in self.graph.nodes(data=True):
            if attrs["kind"] not in ("entry", "exit"):
                nodes.append(nid)
        return nodes

    @property
    def labels(self):
        labels = {nid: attrs["name"] for nid, attrs in self.graph.nodes(data=True)}
        return labels

    def _nodes_by_attr(self, **kwargs):
        nodes = list()
        for nid, attrs in self.graph.nodes(data=True):
            if all([attrs[attribute]==value
                    for attribute, value in kwargs.items()]):
                nodes.append(nid)
        return nodes

    def _draw_edges(self, ax, edges, color, pos, offset):
        for e in edges:
            ax.annotate("",
                        xy=pos[e[0]], xycoords='data',
                        xytext=pos[e[1]], textcoords='data',
                        arrowprops=dict(arrowstyle="<-", color=color,
                                        shrinkA=15, shrinkB=15,
                                        patchA=None, patchB=None,
                                        connectionstyle="arc3,rad=%s"
                                                        % str(0.15 * offset)))

    def draw_execution_edges(self, ax, pos):
        edges = filter(lambda e: e[2]["type"] == "EXECUTION", self.graph.edges(data=True))
        self._draw_edges(ax, edges, self.EXECUTION_EDGE_COLOR, pos, -1)

    def draw_data_edges(self, ax, pos):
        edges = filter(lambda e: e[2]["type"] == "DATA", self.graph.edges(data=True))
        self._draw_edges(ax, edges, self.DATA_EDGE_COLOR, pos, 1)

    def draw(self):
        pos = nx.planar_layout(self.graph)

        nx.draw_networkx_nodes(self.graph, pos, nodelist=self.entry_nodes,
                               node_color=self.ENTRY_NODE_COLOR, node_size=1000,
                               alpha=0.2)
        nx.draw_networkx_nodes(self.graph, pos, nodelist=self.exit_nodes,
                               node_color=self.EXIT_NODE_COLOR, node_size=700,
                               alpha=0.2)
        nx.draw_networkx_nodes(self.graph, pos, nodelist=self.action_nodes,
                               node_color=self.ACTION_NODE_COLOR, node_size=600,
                               alpha=0.2)

        ax = plt.gca()
        self.draw_execution_edges(ax, pos)
        self.draw_data_edges(ax, pos)

        nx.draw_networkx_labels(self.graph, pos, self.labels, font_size=7)

        plt.axis('off')
        plt.show()
