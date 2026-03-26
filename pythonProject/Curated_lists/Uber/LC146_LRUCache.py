class Node:
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None


class LRUCache:
    """
    Design a cache with capacity k

    get(key)         → return value if exists, else -1
    put(key, value)  → insert/update
                       if at capacity → evict LEAST RECENTLY USED

    LRU = the key that was accessed longest ago


    capacity = 2

    put(1,1)   cache: {1:1}
    put(2,2)   cache: {1:1, 2:2}
    get(1)     cache: {2:2, 1:1}   ← 1 now most recent
    put(3,3)   capacity full → evict LRU = 2
               cache: {1:1, 3:3}
    get(2)     → -1  (evicted)

    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.map = {}  # key → node

        # dummy head and tail
        self.head = Node()  # MRU side
        self.tail = Node()  # LRU side
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        """Remove node from list"""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_head(self, node):
        """Add node right after head (= MRU position)"""
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key not in self.map:
            return -1
        node = self.map[key]
        self._remove(node)  # remove from current position
        self._add_to_head(node)  # move to MRU
        return node.val

    def put(self, key: int, value: int) -> None:
        if key in self.map:
            node = self.map[key]
            node.val = value
            self._remove(node)
            self._add_to_head(node)
        else:
            node = Node(key, value)
            self.map[key] = node
            self._add_to_head(node)

            if len(self.map) > self.capacity:
                # evict LRU = node before tail
                lru = self.tail.prev
                self._remove(lru)
                del self.map[lru.key]  # ← need key in node for this


if __name__ == "__main__":
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    print(cache.get(1))  # 1
    cache.put(3, 3)  # evicts 2
    print(cache.get(2))  # -1
    cache.put(4, 4)  # evicts 1
    print(cache.get(1))  # -1
    print(cache.get(3))  # 3
    print(cache.get(4))  # 4
