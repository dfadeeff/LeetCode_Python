from typing import List


class Solution:
    def maximumUnits(self, boxTypes: List[List[int]], truckSize: int) -> int:
        total_units = 0
        sorted_boxTypes = sorted(boxTypes, key=lambda x: x[1], reverse=True)

        for i in range(len(sorted_boxTypes)):
            # Check if the truck can take all boxes of this type
            if truckSize >= sorted_boxTypes[i][0]:
                total_units += sorted_boxTypes[i][0] * sorted_boxTypes[i][1]
                truckSize -= sorted_boxTypes[i][0]
            else:
                # Take only the remaining capacity worth of boxes
                total_units += truckSize * sorted_boxTypes[i][1]
                break  # Truck is full after this

        return total_units


def main():
    boxTypes = [[1, 3], [2, 2], [3, 1]]
    truckSize = 4
    print(Solution().maximumUnits(boxTypes, truckSize))
    boxTypes = [[5, 10], [2, 5], [4, 7], [3, 9]]
    truckSize = 10
    print(Solution().maximumUnits(boxTypes, truckSize))


if __name__ == '__main__':
    main()
