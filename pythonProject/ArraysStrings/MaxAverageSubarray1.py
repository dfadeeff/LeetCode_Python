from typing import List


class Solution:
    def findMaxAverage(self, nums: List[int], k: int) -> float:
        left = 0
        answer = float("-inf")
        curr = 0
        for right in range(len(nums)):
            curr += nums[right]
            len_curr = right - left + 1
            while len_curr > k:
                curr -= nums[left]
                left += 1
                len_curr -= 1
            if len_curr == k:
                answer = max(answer, curr / k)


        return answer

if __name__ == '__main__':
    nums = [1, 12, -5, -6, 50, 3]
    k = 4
    print(Solution().findMaxAverage(nums, k))

