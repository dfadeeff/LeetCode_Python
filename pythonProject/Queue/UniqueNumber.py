from collections import Counter, deque
from typing import List


class FirstUnique:

    def __init__(self, nums: List[int]):
        self.count = Counter()  # Count occurrences
        self.queue = deque()  # Maintain order of unique numbers

        for num in nums:
            self.add(num)

    def showFirstUnique(self) -> int:
        while self.queue and self.count[self.queue[0]] > 1:
            self.queue.popleft()
        return self.queue[0] if self.queue else -1

    def add(self, value: int) -> None:
        self.count[value] += 1
        # Only add to queue the first time we see it
        if self.count[value] == 1:
            self.queue.append(value)


# Your FirstUnique object will be instantiated and called as such:

if __name__ == "__main__":
    firstUnique = FirstUnique([2, 3, 5])
    print(firstUnique.showFirstUnique())  # ➞ 2
    firstUnique.add(5)
    print(firstUnique.showFirstUnique())  # ➞ 2
    firstUnique.add(2)
    print(firstUnique.showFirstUnique())  # ➞ 3
    firstUnique.add(3)
    print(firstUnique.showFirstUnique())  # ➞ -1
