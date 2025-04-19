import re


class Solution:
    def isPalindrome(self, s: str, include) -> bool:
        #cleaned = re.sub(r'[^A-Za-z0-9]', '', s.lower())
        cleaned = re.sub(r'[^A-Za-z0-9]', '', s)

        brute_force = ""
        for c in cleaned:
            if c in include:
                brute_force += c

        left, right = 0 , len(brute_force)-1
        while left < right:
            if brute_force[left] != brute_force[right]:
               return False
            left += 1
            right -= 1

        return True

    def isPalindromeOptimisedSpace(self, s: str, include) -> bool:
        cleaned = re.sub(r'[^A-Za-z0-9]', '', s)
        include_set = set(include)  # For O(1) lookup
        left, right = 0, len(cleaned) - 1

        while left < right:
            while left < right and cleaned[left] not in include_set:
                left += 1
            while left < right and cleaned[right] not in include_set:
                right -= 1

            if cleaned[left] != cleaned[right]:
                return False
            left += 1
            right -= 1

        return True





if __name__ == "__main__":
    s = "racecarX"
    include = {'r','X'}
    print(Solution().isPalindrome(s,include))
    print(Solution().isPalindromeOptimisedSpace(s, include))
    s = "Yo, banana boY"
    include = {"Y","b","o","a","n"}
    print(Solution().isPalindrome(s, include))
    print(Solution().isPalindromeOptimisedSpace(s, include))
