from typing import List


class Solution:
    def minAbbreviation(self, target: str, dictionary: List[str]) -> str:
        """Problem: Leetcode 411
        Given a target string target and an array of strings dictionary, return an abbreviation of target with the shortest possible length such that it is not an abbreviation of any string in dictionary. If there are multiple shortest abbreviations, return any of them.
        Given target word and a list of dictionary words, return the minimum length abbreviation of the target that does not conflict with any word in the dictionary."""
        m = len(target)
        diffs = []

        for word in dictionary:
            if len(word) != m:
                continue
            diff = 0
            for i in range(m):
                if target[i] != word[i]:
                    diff |= 1 << i
            diffs.append(diff)

        if not diffs:
            return str(m)

        res = None
        min_len = float('inf')

        def abbr_len(mask):
            count, length = 0, 0
            for i in range(m):
                if mask & (1 << i):
                    if count:
                        length += len(str(count))
                        count = 0
                    length += 1
                else:
                    count += 1
            if count:
                length += len(str(count))
            return length

        def dfs(pos, mask):
            nonlocal res, min_len
            if pos == m:
                for d in diffs:
                    if (mask & d) == 0:
                        return
                length = abbr_len(mask)
                if length < min_len:
                    min_len = length
                    res = mask
                return
            dfs(pos + 1, mask)
            dfs(pos + 1, mask | (1 << pos))

        dfs(0, 0)

        def build(mask):
            ans = []
            count = 0
            for i in range(m):
                if mask & (1 << i):
                    if count:
                        ans.append(str(count))
                        count = 0
                    ans.append(target[i])
                else:
                    count += 1
            if count:
                ans.append(str(count))
            return ''.join(ans)

        return build(res)


if __name__ == '__main__':
    target = "apple"
    dictionary = ["blade"]
    print(Solution().minAbbreviation(target, dictionary))
