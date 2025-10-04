class Solution:

    def runningSum(self, nums):
        prefix = [nums[0]]
        for i in range(1, len(nums)):
            prefix.append(nums[i] + prefix[i - 1])

        return prefix


if __name__ == "__main__":
    nums = [1, 2, 3, 4]
    print(Solution().runningSum(nums))
