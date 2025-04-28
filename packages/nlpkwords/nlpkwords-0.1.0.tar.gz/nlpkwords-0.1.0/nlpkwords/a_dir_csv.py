import pandas as pd
import heapq

def read_graph_and_heuristic_from_csv(graph_file, heuristic_file):
    graph = {}
    heuristics = {}
    
    graph_df = pd.read_csv(graph_file)
    heuristic_df = pd.read_csv(heuristic_file)
    
    for _, row in graph_df.iterrows():
        src, dest, weight = row['Source'], row['Destination'], row['Weight']
        graph.setdefault(src, []).append((dest, weight))
    
    for _, row in heuristic_df.iterrows():
        node, h = row['Node'], row['Heuristic']
        heuristics[node] = h
        
    return graph, heuristics

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

def main():
    graph_file = 'graph.csv'
    heuristic_file = 'heuristic.csv'
    graph, heuristics = read_graph_and_heuristic_from_csv(graph_file, heuristic_file)
    start = input("Enter start node: ")
    goal = input("Enter goal node: ")
    a_star(graph, heuristics, start, goal)

if __name__ == "__main__":
    main()
