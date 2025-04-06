class ListNode:
    def __init__(self, key, value):
        self.key, self.value = key, value
        self.prev, self.next = None, None


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # key -> node

        # Dummy head and tail nodes
        self.head = ListNode(0, 0)  # LRU
        self.tail = ListNode(0, 0)  # Most recent
        self.head.next = self.tail
        self.tail.prev = self.head

    def add(self, node):
        # Add node before tail (MRU position)
        prev = self.tail.prev
        prev.next = node
        node.prev = prev
        node.next = self.tail
        self.tail.prev = node

    def remove(self, node):
        # Remove node from linked list
        prev = node.prev
        nxt = node.next
        prev.next = nxt
        nxt.prev = prev

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self.remove(node)
        self.add(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.remove(self.cache[key])
        node = ListNode(key, value)
        self.cache[key] = node
        self.add(node)

        if len(self.cache) > self.capacity:
            # Remove from the head (LRU position)
            lru = self.head.next
            self.remove(lru)
            del self.cache[lru.key]


if __name__ == '__main__':
    lRUCache = LRUCache(2)
    print(lRUCache.put(1, 1))  # cache is {1=1}
    print(lRUCache.put(2, 2))  # cache is {1=1, 2=2}
    print(lRUCache.get(1))  # returns 1
    print(lRUCache.put(3, 3))  # evicts key 2, cache is {1=1, 3=3}
    print(lRUCache.get(2))  # returns -1 (not found)
    print(lRUCache.put(4, 4))  # evicts key 1, cache is {4=4, 3=3}
    print(lRUCache.get(1))  # returns -1 (not found)
    print(lRUCache.get(3))  # returns 3
    print(lRUCache.get(4))  # returns 4
