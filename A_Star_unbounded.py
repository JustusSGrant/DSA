from priority_queue import PriorityQueue


def a_star_graph_search(graph, src, dest):
    try:
        graph.pos(src)
        graph.pos(dest)
    except KeyError as e:
        print(f"Source or destination not found in graph: {e}")
        return []

    if is_destination(src, dest):
        print("We have already reached the destination")
        return []

    g_costs = {src: 0.0}
    paths = {src: [src]}
    visited = set()

    pq = PriorityQueue()
    pq.append((0.0, src))

    while pq.size() > 0:
        f_cost, current_node = pq.pop()

        if current_node in visited:
            continue

        if is_destination(current_node, dest):
            print("Found the destination.")
            return paths[current_node]

        visited.add(current_node)

        for neighbor in graph.neighbors(current_node):
            if neighbor in visited:
                continue

            new_g = g_costs[current_node] + graph.get_edge_weight(current_node, neighbor)

            if neighbor not in g_costs or new_g < g_costs[neighbor]:
                g_costs[neighbor] = new_g
                paths[neighbor] = paths[current_node] + [neighbor]
                new_f = new_g + calc_heuristic_val(graph, neighbor, dest)
                pq.append((new_f, neighbor))

    print("Failed to find the destination node.")
    return []


# Calculate the heuristic value using Euclidean distance via graph.pos()
def calc_heuristic_val(graph, node, dest):
    try:
        x1, y1 = graph.pos(node)
        x2, y2 = graph.pos(dest)
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    except (KeyError, TypeError):
        return 0

def is_destination(node, dest):
    return node == dest


def bidirectional_a_star(graph, src, dest):
    if src == dest:
        return [src]

    try:
        graph.pos(src)
        graph.pos(dest)
    except KeyError as e:
        print(f"Source or destination not found in graph: {e}")
        return []

    # g-costs from each origin; path dicts store full routes for reconstruction
    g_f = {src: 0.0}
    g_b = {dest: 0.0}
    path_f = {src: [src]}
    path_b = {dest: [dest]}
    closed_f = set()
    closed_b = set()

    pq_f = PriorityQueue()
    pq_b = PriorityQueue()
    pq_f.append((calc_heuristic_val(graph, src, dest), src))
    pq_b.append((calc_heuristic_val(graph, dest, src), dest))

    best_cost = float('inf')
    best_path = []

    while pq_f.size() > 0 and pq_b.size() > 0:
        f_top_f = pq_f.top()[0]
        f_top_b = pq_b.top()[0]

        # Euclidean heuristic is consistent: once either frontier's minimum
        # f-value >= best_cost, every remaining path through it costs at least
        # best_cost and cannot improve the solution.
        if min(f_top_f, f_top_b) >= best_cost:
            break

        if f_top_f <= f_top_b:
            _, current = pq_f.pop()
            if current in closed_f:
                continue
            closed_f.add(current)

            for neighbor in graph.neighbors(current):
                if neighbor in closed_f:
                    continue
                new_g = g_f[current] + graph.get_edge_weight(current, neighbor)
                if neighbor not in g_f or new_g < g_f[neighbor]:
                    g_f[neighbor] = new_g
                    path_f[neighbor] = path_f[current] + [neighbor]
                    pq_f.append((new_g + calc_heuristic_val(graph, neighbor, dest), neighbor))
                    if neighbor in g_b:
                        total = new_g + g_b[neighbor]
                        if total < best_cost:
                            best_cost = total
                            # path_b[neighbor] = [dest, ..., neighbor];
                            # [-2::-1] reverses it starting from the predecessor,
                            # giving [pred, ..., dest] with no duplicate meeting node.
                            best_path = path_f[neighbor] + path_b[neighbor][-2::-1]
        else:
            _, current = pq_b.pop()
            if current in closed_b:
                continue
            closed_b.add(current)

            for neighbor in graph.neighbors(current):
                if neighbor in closed_b:
                    continue
                new_g = g_b[current] + graph.get_edge_weight(current, neighbor)
                if neighbor not in g_b or new_g < g_b[neighbor]:
                    g_b[neighbor] = new_g
                    path_b[neighbor] = path_b[current] + [neighbor]
                    pq_b.append((new_g + calc_heuristic_val(graph, neighbor, src), neighbor))
                    if neighbor in g_f:
                        total = g_f[neighbor] + new_g
                        if total < best_cost:
                            best_cost = total
                            best_path = path_f[neighbor] + path_b[neighbor][-2::-1]

    if not best_path:
        print("Failed to find the destination node.")
        return []

    print("Found the destination.")
    return best_path


