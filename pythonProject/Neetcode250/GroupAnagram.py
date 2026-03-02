from collections import defaultdict
from typing import List


class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        groups = defaultdict(list)
        for s in strs:
            key = tuple(sorted(s))
            print(key)
            groups[key].append(s)
        return list(groups.values())


if __name__ == "__main__":
    solution = Solution()
    strs = ["act", "pots", "tops", "cat", "stop", "hat"]
    print(solution.groupAnagrams(strs))

