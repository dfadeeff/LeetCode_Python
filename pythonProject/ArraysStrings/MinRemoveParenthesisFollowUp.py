class Solution:
    def minRemoveToMakeValidStack(self, s: str) -> str:
        stack = []
        indexes_to_remove = set()
        print("Initial string:", s)
        # Step 1: Identify invalid parentheses
        for i, c in enumerate(s):
            if c == '(':
                stack.append(i)
                print(f"Found '(': push index {i}, stack: {stack}")
            elif c == ')':
                if stack:
                    matched_index = stack.pop()
                    print(f"Found ')': matched with '(', pop index {matched_index}, stack: {stack}")
                else:
                    indexes_to_remove.add(i)
                    print(
                        f"Found unmatched ')', mark index {i} for removal, indexes_to_remove: {indexes_to_remove}")

        # Step 2: Add remaining unmatched '('
        print(f"Unmatched '(': {stack}, adding to indexes_to_remove")
        """
        equivalent to:
        
        for element in stack:
            indexes_to_remove.add(element)
        Add remaining elements in stack to the list of indices to be removed.
        """
        indexes_to_remove.update(stack)

        # Step 3: Build result string
        result = []
        for i, c in enumerate(s):
            if i not in indexes_to_remove:
                result.append(c)
            else:
                print(f"Skipping character '{c}' at index {i} (marked for removal)")

        final_result = ''.join(result)
        print("Final cleaned string:", final_result)
        return final_result


if __name__ == '__main__':
    s = "lee(t(c)o)de)"  # last unmatched parenthesis at index 12
    print(Solution().minRemoveToMakeValidStack(s))
