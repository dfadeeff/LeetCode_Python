from typing import List


class Solution:
    def splitArray(self, nums: List[int], k: int) -> int:
        minResult, maxResult = 0, 0
        # minResult = max(nums)
        for num in nums:
            maxResult += num
            if num > minResult:
                minResult = num

        finalResult = float('inf')
        while minResult <= maxResult:
            # Start by checking if the value in the middle of the search space satisfies this desired outcome
            # If it does, we can discard all values to the right of this in our search space since we have
            # something better than those already. We only need to search values to the left to see if
            # we can find something better
            # If not, we only need to search values higher than mid

            mid = (minResult + maxResult) // 2
            if self.isPossible(mid, nums, k):
                finalResult = mid
                maxResult = mid - 1

            else:
                minResult = mid + 1

        return finalResult

    def isPossible(self, x, nums, m) -> bool:
        numSubarrays = 1
        subarraySum = 0

        for num in nums:
            # Greedily try to add this element to the current subarray as long as the subarray's sum doesn't exceed our upper limit x
            if (num + subarraySum) <= x:
                subarraySum += num
            # If sum would be exceeded by adding the current element, we need to start a new subarray and put this element into that
            else:
                numSubarrays += 1
                subarraySum = num

        return numSubarrays <= m


def main():
    nums = [7, 2, 5, 10, 8]
    k = 2
    print(Solution().splitArray(nums, k))
    nums = [1, 2, 3, 4, 5]
    k = 2
    print(Solution().splitArray(nums, k))


if __name__ == '__main__':
    main()
