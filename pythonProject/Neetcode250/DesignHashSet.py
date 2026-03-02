class MyHashSet:

    def __init__(self):
        self.size = 1000
        self.buckets = [[] for _ in range(self.size)]

    def _hash(self, key):
        return key % self.size

    def add(self, key: int) -> None:
        bucket = self.buckets[self._hash(key)]
        if key not in bucket:
            bucket.append(key)

    def remove(self, key: int) -> None:
        bucket = self.buckets[self._hash(key)]
        if key in bucket:
            bucket.remove(key)

    def contains(self, key: int) -> bool:
        bucket = self.buckets[self._hash(key)]
        return key in bucket

if __name__ == "__main__":
    obj = MyHashSet()
    obj.add(1)
    obj.add(2)
    print(obj.contains(1))   # True
    print(obj.contains(3))   # False
    obj.add(2)               # already exists, skip
    print(obj.contains(2))   # True
    obj.remove(2)
    print(obj.contains(2))   # False