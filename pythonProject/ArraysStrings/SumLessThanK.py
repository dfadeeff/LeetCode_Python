class Solution:
    def sumLessThanK(self, nums, k):
        left = 0
        curr = 0
        ans = 0

        for right in range(0, len(nums)):
            curr += nums[right]

            while curr > k:
                curr -= nums[left]
                left += 1
            ans = max(ans, right - left + 1)
        return ans


if __name__ == "__main__":
    nums = [3, 1, 2, 7, 4, 2, 1, 1, 5]
    k = 8
    print(Solution().sumLessThanK(nums, k))
