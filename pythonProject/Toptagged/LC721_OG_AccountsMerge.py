from typing import List
from collections import defaultdict


class Solution:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        graph = defaultdict(list)
        email_to_name = {}
        # Step 1: Build graph and map email to name
        for account in accounts:
            name = account[0]
            first_email = account[1]
            for email in account[1:]:
                graph[first_email].append(email)
                graph[email].append(first_email)
                email_to_name[email] = name
        visited = set()
        result = []

        # Step 2: DFS function to collect connected emails
        def dfs(email, component):
            for neighbor in graph[email]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    component.append(neighbor)
                    dfs(neighbor, component)

        # Step 3: Traverse all emails
        for email in graph:
            if email not in visited:
                visited.add(email)
                component = [email]
                dfs(email, component)
                result.append([email_to_name[email]] + sorted(component))

        return result


if __name__ == "__main__":
    accounts = [["John", "johnsmith@mail.com", "john_newyork@mail.com"],
                ["John", "johnsmith@mail.com", "john00@mail.com"], ["Mary", "mary@mail.com"],
                ["John", "johnnybravo@mail.com"]]
    print(Solution().accountsMerge(accounts))
