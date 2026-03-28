from typing import List


class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        # Path compression
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False  # already in same group, no merge happened

        # Union by rank: shorter tree goes under taller tree
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1

        return True


class Solution:
    def numIslands2(self, m: int, n: int, positions: List[List[int]]) -> List[int]:
        uf = UnionFind(m * n)
        grid = [[0] * n for _ in range(m)]

        count = 0
        results = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for r, c in positions:
            # Skip if already land (duplicate position)
            if grid[r][c] == 1:
                results.append(count)
                continue
            grid[r][c] = 1
            count += 1

            # Convert 2D (r,c) to 1D index
            index = r * n + c
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                # Neighbor must be in bounds AND be land
                if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1:
                    neighbor_index = nr * n + nc

                    # If they're in different groups, merge them
                    if uf.union(index, neighbor_index):
                        count -= 1  # two islands became one
            results.append(count)
        return results


if __name__ == "__main__":
    sol = Solution()
    m = 3
    n = 3
    positions = [[0, 0], [0, 1], [1, 2], [2, 1]]
    print(sol.numIslands2(m, n, positions))
