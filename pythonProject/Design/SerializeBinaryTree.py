# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Codec:

    def serialize(self, root):
        """Encodes a tree to a single string.
        Serialize: tree -> string, use preorder
        :type root: TreeNode
        :rtype: str
        """

        vals = []

        def dfs(node):
            if not node:
                vals.append('#')
                return
            vals.append(str(node.val))
            dfs(node.left)
            dfs(node.right)

        dfs(root)
        return ",".join(vals)

    def deserialize(self, data):
        """Decodes your encoded data to tree.
        # Deserialize: string -> tree
        :type data: str
        :rtype: TreeNode
        """
        vals = iter(data.split(','))
        print(vals)

        def dfs():
            val = next(vals)
            if val == '#':
                return None
            node = TreeNode(int(val))
            node.left = dfs()
            node.right = dfs()
            return node

        return dfs()


def print_preorder(node):
    if not node:
        print('#', end=' ')
        return
    print(node.val, end=' ')
    print_preorder(node.left)
    print_preorder(node.right)


if __name__ == '__main__':
    # Build your tree
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.right.left = TreeNode(4)
    root.right.right = TreeNode(5)

    ser = Codec()
    deser = Codec()

    serialized_data = ser.serialize(root)
    print("Serialized string:", serialized_data)

    ans = deser.deserialize(serialized_data)
    print("Preorder of deserialized tree:")
    print_preorder(ans)
