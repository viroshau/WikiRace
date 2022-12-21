import concurrent.futures

def breadth_first_search(graph, start, goal):
    # Queue to store the nodes that need to be explored
    queue = [(start, [start])]

    # Set to store the nodes that have been explored
    visited = set()

    # Function to explore the next node in the queue
    def explore_node(node, path):
        # Mark the node as visited
        visited.add(node)

        # Add the neighbors of the node to the queue
        for neighbor in graph[node]:
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))

    # Create a thread pool with 4 threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        # While there are nodes to explore
        while queue:
            # Get the next node to explore
            node, path = queue.pop(0)

            # If the node is the goal, return the path to it
            if node == goal:
                return path

            # Explore the node in a separate thread
            executor.submit(explore_node, node, path)

    # If the goal was not found, return None
    return None

# Example usage
graph = {
    'A': ['B', 'C', 'D'],
    'B': ['A', 'E', 'F'],
    'C': ['A', 'G'],
    'D': ['A', 'H'],
    'E': ['B'],
    'F': ['B'],
    'G': ['C'],
    'H': ['D']
}

print(breadth_first_search(graph, 'A', 'G'))  # ['A', 'C', 'G']
print(breadth_first_search(graph, 'A', 'H'))  # ['A', 'D', 'H']
print(breadth_first_search(graph, 'A', 'F'))  # ['A', 'B', 'F']