class Solution:
    def numKLenSubstrNoRepeats(self, s: str, k: int) -> int:
        if k > len(s):
            return 0
        seen = set()
        left = 0
        answer = 0
        for right in range(len(s)):
            while s[right] in seen:
                seen.remove(s[left])
                left += 1
            seen.add(s[right])
            # When window is of size k, check and move
            if right - left + 1 == k:
                answer += 1
                seen.remove(s[left])
                left += 1

        return answer


if __name__ == '__main__':
    s = "havefunonleetcode"
    k = 5
    print(Solution().numKLenSubstrNoRepeats(s, k))
