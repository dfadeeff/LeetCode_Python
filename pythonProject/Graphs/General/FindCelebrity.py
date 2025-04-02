# The knows API is already defined for you.
# return a bool, whether a knows b
# def knows(a: int, b: int) -> bool:


def knows(a: int, b: int) -> bool:
    return graph[a][b] == 1


class Solution:
    def findCelebrity(self, n: int) -> int:

        """
        knows(a, b)  # returns True if a knows b
        a → b  (a has a directed edge to b)

        """
        # Step 1: Find the candidate
        candidate = 0
        for i in range(1, n):
            if knows(candidate, i): # True if candidate knows i
                candidate = i

            # Step 2: Validate the candidate
        for i in range(n):
            if i == candidate:
                continue
            # Celebrity should not know anyone,
            # and everyone should know the celebrity
            if knows(candidate, i) or not knows(i, candidate):
                return -1
        return candidate


if __name__ == '__main__':
    graph = [[1, 1, 0], [0, 1, 0], [1, 1, 1]]
    print(Solution().findCelebrity(3))
