from collections import deque
from typing import Optional


# Definition for a Node.
class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


class Solution:
    def cloneGraphDFS(self, node: Optional['Node']) -> Optional['Node']:
        if not node:
            return None
        cloned = {}
        def dfs(node):
            if node in cloned:
                return cloned[node]
            copy = Node(node.val)
            cloned[node] = copy
            for neighbor in node.neighbors:
                copy.neighbors.append(dfs(neighbor))
            return copy
        return dfs(node)


    def cloneGraphBFS(self, node: Optional['Node']) -> Optional['Node']:
        if not node:
            return None

        cloned = {node: Node(node.val)}
        queue = deque([node])

        while queue:
            curr = queue.popleft()
            for neighbor in curr.neighbors:
                if neighbor not in cloned:
                    cloned[neighbor] = Node(neighbor.val)
                    queue.append(neighbor)
                cloned[curr].neighbors.append(cloned[neighbor])

        return cloned[node]

if __name__ == '__main__':
    adjList = [[2, 4], [1, 3], [2, 4], [1, 3]]
    print(Solution().cloneGraphDFS(adjList))