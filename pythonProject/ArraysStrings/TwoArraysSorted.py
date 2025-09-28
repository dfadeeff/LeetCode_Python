class Solution:
    def combineTwoSorted(self, arr1, arr2):
        i, j = 0, 0
        ans = []

        while i < len(arr1) and j < len(arr2):
            if arr1[i] < arr2[j]:
                ans.append(arr1[i])
                i += 1
            else:
                ans.append(arr2[j])
                j += 1

        while i < len(arr1):
            ans.append(arr1[i])
            i += 1
        while j < len(arr2):
            ans.append(arr2[j])
            j += 1

        return ans


if __name__ == "__main__":
    arr1 = [1, 4, 7, 20]
    arr2 = [3, 5, 6]
    print(Solution().combineTwoSorted(arr1, arr2))
