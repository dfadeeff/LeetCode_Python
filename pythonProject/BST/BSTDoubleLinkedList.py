class Node:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def treeToDoublyList(self, root: 'Optional[Node]') -> 'Optional[Node]':
        if not root:
            return None  # 👈 Check for empty tree!

        collect_nodes = []

        def dfs(node):
            if node is None:
                return
            dfs(node.left)
            collect_nodes.append(node)
            dfs(node.right)

        dfs(root)
        # print(collect_nodes)
        for i in range(len(collect_nodes)):
            prev = collect_nodes[i - 1]
            curr = collect_nodes[i]
            curr.left = prev
            prev.right = curr
        collect_nodes[0].left = collect_nodes[-1]
        collect_nodes[-1].right = collect_nodes[0]

        return collect_nodes[0]


if __name__ == '__main__':
    root = Node(4)
    root.left = Node(2)
    root.right = Node(5)
    root.left.left = Node(1)
    root.left.right = Node(3)
    print(Solution().treeToDoublyList(root))
