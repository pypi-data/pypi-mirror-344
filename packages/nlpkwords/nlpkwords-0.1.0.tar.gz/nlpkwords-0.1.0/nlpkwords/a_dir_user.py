import heapq

def a_star(graph, heuristics, start, goal):
    open_set = [(heuristics[start], 0, start)]
    visited = set()

    while open_set:
        est_total, cost_so_far, node = heapq.heappop(open_set)
        if node == goal:
            print(f"Reached {goal} with total cost {cost_so_far}")
            return

        visited.add(node)
        print(node, end=" ")

        for neighbor, weight in graph.get(node, []):
            if neighbor not in visited:
                g = cost_so_far + weight
                f = g + heuristics.get(neighbor, float('inf'))
                heapq.heappush(open_set, (f, g, neighbor))
    print("\nGoal not reachable.")

def create_graph_and_heuristics():
    graph = {}
    heuristics = {}
    n = int(input("Enter number of edges: "))
    for _ in range(n):
        u, v, w = input("Enter edge (u v weight): ").split()
        w = int(w)
        graph.setdefault(u, []).append((v, w))
    m = int(input("Enter number of nodes for heuristics: "))
    for _ in range(m):
        node, h = input("Enter node and heuristic (node h): ").split()
        heuristics[node] = int(h)
    return graph, heuristics

def main():
    graph, heuristics = create_graph_and_heuristics()
    start = input("Enter start node: ")
    goal = input("Enter goal node: ")
    a_star(graph, heuristics, start, goal)

if __name__ == "__main__":
    main()
