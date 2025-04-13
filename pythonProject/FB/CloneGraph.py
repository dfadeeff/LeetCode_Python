# Definition for a Node.
from collections import deque


class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


from typing import Optional


class Solution:
    def cloneGraphBFS(self, node: Optional['Node']) -> Optional['Node']:
        """BFS variant"""
        if not node:
            return None

        cloned = {node: Node(node.val)} # Mapping original ➔ clone
        queue = deque([node]) # Start BFS from given node

        while queue:
            curr = queue.popleft()
            for neighbor in curr.neighbors:
                if neighbor not in cloned:
                    cloned[neighbor] = Node(neighbor.val)
                    queue.append(neighbor)
                cloned[curr].neighbors.append(cloned[neighbor])

        return cloned[node]

    def cloneGraphDFS(self, node: Optional['Node']) -> Optional['Node']:
        if not node:
            return None
        cloned = {}  # Original node ➔ cloned node mapping

        def dfs(node):
            if node in cloned:
                return cloned[node]
            copy = Node(node.val)  # Clone current node
            cloned[node] = copy
            for neighbor in node.neighbors:
                copy.neighbors.append(dfs(neighbor))  # Recursively clone neighbors
            return copy

        return dfs(node)


def build_graph(adjList):
    if not adjList:
        return None

    nodes = {i: Node(i) for i in range(1, len(adjList) + 1)}

    for idx, neighbors in enumerate(adjList, 1):
        nodes[idx].neighbors = [nodes[neighbor] for neighbor in neighbors]

    return nodes[1]  # Return reference to the starting node


if __name__ == '__main__':
    adjList = [[2, 4], [1, 3], [2, 4], [1, 3]]
    start_node = build_graph(adjList)
    cloned_graph = Solution().cloneGraphBFS(start_node)
    print(cloned_graph.val)  # Should print 1 (or starting node val)
