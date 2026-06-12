import json


class ExplorableGraph(object):
    """Graph"""

    def __init__(self, data: dict | None = None, name: str = ""):
        self.name = name
        self._nodes = dict()
        self._edges = dict()
        self._explored_nodes = dict()
        self._adjacency = dict()
        if data:
            self.build_graph(data)

    def explored_nodes(self) -> dict:
        return self._explored_nodes

    def reset_search(self):
        self._explored_nodes = dict([(node, 0) for node in self._nodes])

    def build_graph(self, data: dict):
        self._nodes = data["nodes"]
        self._edges = data["edges"]
        self._explored_nodes = dict([(node, 0) for node in self._nodes])
        self.make_adjacency()

    def build_from_json(self, json_file: str):
        data = {}
        with open(json_file, "r") as file:
            imported = json.load(file)
        data["nodes"] = imported["nodes"]
        data["edges"] = dict()
        for edge in imported["edges"]:
            source = edge["source"]
            target = edge["target"]
            weight = edge["weight"]
            data["edges"][(source, target)] = {"weight": weight}
        self.build_graph(data)

    def save_to_json(self, json_file: str):
        data = {}
        data["nodes"] = self._nodes
        data["edges"] = []
        for edge_key in self._edges:
            data["edges"].append(
                {
                    "source": edge_key[0],
                    "target": edge_key[1],
                    "weight": self._edges[edge_key]["weight"],
                }
            )
        with open(json_file, "w") as file:
            json.dump(data, file)

    def make_adjacency(self):
        for edge_key in self._edges:
            node_u, node_v = edge_key
            if node_u not in self._adjacency:
                self._adjacency[node_u] = set()
            if node_v not in self._adjacency:
                self._adjacency[node_v] = set()
            self._adjacency[node_u].add(node_v)
            self._adjacency[node_v].add(node_u)

    ## Student callable methods below ##

    def pos(self, n) -> tuple:
        """
        Student callable
        """
        if n not in self._nodes:
            raise KeyError(f"Node {n} not found in graph.")
        return self._nodes[n]["pos"]

    def neighbors(self, n) -> list:
        """
        Student callable
        """
        if n in self._nodes:
            self._explored_nodes[n] += 1
        else:
            raise KeyError(f"Node {n} not found in graph.")
        return sorted(list(self._adjacency[n]))

    def get_edge_weight(self, u, v) -> float:
        """
        Student callable
        """
        if (u, v) in self._edges:
            return self._edges[(u, v)]["weight"]
        elif (v, u) in self._edges:
            return self._edges[(v, u)]["weight"]
        else:
            raise KeyError(f"Edge ({u}, {v}) not found in graph.")
