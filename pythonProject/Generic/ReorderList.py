from typing import Optional


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:
        """
        Do not return anything, modify head in-place instead.
        """
        # find the middle
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        # reverse
        prev, curr = None, slow
        while curr:
            # this line is genius, curr.next = prev, then shift to the right, prev, curr = curr, curr.next
            curr.next, prev, curr = prev, curr, curr.next

        # merge
        first, second = head, prev
        while second.next:
            first.next, first = second, first.next
            second.next, second = first, second.next



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
    modified = Solution().reorderList(head)
    print_list(head)
