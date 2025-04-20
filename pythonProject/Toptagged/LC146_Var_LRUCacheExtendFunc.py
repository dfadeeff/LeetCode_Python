class ListNode:
    def __init__(self, key, value):
        self.key, self.value = key, value
        self.prev, self.next = None, None


class LRUCache:
    def __init__(self):
        self.dic = {}  # key -> node
        self.head = ListNode(-1, -1)
        self.tail = ListNode(-1, -1)
        self.head.next = self.tail
        self.tail.prev = self.head

    def remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def add(self, node):
        prev_end = self.tail.prev
        prev_end.next = node
        node.prev = prev_end
        node.next = self.tail
        self.tail.prev = node

    def put(self, key: int, value: int) -> None:
        if key in self.dic:
            self.remove(self.dic[key])
        node = ListNode(key, value)
        self.dic[key] = node
        self.add(node)

    def get(self, key: int) -> int:
        if key not in self.dic:
            return -1
        node = self.dic[key]
        self.remove(node)
        self.add(node)
        return node.value

    def delete(self, key: int) -> bool:
        if key not in self.dic:
            return False
        node = self.dic[key]
        self.remove(node)
        del self.dic[key]
        return True

    def last(self) -> int:
        if self.head.next == self.tail:
            return -1
        return self.tail.prev.value


# Example test
if __name__ == "__main__":
    lru = LRUCache()
    lru.put(4, 4)
    lru.put(5, 5)
    lru.put(3, 30)
    print(lru.last())       # 30
    print(lru.delete(5))    # True
    print(lru.delete(4))    # True
    print(lru.delete(1))    # False
    print(lru.last())       # 30