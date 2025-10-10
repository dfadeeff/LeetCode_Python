class Solution:

    def remove(self, nums):
        k = 0
        for i in range(1, len(nums)):
            if nums[i] == nums[i - 1]:
                nums[k] = nums[i]
                k += 1
        return k


if __name__ == "__main__":
    nums = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
    print(Solution().remove(nums))
