import heapq

def best_first_search(graph, heuristics, start, goal):
    visited = set()
    heap = [(heuristics[start], start)]

    while heap:
        cost, node = heapq.heappop(heap)
        if node in visited:
            continue
        print(node, end=" ")
        visited.add(node)

        if node == goal:
            print("\nGoal found!")
            return

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                heapq.heappush(heap, (heuristics[neighbor], neighbor))
    print("\nGoal not found.")

def create_graph_and_heuristics():
    graph = {}
    heuristics = {}
    n = int(input("Enter number of edges: "))
    for _ in range(n):
        u, v = input("Enter edge (u v): ").split()
        graph.setdefault(u, []).append(v)
        graph.setdefault(v, []).append(u)
    m = int(input("Enter number of nodes for heuristics: "))
    for _ in range(m):
        node, h = input("Enter node and heuristic (node h): ").split()
        heuristics[node] = int(h)
    return graph, heuristics

def main():
    graph, heuristics = create_graph_and_heuristics()
    start = input("Enter start node: ")
    goal = input("Enter goal node: ")
    best_first_search(graph, heuristics, start, goal)

if __name__ == "__main__":
    main()
