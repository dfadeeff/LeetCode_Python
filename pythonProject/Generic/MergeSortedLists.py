from typing import List, Optional


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode()
        tail = dummy

        while list1 and list2:
            if list1.val < list2.val:
                tail.next = list1
                list1 = list1.next
            else:
                tail.next = list2
                list2 = list2.next
            tail = tail.next
        if list1:
            tail.next = list1
        if list2:
            tail.next = list2
        return dummy.next


def print_list(head: Optional[ListNode]) -> None:
    """Pretty‑prints a singly linked list as  val1 -> val2 -> …"""
    vals = []
    curr = head
    while curr:
        vals.append(str(curr.val))
        curr = curr.next
    print(" -> ".join(vals))


if __name__ == "__main__":
    head1 = ListNode(1)
    head1.next = ListNode(2)
    head1.next.next = ListNode(4)
    head2 = ListNode(1)
    head2.next = ListNode(3)
    head2.next.next = ListNode(4)
    new_list = Solution().mergeTwoLists(head1, head2)
    print_list(new_list)
