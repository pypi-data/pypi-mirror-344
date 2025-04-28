def dfs_non_recursive(graph, start):
    visited = set()
    stack = [start]
    
    while stack:
        node = stack.pop()
        if node not in visited:
            print(node, end=" ")
            visited.add(node)
            stack.extend(reversed(graph[node]))  # reverse for correct order

def create_graph():
    graph = {}
    n = int(input("Enter number of edges: "))
    for _ in range(n):
        u, v = input("Enter edge (u v): ").split()
        graph.setdefault(u, []).append(v)
        graph.setdefault(v, []).append(u)
    return graph

def main():
    graph = create_graph()
    start_node = input("Enter the starting node: ")
    print("DFS Traversal:")
    dfs_non_recursive(graph, start_node)

if __name__ == "__main__":
    main()
