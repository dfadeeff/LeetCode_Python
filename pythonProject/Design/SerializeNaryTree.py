class TreeNode:
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children if children is not None else []


class Codec:

    def serialize(self, root):
        if not root:
            return "#"
        result = [str(root.val)]
        for child in root.children:
            result.append(self.serialize(child))
        result.append("#")  # delimiter to mark end of children
        return " ".join(result)  # ✅ add separator!

    def deserialize(self, data):
        if not data or data == "#":
            return None
        tokens = iter(data.split())

        def dfs():
            val = next(tokens)
            if val == '#':
                return None
            node = TreeNode(int(val))
            while True:
                child = dfs()
                if child is None:
                    break
                node.children.append(child)
            return node

        return dfs()


def print_preorder(node):
    if not node:
        print('#', end=' ')
        return
    print(node.val, end=' ')
    for child in node.children:
        print_preorder(child)


if __name__ == "__main__":
    root = TreeNode(1, [
        TreeNode(2),
        TreeNode(3, [TreeNode(5)]),
        TreeNode(4)
    ])

    codec = Codec()
    data = codec.serialize(root)
    print("Serialized:", data)

    new_root = codec.deserialize(data)
    print("Deserialized Preorder:")
    print_preorder(new_root)