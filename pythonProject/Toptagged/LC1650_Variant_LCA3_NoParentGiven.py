# Definition for a Node.
class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


class Solution:
    def lowestCommonAncestor(self, nodes: list['Node'], p: 'Node', q: 'Node') -> 'Node':
        # Step 1: Build child-to-parent map
        child_to_parent = {}
        for node in nodes:
            if node.left:
                child_to_parent[node.left] = node
            if node.right:
                child_to_parent[node.right] = node


        print("Parent -> [Left, Right]")
        for node in nodes_list:
            left_val = node.left.val if node.left else None
            right_val = node.right.val if node.right else None
            print(f"{node.val} -> [{left_val}, {right_val}]")

        # Step 2: Simulate parent pointers and use two-pointer trick
        a, b = p, q
        while a != b:
            a = child_to_parent[a] if a in child_to_parent else q
            b = child_to_parent[b] if b in child_to_parent else p
        return a


if __name__ == "__main__":
    # Build tree nodes
    # Build all nodes
    nodes_map = {val: Node(val) for val in [1, 2, 3, 4, 5, 6]}

    # Set up connections
    nodes_map[1].left = nodes_map[2]
    nodes_map[1].right = nodes_map[3]
    nodes_map[2].left = nodes_map[4]
    nodes_map[2].right = nodes_map[5]
    nodes_map[5].right = nodes_map[6]

    # Collect all nodes in a list (unordered)
    nodes_list = [nodes_map[i] for i in [2, 5, 4, 1, 3, 6]]  # as per screenshot

    # Run the solution

    lca = Solution().lowestCommonAncestor(nodes_list, nodes_map[4], nodes_map[6])
    print("LCA of 4 and 6:", lca.val)  # Expected output: 2
