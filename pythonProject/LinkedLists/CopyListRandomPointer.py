# Definition for a Node.
class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random


class Solution:
    def copyRandomList(self, head: 'Optional[Node]') -> 'Optional[Node]':
        """
        Approach: Hash Map (node → copy of node)

        We need to preserve random pointers, but we can’t do that while creating nodes on first pass because random pointers might point to nodes that haven’t been created yet!

        First pass:
        For every original node:
            Create a copy of the node (without setting next/random yet).
            Store: old_node → new_node in a hash map.

        Second pass:
        For every original node:
            copy.next = mapping[original.next]
            copy.random = mapping[original.random]

        Return the head of the copied list!

        O(n) time complexity
        O(n) space complexity

        :param head:
        :return:
        """

        if not head:
            return None
        # Step 1: Create mapping from old node to new node
        old_to_new = {}
        current = head
        while current:
            copy = Node(current.val)
            old_to_new[current] = copy
            current = current.next

        # Step 2: Assign next and random pointers
        current = head
        while current:
            copy = old_to_new[current]
            copy.next = old_to_new.get(current.next)
            copy.random = old_to_new.get(current.random)
            current = current.next
        return old_to_new[head]

    def copyRandomListSpaceOptimised(self, head: 'Optional[Node]') -> 'Optional[Node]':
        """
        O(n) time complexity
        O(1) space complexity

        I interleave the cloned nodes within the original list.
        This allows me to assign random pointers in O(1) space, because the cloned node is always next to its original.
        After setting up the random pointers, I separate the cloned list from the original list.



        """
        if not head:
            return None
        # Step 1: Clone and interleave nodes
        current = head
        while current:
            clone = Node(current.val)
            clone.next = current.next
            current.next = clone
            current = clone.next
        # Step 2: Set random pointers for cloned nodes
        current = head
        while current:
            if current.random:
                current.next.random = current.random.next
            current = current.next.next  # Move to next original node

        # Step 3: Detach the cloned list from the original list
        original = head
        clone_head = head.next
        while original:
            clone = original.next
            original.next = clone.next
            if clone.next:
                clone.next = clone.next.next
            original = original.next
        return clone_head


def print_list(node):
    nodes = []
    idx_map = {}

    # Assign indices for printing
    idx = 0
    current = node
    while current:
        idx_map[current] = idx
        nodes.append(current)
        idx += 1
        current = current.next

    for node in nodes:
        random_idx = idx_map.get(node.random, None)
        print(f"Node idx: {idx_map[node]}, Val: {node.val}, Random idx: {random_idx}, Memory id: {id(node)}")


def build_linked_list(arr):
    if not arr:
        return None

    # Step 1: Create all nodes
    nodes = [Node(x=val) for val, _ in arr]

    # Step 2: Link next pointers
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]

    # Step 3: Link random pointers
    for i, (_, random_index) in enumerate(arr):
        if random_index is not None:
            nodes[i].random = nodes[random_index]

    return nodes[0]  # Return head node


if __name__ == '__main__':
    head_input = [[7, None], [13, 0], [11, 4], [10, 2], [1, 0]]
    head = build_linked_list(head_input)

    print("Original List:")
    print_list(head)

    # Run O(1) space solution (you can also switch to hashmap if you want)
    solution = Solution()
    # cloned_head = solution.copyRandomListSpaceOptimised(head)
    cloned_head = solution.copyRandomList(head)

    print("\nCloned List:")
    print_list(cloned_head)
