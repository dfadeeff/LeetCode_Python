# Definition for a binary tree node.
class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.parent = None


class Solution:

    def lowestCommonAncestorSet(self, p: 'Node', q: 'Node') -> 'Node':
        """In contrast to LCA, there is NO root, only parent, so go up"""
        ancestors = set()

        # Add all ancestors of p to the set
        while p:
            ancestors.add(p)
            p = p.parent

        while q:
            if q in ancestors:
                return q
            q = q.parent
        return None

    def lowestCommonAncestorTwoPointers(self, p: 'Node', q: 'Node') -> 'Node':
        a,b, = p,q
        while a != b:
            a = a.parent if a else q
            b = b.parent if b else p
        return a


if __name__ == '__main__':
    # Build tree
    root = Node(3)
    root.left = Node(5)
    root.right = Node(1)
    root.left.left = Node(6)
    root.left.right = Node(2)
    root.left.right.left = Node(7)
    root.left.right.right = Node(4)
    root.right.left = Node(0)
    root.right.right = Node(8)

    # Set parent pointers
    root.left.parent = root
    root.right.parent = root
    root.left.left.parent = root.left
    root.left.right.parent = root.left
    root.left.right.left.parent = root.left.right
    root.left.right.right.parent = root.left.right
    root.right.left.parent = root.right
    root.right.right.parent = root.right

    # Test
    p = root.left            # Node 5
    q = root.right           # Node 1
    lca = Solution().lowestCommonAncestorSet(p, q)
    print(f"LCA of {p.val} and {q.val} is: {lca.val}")
    lca = Solution().lowestCommonAncestorTwoPointers(p, q)
    print(f"LCA of {p.val} and {q.val} is: {lca.val}")
