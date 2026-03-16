from typing import List


class Solution:
    def canVisitAllRooms(self, rooms: List[List[int]]) -> bool:
        def dfs(node):
            for neighbor in rooms[node]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    dfs(neighbor)

        seen = {0}
        dfs(0)
        return len(seen) == len(rooms)

if __name__ == "__main__":
    sol = Solution()
    rooms = [[1], [2], [3], []]
    print(sol.canVisitAllRooms(rooms))
    rooms = [[1, 3], [3, 0, 1], [2], [0]]
    print(sol.canVisitAllRooms(rooms))
