class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.parent = None


class Solution:
    def lowestCommonAncestor(self, p: 'Node', q: 'Node') -> 'Node':
        p_copy = p
        q_copy = q
        while p_copy != q_copy:
            p_copy = p_copy.parent if p_copy else q
            q_copy = q_copy.parent if q_copy else p

        return q_copy


if __name__ == '__main__':
    root = Node(3)
    root.left = Node(5)
    root.left.parent = root
    root.left.left = Node(6)
    root.left.left.parent = root.left
    root.left.right = Node(2)
    root.left.right.parent = root.left
    root.left.right.left = Node(7)
    root.left.right.left.parent = root.left.right
    root.left.right.right = Node(4)
    root.left.right.right.parent = root.left.right
    root.right = Node(1)
    root.right.parent = root
    root.right.left = Node(0)
    root.right.left.parent = root.right
    root.right.right = Node(8)
    root.right.right.parent = root.right

    p = root.left  # Node 5
    q = root.right  # Node 1

    result = Solution().lowestCommonAncestor(p, q)
    print(result.val)  # Should print 3
