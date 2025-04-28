import pandas as pd

def dfs_recursive(graph, node, visited):
    if node not in visited:
        print(node, end=" ")
        visited.add(node)
        for neighbor in graph[node]:
            dfs_recursive(graph, neighbor, visited)

def read_graph_from_csv(file_path):
    df = pd.read_csv(file_path)
    graph = {}
    for _, row in df.iterrows():
        src, dest = row['Source'], row['Destination']
        graph.setdefault(src, []).append(dest)
        graph.setdefault(dest, []).append(src)
    return graph

def main():
    file_path = 'graph.csv'  # Change this path if needed
    graph = read_graph_from_csv(file_path)
    start_node = input("Enter the starting node: ")
    visited = set()
    print("DFS Traversal:")
    dfs_recursive(graph, start_node, visited)

if __name__ == "__main__":
    main()
