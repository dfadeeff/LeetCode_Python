# Definition for a Node.
from collections import deque
from typing import Optional

class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

class Solution:
    def cloneGraphDFS(self, nodes: dict) -> dict:
        cloned = {}  # Original node ➔ cloned node mapping

        def dfs(node):
            if node in cloned:
                return cloned[node]
            copy = Node(node.val)  # Clone current node
            cloned[node] = copy
            for neighbor in node.neighbors:
                copy.neighbors.append(dfs(neighbor))  # Recursively clone neighbors
            return copy

        # Loop over all nodes to handle disconnected graphs
        for node in nodes.values():
            if node not in cloned:
                dfs(node)

        return cloned

def build_graph(adjList):
    if not adjList:
        return {}

    # Create all nodes
    nodes = {i: Node(i) for i in range(1, len(adjList) + 1)}

    # Connect nodes according to adjacency list
    for idx, neighbors in enumerate(adjList, 1):
        nodes[idx].neighbors = [nodes[neighbor] for neighbor in neighbors]

    return nodes  # ✅ Return the full dict of nodes!

if __name__ == '__main__':
    # Two disconnected components: (1-2), (3-4)
    adjList = [[2], [1], [4], [3]]
    all_nodes = build_graph(adjList)  # ✅ Now returns full dict!

    cloned_nodes = Solution().cloneGraphDFS(all_nodes)

    # Print cloned nodes
    for node in cloned_nodes.values():
        print(f"Node {node.val}: {[n.val for n in node.neighbors]}")