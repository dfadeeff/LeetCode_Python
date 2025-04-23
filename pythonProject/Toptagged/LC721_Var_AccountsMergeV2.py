from typing import List
from collections import defaultdict


class Solution:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        def dfs_variant_721(adjs, email_to_id, visited, curr_email, id):
            visited.add(curr_email)
            email_to_id[curr_email] = id
            for adj in adjs.get(curr_email, []):
                if adj not in visited:
                    dfs_variant_721(adjs, email_to_id, visited, adj, id)

        # Create adjacency list
        adjs = {}
        for id, emails in accounts.items():
            first_email = emails[0]
            for email in emails[1:]:
                if first_email not in adjs:
                    adjs[first_email] = []
                if email not in adjs:
                    adjs[email] = []
                adjs[first_email].append(email)
                adjs[email].append(first_email)

        # Helper structures
        email_to_id = {}
        visited = set()
        result = {}

        # Perform DFS and group by connected components
        for id, emails in accounts.items():
            first_email = emails[0]
            if first_email in visited:
                same_id = email_to_id[first_email]
                if same_id not in result:
                    result[same_id] = []
                result[same_id].append(id)
            else:
                result[id] = []
                dfs_variant_721(adjs, email_to_id, visited, first_email, id)

        # Prepare result as a list of lists
        result_v2 = []
        for id, same_ids in result.items():
            same = [id] + same_ids
            result_v2.append(same)

        return result_v2


if __name__ == "__main__":
    accounts = {
        "C1": ["a", "b"],
        "C2": ["c"],
        "C3": ["b", "d"],
        "C4": ["d"],
        "C5": ["e"],
        "C6": ["c"],
        "C7": ["a"]
    }
    print(Solution().accountsMerge(accounts))
    accounts = {
        "ID1": ["aa@gmail.com", "bb@gmail.com"],
        "ID2": ["cc@gmail.com"],
        "ID3": ["bb@gmail.com", "dd@gmail.com"],
        "ID4": ["dd@gmail.com"],
        "ID5": ["ee@gmail.com"],
        "ID6": ["cc@gmail.com"],
        "ID7": ["aa@gmail.com"]
    }
    print(Solution().accountsMerge(accounts))
