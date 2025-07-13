from typing import List


class Solution:
    def numRescueBoats(self, people: List[int], limit: int) -> int:
        ans = 0
        left = 0
        right = len(people) - 1
        people.sort()

        while left <= right:
            if people[left] + people[right] <= limit:
                # include also the lightest person, ie increment i
                left += 1 # lightest boards too
            # put the heaviest person on the boat
            right -= 1
            ans += 1

        return ans


if __name__ == "__main__":
    people = [1, 2]
    limit = 3
    print(Solution().numRescueBoats(people, limit))
