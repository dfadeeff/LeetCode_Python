import heapq
from collections import defaultdict


class Solution:
    def reorganizeString(self, s: str) -> str:
        count = defaultdict(int)
        for c in s:
            count[c] += 1
        print(count)

        maxheap = [[-cnt, char] for char, cnt in count.items()]
        heapq.heapify(maxheap)

        prev = None
        res = ""
        while maxheap or prev:

            if prev and not maxheap:
                return ""
            # most frequent char except equal to prev
            cnt, char = heapq.heappop(maxheap)
            res += char
            cnt += 1  # since cnt is negative
            if prev:
                heapq.heappush(maxheap, prev)
                prev = None

            if cnt != 0:
                prev = [cnt, char]

        return res


if __name__ == "__main__":
    s = "aab"
    print(Solution().reorganizeString(s))
