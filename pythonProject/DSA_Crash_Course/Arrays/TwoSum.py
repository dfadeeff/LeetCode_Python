def twoSum(nums, target):
    left = 0
    right = len(nums) - 1

    while left < right:
        if nums[left] + nums[right] == target:
            return True
        elif nums[left] + nums[right] < target:
            left += 1
        elif nums[left] + nums[right] > target:
            right -= 1
    return False


if __name__ == '__main__':
    nums1 = [1, 2, 4, 6, 8, 9, 14, 15]
    target1 = 13
    print(twoSum(nums1, target1))
