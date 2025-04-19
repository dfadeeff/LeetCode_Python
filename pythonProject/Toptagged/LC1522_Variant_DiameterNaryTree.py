# Definition for a Node.
from typing import Optional, List


class Node:
    def __init__(self, val: Optional[int] = None, children: Optional[List['Node']] = None):
        self.val = val
        self.children = children if children is not None else []


class Solution:
    def diameter(self, root: 'Node') -> int:
        """
        :type root: 'Node'
        :rtype: int
        """
        if not root:
            return 0

        diameter = 0

        def dfs(node):
            nonlocal diameter
            if not node:
                return 0
            # two longest paths
            first, second = 0, 0
            for child in node.children:
                depth = dfs(child)

                if depth > first:
                    second = first
                    first = depth
                elif depth > second:
                    second = depth
            diameter = max(diameter, first + second)

            return first + 1

        dfs(root)
        return diameter


if __name__ == "__main__":
    #               1
    #             / | \
    #            3  2  4
    #           / |
    #          5  6

    # Example: root = [1,null,3,2,4,null,5,6], diameter = 3
    nodes = {i: Node(i) for i in range(1, 7)}
    # Level 1 children of 1: 3,2,4
    nodes[1].children = [nodes[3], nodes[2], nodes[4]]
    # Level 2 children of 3: 5,6
    nodes[3].children = [nodes[5], nodes[6]]
