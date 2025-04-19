# Definition for a Node.
class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.parent = None


class Solution:
    def lowestCommonAncestor(self, p: 'Node', q: 'Node') -> 'Node':
        a, b = p, q
        while a != b:
            a = a.parent if a else q
            b = b.parent if b else p
        return a


if __name__ == "__main__":
    # Build tree nodes
    nodes = {val: Node(val) for val in [3, 5, 1, 6, 2, 0, 8, 7, 4]}

    # Manually link the tree structure (with parent pointers)
    nodes[3].left = nodes[5]
    nodes[3].right = nodes[1]
    nodes[5].parent = nodes[3]
    nodes[1].parent = nodes[3]

    nodes[5].left = nodes[6]
    nodes[5].right = nodes[2]
    nodes[6].parent = nodes[5]
    nodes[2].parent = nodes[5]

    nodes[1].left = nodes[0]
    nodes[1].right = nodes[8]
    nodes[0].parent = nodes[1]
    nodes[8].parent = nodes[1]

    nodes[2].left = nodes[7]
    nodes[2].right = nodes[4]
    nodes[7].parent = nodes[2]
    nodes[4].parent = nodes[2]
    lca = Solution().lowestCommonAncestor(nodes[7], nodes[4])
    print(lca.val)
    lca = Solution().lowestCommonAncestor(nodes[6], nodes[4])
    print(lca.val)
