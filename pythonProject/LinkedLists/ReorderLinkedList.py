from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:
        """
        Do not return anything, modify head in-place instead.
        """
        # 1. Find the middle:
        #   Use slow / fast pointers:
        #   Fast moves 2 steps, slow moves 1 step.
        #   When fast reaches the end, slow is at the middle.

        # 2. Reverse the second half
        # Standard in-place reversal.

        # 3. Merge:
        # Alternate nodes from first and reversed second half.

        if not head or not head.next:
            return

        # Step 1: Find the middle
        slow, fast = head, head.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        # Step 2: Reverse second half
        second = slow.next
        prev = None
        while second:
            tmp = second.next
            second.next = prev
            prev = second
            second = tmp
        slow.next = None  # Cut the list

        # Step 3: Merge two halves
        first, second = head, prev
        while second:
            tmp1, tmp2 = first.next, second.next
            first.next = second
            second.next = tmp1
            first, second = tmp1, tmp2


# Helper function to print list
def print_list(head):
    current = head
    while current:
        print(current.val, end=" -> " if current.next else "\n")
        current = current.next


if __name__ == "__main__":
    head = ListNode(1)
    head.next = ListNode(2)
    head.next.next = ListNode(3)
    head.next.next.next = ListNode(4)

    print("Before reorder:")
    print_list(head)

    Solution().reorderList(head)

    print("After reorder:")
    print_list(head)
