from typing import List


class Solution:
    def answerQueries(self, nums: List[int], queries: List[int]) -> List[int]:

        # Step 1: Sort the nums array
        nums.sort()

        # Step 2: Compute prefix sums
        prefix_sums = [0]
        for num in nums:
            prefix_sums.append(prefix_sums[-1] + num)

        def binary_search(target):
            left, right = 0, len(prefix_sums) - 1
            while left <= right:
                mid = (left + right) // 2
                if prefix_sums[mid] <= target:
                    left = mid + 1  # Move right to find a larger valid subsequence
                else:
                    right = mid - 1  # Move left to stay within the target limit
            return right  # 'right' is the max index where sum <= target

        answer = []
        for query in queries:
            max_length = binary_search(query)
            answer.append(max_length)
        return answer


def main():
    nums = [4, 5, 2, 1]
    queries = [3, 10, 21]
    print(Solution().answerQueries(nums, queries))
    nums = [2, 3, 4, 5]
    queries = [1]
    print(Solution().answerQueries(nums, queries))


if __name__ == '__main__':
    main()
