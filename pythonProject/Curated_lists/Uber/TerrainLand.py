class TerrainLand:
    def __init__(self):
        self.land = set()

    def addLand(self, x, y):
        self.land.add((x, y))

    def isLand(self, x, y):
        return (x, y) in self.land

    def getIsland(self):
        visited = set()
        count = 0

        def dfs(x, y):
            if (x, y) not in self.land or (x, y) in visited:
                return
            visited.add((x, y))

            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                dfs(x + dx, y + dy)

        for (x, y) in self.land:
            if (x, y) not in visited:
                dfs(x, y)
                count += 1

        return count


if __name__ == "__main__":
    t = TerrainLand()
    t.addLand(1, 0)
    t.addLand(2, 0)
    t.addLand(4, 0)
    print(t.getIsland())
