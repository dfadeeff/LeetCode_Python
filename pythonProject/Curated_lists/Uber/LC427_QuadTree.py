from typing import List


# Definition for a QuadTree node.
class Node:
    def __init__(self, val, isLeaf, topLeft=None, topRight=None,
                 bottomLeft=None, bottomRight=None):
        self.val = val
        self.isLeaf = isLeaf
        self.topLeft = topLeft
        self.topRight = topRight
        self.bottomLeft = bottomLeft
        self.bottomRight = bottomRight


class Solution:
    """
        Rule 1: If ALL cells in the current region are the SAME value
        → Make a LEAF node with that value. Done.

        Rule 2: If the cells are MIXED (some 0s, some 1s)
        → Split into 4 equal quadrants
        → Recurse on each quadrant
    """

    def construct(self, grid: List[List[int]]) -> 'Node':
        return self.build(grid, 0, 0, len(grid))

    def sameValue(self, grid, x, y, sideLength):
        value = grid[x][y]
        for i in range(x, x + sideLength):
            for j in range(y, y + sideLength):
                if grid[i][j] != value:
                    return False

        return True

    def build(self, grid, x, y, sideLength):
        if self.sameValue(grid, x, y, sideLength):
            return Node(grid[x][y], True)

        root = Node(0, False)
        newSideLength = sideLength // 2
        root.topLeft = self.build(grid, x, y, newSideLength)
        root.topRight = self.build(grid, x, y + newSideLength, newSideLength)
        root.bottomLeft = self.build(grid, x + newSideLength, y, newSideLength)
        root.bottomRight = self.build(grid, x + newSideLength, y + newSideLength, newSideLength)

        return root


def print_tree(node, indent=0):
    """Pretty print the quad tree"""
    prefix = "  " * indent
    if node.isLeaf:
        print(f"{prefix}Leaf(val={node.val})")
    else:
        print(f"{prefix}Node(not leaf)")
        print(f"{prefix}  TL:");
        print_tree(node.topLeft, indent + 2)
        print(f"{prefix}  TR:");
        print_tree(node.topRight, indent + 2)
        print(f"{prefix}  BL:");
        print_tree(node.bottomLeft, indent + 2)
        print(f"{prefix}  BR:");
        print_tree(node.bottomRight, indent + 2)


if __name__ == "__main__":
    sol = Solution()

    # Test 1: 2x2 mixed
    grid1 = [[0, 1], [1, 0]]
    print("=== Grid 1 (2x2 mixed) ===")
    root1 = sol.construct(grid1)
    print_tree(root1)

    # Test 2: 4x4
    grid2 = [[1, 1, 0, 0],
             [1, 1, 0, 0],
             [0, 0, 0, 0],
             [0, 0, 0, 0]]
    print("\n=== Grid 2 (4x4) ===")
    root2 = sol.construct(grid2)
    print_tree(root2)
