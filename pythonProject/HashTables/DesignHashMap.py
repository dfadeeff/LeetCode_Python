class MyHashMap:
    def __init__(self):
        self.size = 1000  # Number of buckets
        self.buckets = [[] for _ in range(self.size)]  # Array of lists (chaining)

    def _hash(self, key: int) -> int:
        """Hash function: returns index for a given key."""
        return key % self.size

    def put(self, key: int, value: int) -> None:
        """Insert (key, value) into HashMap. Update if key exists."""
        index = self._hash(key)
        for i, (k, v) in enumerate(self.buckets[index]):  # Search for key
            if k == key:
                self.buckets[index][i] = (key, value)  # Update value
                return
        self.buckets[index].append((key, value))  # Add new key-value pair

    def get(self, key: int) -> int:
        """Return value associated with key, or -1 if not found."""
        index = self._hash(key)
        for k, v in self.buckets[index]:
            if k == key:
                return v
        return -1  # Key not found

    def remove(self, key: int) -> None:
        """Remove key-value pair from HashMap if it exists."""
        index = self._hash(key)
        self.buckets[index] = [(k, v) for k, v in self.buckets[index] if k != key]


if __name__ == '__main__':
    myHashMap = MyHashMap();
    myHashMap.put(1, 1);  # Themap is now[[1, 1]]
    myHashMap.put(2, 2);  # The map is now[[1, 1], [2, 2]]
    myHashMap.get(1);  # return 1, The map is now[[1, 1], [2, 2]]
    myHashMap.get(3);  # return -1(i.e., not found), The map is now[[1, 1], [2, 2]]
    myHashMap.put(2, 1);  # The map is now[[1, 1], [2, 1]](i.e., update the existing value)
    myHashMap.get(2);  # return 1, The map is now[[1, 1], [2, 1]]
    myHashMap.remove(2);  # remove the mappin for 2, The map is now[[1, 1]]
    myHashMap.get(2);  # return -1(i.e., not found), The map is now[[1, 1]]
