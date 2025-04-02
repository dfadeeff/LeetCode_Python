from typing import List


class Solution:
    def missingNumber(self, arr: List[int]) -> int:
        diffarray = []
        for i in range(1, len(arr)):
            diff = abs(arr[i] - arr[i - 1])
            diffarray.append(diff)
        max_element_index = diffarray.index(max(diffarray))
        min_element = min(diffarray)
        if arr[1] < arr[0]:
            min_element = -min_element
        # print(diffarray)
        # print("index of max elemenet", max_element_index)
        # print("min elemenet", min_element)

        return arr[max_element_index] + min_element


if __name__ == "__main__":
    arr = [5, 7, 11, 13]
    print(Solution().missingNumber(arr))
    arr = [15, 13, 12]
    print(Solution().missingNumber(arr))
