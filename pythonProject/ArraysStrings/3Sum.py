from typing import List


class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()  # Step 1: Sort input array
        result = []

        for i in range(len(nums) - 2):
            if i > 0 and nums[i] == nums[i - 1]:  # Step 2: Skip duplicates for `i`
                continue

            left, right = i + 1, len(nums) - 1

            while left < right:
                curr_sum = nums[i] + nums[left] + nums[right]

                if curr_sum == 0:
                    result.append([nums[i], nums[left], nums[right]])

                    # Step 3: Skip duplicates for `left` and `right`
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1

                    # Move both pointers after storing a valid triplet
                    left += 1
                    right -= 1

                elif curr_sum < 0:
                    left += 1  # Increase sum
                else:
                    right -= 1  # Decrease sum

        return result


if __name__ == '__main__':
    nums = [-1, 0, 1, 2, -1, -4]
    print(Solution().threeSum(nums))
