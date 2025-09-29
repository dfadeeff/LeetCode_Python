class Solution:

    def productLessThanK(self, nums, k):
        if k <= 1:
            return 0

        left = 0
        ans = 0
        curr = 1
        for right in range(len(nums)):
            curr *= nums[right]
            while curr >= k:
                curr //= nums[left]
                left += 1
            ans += right - left + 1

        return ans


if __name__ == "__main__":
    nums = [10, 5, 2, 6]
    k = 100
    print(Solution().productLessThanK(nums, k))
