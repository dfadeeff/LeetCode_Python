import heapq
from collections import defaultdict
from typing import List


class Solution:
    def kSmallestPairsBruteForce(self, nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
        dic = defaultdict(list)
        pairs = []
        for i in range(0, len(nums1)):
            for j in range(0, len(nums2)):
                sum = nums1[i] + nums2[j]
                dic[sum].append([nums1[i], nums2[j]])
        sorted_sums = sorted(dic.keys())
        for s in sorted_sums:
            for pair in dic[s]:
                pairs.append(pair)
                if len(pairs) >= k:
                    return pairs


        return pairs

    def kSmallestPairs(self, nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:

        if not nums1 or not nums2 or k == 0:
            return []

        heap = []
        result = []

        print("🌱 Step 1: Pushing initial pairs (nums1[i] + nums2[0]) into heap")
        for i in range(min(k, len(nums1))):
            pair_sum = nums1[i] + nums2[0]
            heapq.heappush(heap, (pair_sum, i, 0))  # (sum, index in nums1, index in nums2)
            print(f"Pushed: ({nums1[i]} + {nums2[0]} = {pair_sum})")

        print("\n🌪 Step 2: Extracting k smallest pairs from heap")
        while heap and len(result) < k:
            curr_sum, i, j = heapq.heappop(heap)
            pair = [nums1[i], nums2[j]]
            result.append(pair)
            print(f"🧩 Popped: {pair} with sum = {curr_sum}")

            if j + 1 < len(nums2):
                new_sum = nums1[i] + nums2[j + 1]
                heapq.heappush(heap, (new_sum, i, j + 1))
                print(f"🔁 Added next pair from same row: ({nums1[i]} + {nums2[j + 1]} = {new_sum})")

        print("\n✅ Final Result:", result)
        return result


if __name__ == '__main__':
    nums1 = [1, 7, 11]
    nums2 = [2, 4, 6]
    k = 3
    print(Solution().kSmallestPairsBruteForce(nums1, nums2, k))
