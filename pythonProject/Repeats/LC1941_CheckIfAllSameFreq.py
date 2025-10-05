from black.trans import defaultdict


class Solution:
    def areOccurrencesEqual(self, s: str) -> bool:
        counts = defaultdict(int)
        for c in s:
            counts[c] += 1

        #print(counts)
        get_set = set()
        for i in counts.values():
            get_set.add(i)
        return len(get_set) == 1

if __name__ == "__main__":
    s = "abacbc"
    print(Solution().areOccurrencesEqual(s))
    s = "aaabb"
    print(Solution().areOccurrencesEqual(s))