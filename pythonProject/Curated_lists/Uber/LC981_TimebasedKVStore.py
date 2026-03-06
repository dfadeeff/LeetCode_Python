from collections import defaultdict


class TimeMap:

    def __init__(self):
        # key → list of (timestamp, value) pairs
        # pairs are automatically sorted because timestamps are strictly increasing
        self.store = defaultdict(list)

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.store[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        values = self.store[key]

        left, right = 0, len(values) - 1
        result = -1
        while left <= right:
            mid = (left + right) // 2
            if values[mid][0] <= timestamp:  # [0] is the timestamp
                result = mid
                left = mid + 1
            else:
                right = mid - 1
        if result == -1:
            return ""
        return values[result][1]  # [1] get value


if __name__ == "__main__":
    timeMap = TimeMap()
    timeMap.set("foo", "bar", 1)
    print(timeMap.get("foo", 1))
    print(timeMap.get("foo", 3))
    timeMap.set("foo", "bar2", 4)
    print(timeMap.get("foo", 4))
    print(timeMap.get("foo", 5))
