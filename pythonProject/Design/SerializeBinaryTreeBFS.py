# Definition for a binary tree node.
from collections import deque


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
        if not root:
            return "#"

        result = []
        queue = deque([root])

        while queue:
            node = queue.popleft()
            if node:
                result.append(str(node.val))
                queue.append(node.left)
                queue.append(node.right)
            else:
                result.append("#")

        return ",".join(result)

    def deserialize(self, data):
        """Decodes your encoded data to tree.
        # Deserialize: string -> tree
        :type data: str
        :rtype: TreeNode
        """
        if data == "#":
            return None

        nodes = data.split(",")
        root = TreeNode(int(nodes[0]))
        queue = deque([root])
        index = 1

        while queue:
            node = queue.popleft()
            if nodes[index] != "#":
                node.left = TreeNode(int(nodes[index]))
                queue.append(node.left)
            index += 1

            if nodes[index] != "#":
                node.right = TreeNode(int(nodes[index]))
                queue.append(node.right)
            index += 1

        return root


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
