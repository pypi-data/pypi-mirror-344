from collections import deque

def bfs(graph, start):
    visited = set()
    queue = deque([start])

    while queue:
        node = queue.popleft()
        if node not in visited:
            print(node, end=" ")
            visited.add(node)
            queue.extend(graph[node])

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
    print("BFS Traversal:")
    bfs(graph, start_node)

if __name__ == "__main__":
    main()
