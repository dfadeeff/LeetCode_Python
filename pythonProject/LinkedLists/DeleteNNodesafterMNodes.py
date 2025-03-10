# Definition for singly-linked list.
from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def deleteNodes(self, head: Optional[ListNode], m: int, n: int) -> Optional[ListNode]:
        curr = head
        while curr:
            # Step 1: Keep m nodes
            for _ in range(1, m):
                if not curr:
                    return head
                curr = curr.next

            # If we reach end while keeping
            if not curr:
                break

            # Step 2: Skip n nodes
            temp = curr.next
            for _ in range(n):
                if not temp:
                    break
                temp = temp.next
            # Step 3: Connect current node to the rest
            curr.next = temp
            curr = temp

        return head


if __name__ == '__main__':
    head = ListNode(1)
    head.next = ListNode(2)
    head.next.next = ListNode(3)
    head.next.next.next = ListNode(4)
    head.next.next.next.next = ListNode(5)
    head.next.next.next.next.next = ListNode(6)
    head.next.next.next.next.next.next = ListNode(7)
    head.next.next.next.next.next.next.next = ListNode(8)
    head.next.next.next.next.next.next.next.next = ListNode(9)
    head.next.next.next.next.next.next.next.next.next = ListNode(10)
    head.next.next.next.next.next.next.next.next.next.next = ListNode(11)
    head.next.next.next.next.next.next.next.next.next.next.next = ListNode(12)
    head.next.next.next.next.next.next.next.next.next.next.next.next = ListNode(13)

    m = 2
    n = 3
    result = Solution().deleteNodes(head, m, n)

    # Print the modified linked list
    curr = result
    while curr:
        print(curr.val, end=" -> ")
        curr = curr.next
    print("None")
