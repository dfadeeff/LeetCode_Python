from collections import Counter
from typing import List


class Solution:
    def numFriendRequests(self, ages: List[int]) -> int:
        count = Counter(ages)
        print(count)
        res = 0
        for age_x in count:
            for age_y in count:
                if age_y <= 0.5 * age_x + 7:
                    continue
                if age_y > age_x:
                    continue
                if age_y > 100 and age_x < 100:
                    continue
                # count[x] * count[y]
                if age_x == age_y:
                    res += count[age_x] * (count[age_x] - 1)
                else:
                    res += count[age_x] * count[age_y]
        return res


if __name__ == '__main__':
    ages = [16, 17, 18]
    print(Solution().numFriendRequests(ages))
    ages = [16, 16]
    print(Solution().numFriendRequests(ages))


