class Node:
    def __init__(self, val=0, left=None, right=None, random=None):
        self.val = val
        self.left = left
        self.right = right
        self.random = random


class NodeCopy:
    def __init__(self, val=0, left=None, right=None, random=None):
        self.val = val
        self.left = left
        self.right = right
        self.random = random


class Solution:
    def copyRandomBinaryTree(self, root: "Optional[Node]") -> "Optional[NodeCopy]":
        visited = {}

        def dfs(root) -> "Optional[NodeCopy]":
            if root is None:
                return None
            if root in visited:
                return visited[root]
            copy = NodeCopy(root.val)
            visited[root] = copy
            copy.left = dfs(root.left)
            copy.right = dfs(root.right)
            copy.random = dfs(root.random)
            return copy

        return dfs(root)


if __name__ == "__main__":
    # Build a small tree:
    #      (1)
    #      / \
    #    (2) (3)
    #
    # With random pointers:
    # 1.random -> 3
    # 2.random -> None
    # 3.random -> 2

    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)

    root.random = root.right  # 1 → 3
    root.left.random = None  # 2 → None
    root.right.random = root.left  # 3 → 2

    # Clone it
    clone = Solution().copyRandomBinaryTree(root)

    # Now print (val, left.val, right.val, random.val) for each original & clone
    originals = [root, root.left, root.right]
    copies = [clone, clone.left, clone.right]

    print("orig      | clone")
    print("---       | -----")
    for o, c in zip(originals, copies):
        o_l = o.left.val if o.left else None
        o_r = o.right.val if o.right else None
        o_x = o.random.val if o.random else None

        c_l = c.left.val if c.left else None
        c_r = c.right.val if c.right else None
        c_x = c.random.val if c.random else None

        print(f"{o.val, o_l, o_r, o_x} | {c.val, c_l, c_r, c_x}")