def tridirectional_a_star(graph, node_a, node_b, node_c):
    try:
        graph.pos(node_a)
        graph.pos(node_b)
        graph.pos(node_c)
    except KeyError as e:
        print(f"Node not found in graph: {e}")
        return float('inf'), []

    g_costs_a = {node_a: 0.0}
    g_costs_b = {node_b: 0.0}
    g_costs_c = {node_c: 0.0}

    paths_a = {node_a: [node_a]}
    paths_b = {node_b: [node_b]}
    paths_c = {node_c: [node_c]}

    visited_a = set()
    visited_b = set()
    visited_c = set()

    pq_a = PriorityQueue()
    pq_b = PriorityQueue()
    pq_c = PriorityQueue()

    # h_x(n) = min(h(n,Y), h(n,Z)): admissible lower bound on the first
    # segment of the cheapest ordering from X, since any path from n must
    # reach at least one other terminal and costs >= the shorter Euclidean leg.
    pq_a.append((min(calc_heuristic_val(graph, node_a, node_b),
                     calc_heuristic_val(graph, node_a, node_c)), node_a))
    pq_b.append((min(calc_heuristic_val(graph, node_b, node_a),
                     calc_heuristic_val(graph, node_b, node_c)), node_b))
    pq_c.append((min(calc_heuristic_val(graph, node_c, node_a),
                     calc_heuristic_val(graph, node_c, node_b)), node_c))

    # Track best cost and path for each pair of frontiers meeting at any node M.
    # paths_x[M] = [node_x, ..., M], so paths_x[M] + paths_y[M][-2::-1]
    # gives the full path from node_x to node_y through M.
    best_ab = float('inf')
    best_bc = float('inf')
    best_ac = float('inf')
    path_ab = []
    path_bc = []
    path_ac = []

    best_cost = float('inf')
    best_path = []

    def _update_orderings():
        nonlocal best_cost, best_path
        # A → B → C
        if best_ab + best_bc < best_cost:
            best_cost = best_ab + best_bc
            best_path = path_ab + path_bc[1:]
        # A → C → B
        if best_ac + best_bc < best_cost:
            best_cost = best_ac + best_bc
            best_path = path_ac + path_bc[::-1][1:]
        # B → A → C
        if best_ab + best_ac < best_cost:
            best_cost = best_ab + best_ac
            best_path = path_ab[::-1] + path_ac[1:]

    def _check_pairwise(node):
        nonlocal best_ab, best_bc, best_ac, path_ab, path_bc, path_ac
        if node in g_costs_a and node in g_costs_b:
            cost = g_costs_a[node] + g_costs_b[node]
            if cost < best_ab:
                best_ab = cost
                path_ab = paths_a[node] + paths_b[node][-2::-1]
                _update_orderings()
        if node in g_costs_b and node in g_costs_c:
            cost = g_costs_b[node] + g_costs_c[node]
            if cost < best_bc:
                best_bc = cost
                path_bc = paths_b[node] + paths_c[node][-2::-1]
                _update_orderings()
        if node in g_costs_a and node in g_costs_c:
            cost = g_costs_a[node] + g_costs_c[node]
            if cost < best_ac:
                best_ac = cost
                path_ac = paths_a[node] + paths_c[node][-2::-1]
                _update_orderings()

    _check_pairwise(node_a)
    _check_pairwise(node_b)
    _check_pairwise(node_c)

    while pq_a.size() > 0 or pq_b.size() > 0 or pq_c.size() > 0:
        f_top_a = pq_a.top()[0] if pq_a.size() > 0 else float('inf')
        f_top_b = pq_b.top()[0] if pq_b.size() > 0 else float('inf')
        f_top_c = pq_c.top()[0] if pq_c.size() > 0 else float('inf')

        if min(f_top_a, f_top_b, f_top_c) >= best_cost:
            break

        if f_top_a <= f_top_b and f_top_a <= f_top_c:
            f_cost, current_node = pq_a.pop()
            if current_node in visited_a:
                continue
            visited_a.add(current_node)
            _check_pairwise(current_node)

            for neighbor in graph.neighbors(current_node):
                if neighbor in visited_a:
                    continue
                new_g = g_costs_a[current_node] + graph.get_edge_weight(current_node, neighbor)
                if neighbor not in g_costs_a or new_g < g_costs_a[neighbor]:
                    g_costs_a[neighbor] = new_g
                    paths_a[neighbor] = paths_a[current_node] + [neighbor]
                    new_f = new_g + min(calc_heuristic_val(graph, neighbor, node_b),
                                       calc_heuristic_val(graph, neighbor, node_c))
                    pq_a.append((new_f, neighbor))
                    _check_pairwise(neighbor)

        elif f_top_b <= f_top_c:
            f_cost, current_node = pq_b.pop()
            if current_node in visited_b:
                continue
            visited_b.add(current_node)
            _check_pairwise(current_node)

            for neighbor in graph.neighbors(current_node):
                if neighbor in visited_b:
                    continue
                new_g = g_costs_b[current_node] + graph.get_edge_weight(current_node, neighbor)
                if neighbor not in g_costs_b or new_g < g_costs_b[neighbor]:
                    g_costs_b[neighbor] = new_g
                    paths_b[neighbor] = paths_b[current_node] + [neighbor]
                    new_f = new_g + min(calc_heuristic_val(graph, neighbor, node_a),
                                       calc_heuristic_val(graph, neighbor, node_c))
                    pq_b.append((new_f, neighbor))
                    _check_pairwise(neighbor)

        else:
            f_cost, current_node = pq_c.pop()
            if current_node in visited_c:
                continue
            visited_c.add(current_node)
            _check_pairwise(current_node)

            for neighbor in graph.neighbors(current_node):
                if neighbor in visited_c:
                    continue
                new_g = g_costs_c[current_node] + graph.get_edge_weight(current_node, neighbor)
                if neighbor not in g_costs_c or new_g < g_costs_c[neighbor]:
                    g_costs_c[neighbor] = new_g
                    paths_c[neighbor] = paths_c[current_node] + [neighbor]
                    new_f = new_g + min(calc_heuristic_val(graph, neighbor, node_a),
                                       calc_heuristic_val(graph, neighbor, node_b))
                    pq_c.append((new_f, neighbor))
                    _check_pairwise(neighbor)

    if not best_path:
        print("Failed to find the destination node.")
        return float('inf'), []

    print("Found the destination.")
    return best_cost, best_path
