import heapq
class GraphSearch:
    def uniform_cost(graph, start, target):
        # AKA 'cheapest first search'
        # Priority Queue stores: (cummulative cost, current_node, path)
        priority_queue = [(0, start, [start])]
        # set to keep track of visited nodes & avoid cycles
        visited = set()
        while priority_queue:
            # Pop the node with the lowest cummulative cost
            cost, current_node, path = heapq.heappop(priority_queue)
            if current_node in visited:
                continue
            if current_node == target:
                return cost, path
            visited.add(current_node)
            # Explore neighbors
            for neighbor, edge_cost in graph.get(current_node, {}).items():
                if neighbor not in visited:
                    total_cost = cost + edge_cost
                    # Add new path to priority queue
                    heapq.heappush(priority_queue, (total_cost, neighbor, path + [neighbor]))
        return float('inf'), []
    
    def greedy_best_first(graph, start, goal, heuristics):
        # This algorithm searches for the goal by continuously trying to get closer to it.
        # If the most optimal path requires this search to take a step that is further from
        # the goal than its current position that path will not be considered.
        
        # Priority QUeue stores (heuristic_val, current_node, path)
        priority_queue = [(heuristics[start], start, [start])]
        visited = set()
        while priority_queue:
            # pop the node with the lowest heuristic value
            h_val, current, path = heapq.heappop(priority_queue)
            if current == goal:
                return path
            if current not in visited:
                visited.add(current)
                # add all neighbors. THis algorithm ignores weight
                for neighbor in graph[current]:
                    if neighbor not in visited:
                        new_path = path + [neighbor]
                        heapq.heappush(priority_queue, (heuristics[neighbor], neighbor, new_path))
        return None
                        
                    
    
    
# Example Graph: Adjacency list with weights
graph = {
    'S': {'A': 2, 'B': 5},
    'A': {'C': 2, 'D': 4},
    'B': {'D': 1, 'G': 10},
    'C': {'G': 4},
    'D': {'G': 3},
    'G': {}
}