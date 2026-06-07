from collections import deque

class TreeSearch:
    def dfs(node, target):
        if node.value == target:
            return node
        for child in node.children:
            result = search_dfs(child, target)
            if result:
                return result
        return None
    
    def bfs_shortest_path(graph, root_node, target):
        if (root_node.value == target):
            return [root_node.value]
        # Track visited nodes to avoid infinite loops in cyclic graphs
        visited = set(root_node)
        #initialize the queue with the root node and the path taken to reach it.
        queue = deque([(root_node, [root_node.value])])
        while queue:
            current, path = queue.popleft()
            for neighbor in graph[current]:
                if neighbor == target:
                    return path + [neighbor.value]
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor.value]))
        return None
    
    
    def bfs_shortest_path_two(graph, root_node, target):
        if root_node == target:
            return [root_node]
        visited = {root_node}
        queue = deque([(root_node, [root_node])])
        while queue:
            current, path = queue.popleft()
            for neighbor in graph.neighbors(current):
                if neighbor == target:
                    return path + [neighbor]
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return None
        
        