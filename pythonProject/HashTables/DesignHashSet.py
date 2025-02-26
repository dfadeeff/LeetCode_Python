class MyHashSet:
    def __init__(self):
        self.size = 1000  # Number of buckets
        self.buckets = [[] for _ in range(self.size)]  # Array of lists

    def _hash(self, key: int) -> int:
        """Hash function: returns index for a given key."""
        return key % self.size

    def add(self, key: int) -> None:
        """Inserts the value key into the HashSet."""
        index = self._hash(key)
        if key not in self.buckets[index]:  # Avoid duplicates
            self.buckets[index].append(key)

    def remove(self, key: int) -> None:
        """Removes the key if it exists."""
        index = self._hash(key)
        if key in self.buckets[index]:  # If key exists, remove it
            self.buckets[index].remove(key)

    def contains(self, key: int) -> bool:
        """Returns whether the value key exists in the HashSet."""
        index = self._hash(key)
        return key in self.buckets[index]  # Check if key exists


if __name__ == '__main__':
    myHashSet = MyHashSet();
    myHashSet.add(1);  # set = [1]
    myHashSet.add(2);  # set = [1, 2]
    myHashSet.contains(1);  # return True
    myHashSet.contains(3);  # return False, (not found)
    myHashSet.add(2);  # set = [1, 2]
    myHashSet.contains(2);  # return True
    myHashSet.remove(2);  # set = [1]
    myHashSet.contains(2);  # return False, (already removed)
