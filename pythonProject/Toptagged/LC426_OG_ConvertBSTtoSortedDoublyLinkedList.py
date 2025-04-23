# Definition for a Node.
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def treeToDoublyListV1(self, root: 'Optional[Node]') -> 'Optional[Node]':
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

    def treeToDoublyListV2(self, root: 'Optional[Node]') -> 'Optional[Node]':
        if not root:
            return None

        self.first = None
        self.last  = None

        def dfs(node):
            if not node:
                return
            dfs(node.left)

            if self.last is None:
                # first node seen
                self.first = node
            else:
                node.left       = self.last
                self.last.right = node

            self.last = node
            dfs(node.right)

        dfs(root)

        # close the circle
        self.first.left  = self.last
        self.last.right  = self.first
        return self.first




if __name__ == "__main__":
    root = TreeNode(4)
    root.left = TreeNode(2)
    root.right = TreeNode(5)
    root.left.left = TreeNode(1)
    root.left.right = TreeNode(3)

    head = Solution().treeToDoublyListV2(root)
    if not head:
        print("[]")
    else:
        # walk once around the circle, collecting values
        vals = []
        cur = head
        while True:
            vals.append(str(cur.val))
            cur = cur.right
            if cur is head:
                break

        # print in a->b->c form
        print(" <-> ".join(vals))
