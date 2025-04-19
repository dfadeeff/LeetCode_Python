class TreeNode:
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children if children is not None else []


class Solution:
    def lowestCommonAncestor(self, root: "TreeNode", p: "TreeNode", q: "TreeNode") -> "TreeNode":
        # Base case: if we hit None, or we find p or q, return it
        if not root or root == p or root == q:
            return root
        # Recurse into every child, collect any non‐null hits
        hits = []
        for child in root.children:
            res = self.lowestCommonAncestor(child, p, q)
            if res:
                hits.append(res)

        # If two or more children report back a hit, root is LCA
        if len(hits) >= 2:
            return root
        # If exactly one child did, bubble it up
        if len(hits) == 1:
            return hits[0]
        # Otherwise none found here
        return None


if __name__ == "__main__":
    #               1
    #             / | \
    #            3  2  4
    #           / |
    #          5  6
    # Example from the prompt: [1,null,3,2,4,null,5,6], p=5, q=2
    nodes = {v: TreeNode(v) for v in range(1, 7)}
    nodes[1].children = [nodes[3], nodes[2], nodes[4]]
    nodes[3].children = [nodes[5], nodes[6]]

    root = nodes[1]
    p = nodes[5]
    q = nodes[2]

    sol = Solution()
    lca = sol.lowestCommonAncestor(root, p, q)
    print("LCA of", p.val, "and", q.val, "is", lca.val)  # expected 1

