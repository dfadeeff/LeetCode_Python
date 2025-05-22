import heapq
from typing import List

from black.trans import defaultdict


class Pair:
    def __init__(self, word, freq):
        self.word = word
        self.freq = freq

    def __lt__(self, p):
        return self.freq < p.freq or (self.freq == p.freq and self.word > p.word)


class Solution:
    def topKFrequent(self, words: List[str], k: int) -> List[str]:
        heap = []
        hashmap = defaultdict(int)
        for w in words:
            hashmap[w] += 1
        print(hashmap)
        for word, freq in hashmap.items():
            heapq.heappush(heap, Pair(word, freq))
            if len(heap) > k:
                heapq.heappop(heap)

        return [p.word for p in sorted(heap, reverse=True)]


if __name__ == "__main__":
    strs = ['go', 'coding', 'byte', 'byte', 'go', 'interview', 'go']
    k = 2
    print(Solution().topKFrequent(strs, k))
    strs = ["byte", "byte", "go", "city"]
    k = 2
    print(Solution().topKFrequent(strs, k))
