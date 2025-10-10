class Tree:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def flatten(self, root):
        nodes = []

        def dfs(node):
            if not node:
                return

            nodes.append(node)
            dfs(node.left)
            dfs(node.right)

        dfs(root)

        # link the nodes
        for i in range(1, len(nodes)):
            prev = nodes[i - 1]
            curr = nodes[i]
            prev.left = None
            prev.right = curr

        return root


if __name__ == "__main__":
    root = Tree(1)
    root.left = Tree(2)
    root.right = Tree(5)
    root.left.left = Tree(3)
    root.left.right = Tree(4)
    root.right.right = Tree(6)
    Solution().flatten(root)
    curr = root
    while curr:
        print(curr.val, end=" -> ")
        curr = curr.right
