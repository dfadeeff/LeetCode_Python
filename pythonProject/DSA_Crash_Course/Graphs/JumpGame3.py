from collections import deque
from typing import List


class Solution:
    def canReach(self, arr: List[int], start: int) -> bool:
        n = len(arr)
        queue = deque([start])  # Initialize the queue with the starting index
        seen = set()  # To track visited nodes

        while queue:
            node = queue.popleft()  # Pop from the front of the queue

            # Check if we can reach a zero
            if arr[node] == 0:
                return True

            # If the node is already visited (seen set), skip it
            if node in seen:
                continue

            # Mark this node as visited
            seen.add(node)

            # Explore the neighbors (next possible jumps)
            for i in [node + arr[node], node - arr[node]]:
                if 0 <= i < n:  # Check if the next index is within bounds
                    queue.append(i)  # Add to the queue for further exploration

        return False  # If we exhaust the queue and don't find a 0, return False


def main():
    arr = [4, 2, 3, 0, 3, 1, 2]
    start = 5
    print(Solution().canReach(arr, start))
    arr = [4, 2, 3, 0, 3, 1, 2]
    start = 0
    print(Solution().canReach(arr, start))


if __name__ == '__main__':
    main()
