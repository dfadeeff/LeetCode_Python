from typing import List


class Solution:
    def rotateNSpace(self, nums: List[int], k: int) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        n = len(nums)
        temp = [0] * n
        for i in range(n):
            temp[(i + k) % n] = nums[i]
        # print(temp)
        nums[:] = temp  # modifies nums in-place

    def rotateConstant(self, nums: List[int], k: int) -> None:
        k = k % len(nums)
        l, r = 0, len(nums) - 1
        while l < r:
            nums[l], nums[r] = nums[r], nums[l]
            l += 1
            r -= 1

        self.revertPeriod(nums, 0, k - 1)

        self.revertPeriod(nums, k, len(nums) - 1)

        print(nums)

    def revertPeriod(self, nums, start, end):
        l, r = start, end
        while l < r:
            nums[l], nums[r] = nums[r], nums[l]
            l += 1
            r -= 1


if __name__ == "__main__":
    nums = [1, 2, 3, 4, 5, 6, 7]
    k = 3
    # print(Solution().rotateNSpace(nums, k))
    print(Solution().rotateConstant(nums, k))
    nums = [-1, -100, 3, 99]
    k = 2
    print(Solution().rotateConstant(nums, k))
