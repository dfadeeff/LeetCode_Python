# Definition for a Node.
class Node:
    def __init__(self, val=None, next=None):
        self.val = val
        self.next = next


class Solution:
    def insert(self, head: 'Optional[Node]', insertVal: int) -> 'Node':
        if not head:
            new_head = Node(insertVal)
            new_head.next = new_head
            return new_head

        current = head
        while current.next != head:
            if current.val <= insertVal <= current.next.val:
                new_node = Node(insertVal, current.next)
                current.next = new_node
                return head

            elif current.val > current.next.val:
                if insertVal >= current.val or insertVal <= current.next.val:
                    new_node = Node(insertVal, current.next)
                    current.next = new_node
                    return head

            current = current.next

        # Case 4
        new_node = Node(insertVal, current.next)
        current.next = new_node
        return head


if __name__ == '__main__':
    head = Node(3)
    head.next = Node(4)
    head.next.next = Node(1)
    head.next.next.next = head
    insertVal = 2
    print(Solution().insert(head, 1))
