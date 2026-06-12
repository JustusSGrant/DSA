from priority_queue import PriorityQueue

class GraphSearch:
    def uniform_cost(graph, start, goal):
        # AKA 'cheapest first search'
        # PriorityQueue stores: (cumulative cost, (current_node, path))
        pq = PriorityQueue()
        pq.append((0, (start, [start])))
        visited = set()
        while pq.size() > 0:
            cost, (current_node, path) = pq.pop()
            if current_node in visited:
                continue
            if current_node == goal:
                return cost, path
            visited.add(current_node)
            for neighbor in graph.neighbors(current_node):
                if neighbor not in visited:
                    total_cost = cost + graph.get_edge_weight(current_node, neighbor)
                    pq.append((total_cost, (neighbor, path + [neighbor])))
        return float('inf'), []

    def bidirectional_ucs(graph, start, goal):
        # ExplorableGraph is undirected, so both searches use graph.neighbors()
        if start == goal:
            return 0, [start]

        pq_f = PriorityQueue()
        pq_b = PriorityQueue()
        pq_f.append((0, (start, [start])))
        pq_b.append((0, (goal, [goal])))

        visited_f = {}  # node -> (cost, path)
        visited_b = {}

        best_cost = float('inf')
        best_path = []

        while pq_f.size() > 0 or pq_b.size() > 0:
            # Expand forward frontier
            if pq_f.size() > 0:
                cost_f, (node_f, path_f) = pq_f.pop()
                if node_f not in visited_f:
                    visited_f[node_f] = (cost_f, path_f)
                    if node_f in visited_b:
                        cost_b, path_b = visited_b[node_f]
                        total = cost_f + cost_b
                        if total < best_cost:
                            best_cost = total
                            best_path = path_f + list(reversed(path_b))[1:]
                    for neighbor in graph.neighbors(node_f):
                        if neighbor not in visited_f:
                            edge_cost = graph.get_edge_weight(node_f, neighbor)
                            pq_f.append((cost_f + edge_cost, (neighbor, path_f + [neighbor])))

            # Expand backward frontier
            if pq_b.size() > 0:
                cost_b, (node_b, path_b) = pq_b.pop()
                if node_b not in visited_b:
                    visited_b[node_b] = (cost_b, path_b)
                    if node_b in visited_f:
                        cost_f, path_f = visited_f[node_b]
                        total = cost_f + cost_b
                        if total < best_cost:
                            best_cost = total
                            best_path = path_f + list(reversed(path_b))[1:]
                    for neighbor in graph.neighbors(node_b):
                        if neighbor not in visited_b:
                            edge_cost = graph.get_edge_weight(node_b, neighbor)
                            pq_b.append((cost_b + edge_cost, (neighbor, path_b + [neighbor])))

            # Stop early once the frontiers can't improve the best found path
            min_f = pq_f.top()[0] if pq_f.size() > 0 else float('inf')
            min_b = pq_b.top()[0] if pq_b.size() > 0 else float('inf')
            if min_f + min_b >= best_cost:
                break

        return best_cost, best_path

    def tridirectional_ucs(graph, node_a, node_b, node_c):
        # Single UCS over an augmented state space: (current_node, frozenset of goal nodes visited so far).
        # Starting simultaneously from all three goal nodes ensures the optimal starting point is found.
        goals = frozenset({node_a, node_b, node_c})
        pq = PriorityQueue()
        for start in goals:
            pq.append((0, (start, frozenset({start}), [start])))

        visited = {}  # (node, visited_goals) -> cost

        while pq.size() > 0:
            cost, (node, visited_goals, path) = pq.pop()
            state = (node, visited_goals)
            if state in visited:
                continue
            visited[state] = cost
            if visited_goals == goals:
                return cost, path
            for neighbor in graph.neighbors(node):
                new_visited = visited_goals | (frozenset({neighbor}) & goals)
                if (neighbor, new_visited) not in visited:
                    edge_cost = graph.get_edge_weight(node, neighbor)
                    pq.append((cost + edge_cost, (neighbor, new_visited, path + [neighbor])))

        return float('inf'), []

    def greedy_best_first(graph, start, goal, heuristics):
        # Priority Queue stores (heuristic_val, (current_node, path))
        pq = PriorityQueue()
        pq.append((heuristics[start], (start, [start])))
        visited = set()
        while pq.size() > 0:
            h_val, (current, path) = pq.pop()
            if current == goal:
                return path
            if current not in visited:
                visited.add(current)
                for neighbor in graph.neighbors(current):
                    if neighbor not in visited:
                        pq.append((heuristics[neighbor], (neighbor, path + [neighbor])))
        return None
