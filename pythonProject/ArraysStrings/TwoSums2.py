from typing import List


class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        left = 0
        right = len(numbers) - 1
        answer = []
        while left < right:
            curr = numbers[left] + numbers[right]
            if curr == target:
                answer.append(left + 1)
                answer.append(right + 1)
                break
            elif curr < target:
                left += 1
            else:
                right -= 1
        return answer


if __name__ == '__main__':
    numbers = [2, 7, 11, 15]
    target = 9
    print(Solution().twoSum(numbers, target))
    numbers = [2, 3, 4]
    target = 6
    print(Solution().twoSum(numbers, target))