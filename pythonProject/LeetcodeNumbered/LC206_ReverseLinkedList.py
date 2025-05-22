from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        curr = head
        prev = None

        while curr:
            # this line is genius, curr.next = prev, then shift to the right, prev, curr = curr, curr.next
            curr.next, prev, curr = prev, curr, curr.next

        return prev


def print_list(head: Optional[ListNode]) -> None:
    """Pretty‑prints a singly linked list as  val1 -> val2 -> …"""
    vals = []
    curr = head
    while curr:
        vals.append(str(curr.val))
        curr = curr.next
    print(" -> ".join(vals))


if __name__ == "__main__":
    head = ListNode(1)
    head.next = ListNode(2)
    head.next.next = ListNode(3)
    head.next.next.next = ListNode(4)
    head.next.next.next.next = ListNode(5)
    modified = Solution().reverseList(head)
    print_list(modified)
