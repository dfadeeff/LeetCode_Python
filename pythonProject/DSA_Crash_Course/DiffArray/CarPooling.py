from typing import List


class Solution:
    def carPooling(self, trips: List[List[int]], capacity: int) -> bool:
        arr = [0] * (max(trip[2] for trip in trips) + 1)
        for (value, left, right) in trips:
            arr[left] += value
            arr[right] -= value

        print("constructed array: ", arr)
        curr = 0
        for i in range(len(arr)):
            curr += arr[i]
            if curr > capacity:
                return False
        return True


def main():
    trips = [[2, 1, 5], [3, 3, 7]]
    capacity = 4
    print(Solution().carPooling(trips, capacity))
    trips = [[2, 1, 5], [3, 3, 7]]
    capacity = 5
    print(Solution().carPooling(trips, capacity))


if __name__ == '__main__':
    main()
