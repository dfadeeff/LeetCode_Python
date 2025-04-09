from collections import Counter
from typing import List


class Solution:
    def findRLEArray(self, encoded1: List[List[int]], encoded2: List[List[int]]) -> List[List[int]]:
        array1 = []
        array2 = []

        for _list in encoded1:
            i = 1
            while i <= _list[1]:
                array1.append(_list[0])
                i += 1

        for _list in encoded2:
            i = 1
            while i <= _list[1]:
                array2.append(_list[0])
                i += 1
        print(array1)
        print(array2)
        result = [x * y for x, y in zip(array1, array2)]
        freq = Counter(result)

        final_array = []
        for key, value in freq.items():
            final_array.append([key, value])
        return final_array

    def findRLEArrayOptimal(self, encoded1: List[List[int]], encoded2: List[List[int]]) -> List[List[int]]:
        """
        Compress prodNums into a run-length encoded array
        Run-length” means consecutive identical numbers, not total counts

        Counter counts total, but ignores order and runs.

        """
        res = []
        i = j = 0

        while i < len(encoded1) and j < len(encoded2):
            val1, freq1 = encoded1[i]
            val2, freq2 = encoded2[j]
            product = val1 * val2
            min_freq = min(freq1, freq2)

            print(f"\nProcessing:")
            print(f"  encoded1[{i}]: {encoded1[i]}")
            print(f"  encoded2[{j}]: {encoded2[j]}")
            print(f"  Product: {product} * Frequency: {min_freq}")

            # Merge if last value is same
            if res and res[-1][0] == product:
                res[-1][1] += min_freq
            else:
                res.append([product, min_freq])

            # Decrease frequencies
            encoded1[i][1] -= min_freq
            encoded2[j][1] -= min_freq

            # Move pointers if a segment is consumed
            if encoded1[i][1] == 0:
                i += 1
            if encoded2[j][1] == 0:
                j += 1

        return res


if __name__ == '__main__':
    print("Test1")
    encoded1 = [[1, 3], [2, 1], [3, 2]]
    encoded2 = [[2, 3], [3, 3]]
    # print(Solution().findRLEArray(encoded1, encoded2))
    print(Solution().findRLEArrayOptimal(encoded1, encoded2))
    # print("Test2")
    # encoded1 = [[1, 3], [2, 3]]
    # encoded2 = [[6, 3], [3, 3]]
    # # print(Solution().findRLEArray(encoded1, encoded2))
    # print(Solution().findRLEArrayOptimal(encoded1, encoded2))
    # print("Test3")
    # encoded1 = [[1, 1], [2, 1], [1, 1], [2, 1], [1, 1]]
    # encoded2 = [[1, 1], [2, 1], [1, 1], [2, 1], [1, 1]]
    # # print(Solution().findRLEArray(encoded1, encoded2))
    # print(Solution().findRLEArrayOptimal(encoded1, encoded2))
