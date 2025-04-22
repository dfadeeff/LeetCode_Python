from typing import List
from collections import defaultdict, deque


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def distanceK(self, root: TreeNode, target: TreeNode, k: int) -> List[int]:
        # 1) Build an undirected adjacency list of all TreeNode references
        graph = defaultdict(list)

        def build(u):
            if not u:
                return
            for v in (u.left, u.right):
                if v:
                    graph[u].append(v)
                    graph[v].append(u)
                    build(v)

        build(root)

        # 2) BFS from target outwards for exactly K layers
        res = []
        seen = {target}
        q = deque([(target, 0)])  # (node, distance from target)
        while q:
            node, dist = q.popleft()
            if dist == k:
                res.append(node.val)
            elif dist < k:
                for nei in graph[node]:
                    if nei not in seen:
                        seen.add(nei)
                        q.append((nei, dist + 1))
        return res


if __name__ == "__main__":
    root = TreeNode(3)
    root.left = TreeNode(5)
    root.right = TreeNode(1)
    root.left.left = TreeNode(6)
    root.left.right = TreeNode(2)
    root.left.right.left = TreeNode(7)
    root.left.right.right = TreeNode(4)
    root.right.left = TreeNode(0)
    root.right.right = TreeNode(8)
    target = root.left
    k = 2
    print(Solution().distanceK(root, target, k))
