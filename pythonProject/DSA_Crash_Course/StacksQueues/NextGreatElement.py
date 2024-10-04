def nextGreaterElement( nums1: list[int], nums2: list[int]) -> list[int]:
    stack = []
    hashmap = {}

    for num in nums2:
        while stack and num > stack[-1]:
            hashmap[stack.pop()] = num
        stack.append(num)

    while stack:
        hashmap[stack.pop()] = -1

    return [hashmap.get(i, -1) for i in nums1]


if __name__ == '__main__':
    nums1 = [4, 1, 2]
    nums2 = [1, 3, 4, 2]
    print(nextGreaterElement(nums1, nums2))

