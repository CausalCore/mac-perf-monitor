class Node:
    def __init__(self, node_id, node_type, value):
        self.id = node_id
        self.type = node_type  # SYMPTOM, METRIC, PROCESS, ROOT
        self.value = value
        self.influence_score = 0.0


class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = []

    def add_node(self, node_id, node_type, value=0):
        if node_id not in self.nodes:
            self.nodes[node_id] = Node(node_id, node_type, value)

    def add_edge(self, source, target, weight):
        self.edges.append({"source": source, "target": target, "weight": weight})
        if source in self.nodes:
            self.nodes[source].influence_score += weight


def build_graph(timeline_data, processes, current_lag_event=True):
    """
    Builds the initial DAG structure from telemetry data.
    """
    g = Graph()

    # Add Symptom
    if current_lag_event:
        g.add_node("UI_LAG", "SYMPTOM", 1)

    # Add System Metrics
    g.add_node("IO_SPIKE", "METRIC")
    g.add_node("SWAP_THRASH", "METRIC")
    g.add_node("MEM_LEAK", "METRIC")
    g.add_node("CPU_HOG", "METRIC")
    g.add_node("GPU_LOAD", "METRIC")
    g.add_node("WAKEUP_STORM", "METRIC")

    # Add Processes
    for p in processes:
        g.add_node(f"PROC_{p['name']}", "PROCESS", p["cpu_percent"])

    return g
