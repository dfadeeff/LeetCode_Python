from collections import defaultdict, Counter


class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if t == "":
            return ""

        countT = Counter(t)
        window = defaultdict(int)

        # need = 3 because we have 3 unique characters in t, example t = "ABC",s = "ADOBECODEBANC"
        # have tracks how many of those characters we’ve fully satisfied in the current window
        have, need = 0, len(countT)
        # res will store indices [start, end] of the best (smallest valid) window found so far
        # 	resLen stores the length of that best window
        res, resLen = [-1, -1], float("inf")

        left = 0

        for right in range(len(s)):
            c = s[right]
            window[c] += 1

            # does that count satisfy what we are looking for
            if c in countT and window[c] == countT[c]:
                have += 1

            while have == need:
                # update the result
                if right - left + 1 < resLen:
                    res = [left, right]
                    resLen = right - left + 1

                window[s[left]] -= 1
                if s[left] in countT and window[s[left]] < countT[s[left]]:
                    have -= 1
                left += 1
        # unpacks the best window indices stored in res
        left, right = res

        return s[left:right + 1] if resLen != float("inf") else ""


if __name__ == "__main__":
    s = "ADOBECODEBANC"
    t = "ABC"
    print(Solution().minWindow(s, t))
