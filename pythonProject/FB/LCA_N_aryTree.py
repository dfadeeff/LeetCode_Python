class Node:
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children or []


class Solution:
    def lowestCommonAncestor(self, root: 'Node', p: 'Node', q: 'Node') -> 'Node':
        if not root:
            return None

        if root == p or root == q:
            return root

        # Recurse for all children
        found = []
        for child in root.children:
            res = self.lowestCommonAncestor(child, p, q)
            if res:
                found.append(res)

        # If at least two children return non-null, current is LCA
        if len(found) >= 2:
            return root

        # Else, return non-null child result, or None
        return found[0] if found else None


if __name__ == '__main__':
    # Tree:
    #         1
    #     /   |  \
    #     2   3   4
    #        / \
    #       5   6

    node5 = Node(5)
    node6 = Node(6)
    node3 = Node(3, [node5, node6])
    node2 = Node(2)
    node4 = Node(4)
    root = Node(1, [node2, node3, node4])

    p = node5
    q = node2

    sol = Solution()
    lca = sol.lowestCommonAncestor(root, p, q)
    print(f"LCA of {p.val} and {q.val} is: {lca.val}")
