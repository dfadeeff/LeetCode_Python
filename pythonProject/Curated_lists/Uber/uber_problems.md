# Uber LeetCode — Pattern Guide (42 problems)

## 1. DFS on Grid (4) — "flood fill thinking"
**Pattern**: scan grid → when you find target → DFS/BFS to explore all connected cells

| # | Problem | Diff | How to think |
|---|---------|------|-------------|
| 200 | Number of Islands | Med | Scan grid. Found '1'? Count +1, DFS to sink all connected land. |
| 79 | Word Search | Med | DFS + backtracking. From each cell, try to match word char by char. Mark visited, unmark on backtrack. |
| 827 | Making A Large Island | Hard | Step 1: DFS to label each island with ID + size. Step 2: for each '0', check its 4 neighbors' island IDs, sum unique sizes +1. |
| 934 | Shortest Bridge | Med | DFS to find first island and mark it. BFS outward from that island layer by layer until you hit the second island. Layers = distance. |

**Key insight**: DFS to explore/mark, BFS when you need shortest distance.

---

## 2. BFS — Shortest Path (5) — "level-by-level thinking"
**Pattern**: state space search. Each "state" is a node. BFS guarantees shortest path.

| # | Problem | Diff | How to think |
|---|---------|------|-------------|
| 127 | Word Ladder | Hard | Each word = node. Two words connected if differ by 1 char. BFS from beginWord to endWord. Trick: generate neighbors by trying a-z at each position. |
| 752 | Open the Lock | Med | Each 4-digit combo = node. 8 neighbors (each digit ±1). BFS from "0000" to target. Skip deadends (put in visited set before starting). |
| 815 | Bus Routes | Hard | DON'T model stops as nodes with bus edges — too slow. Model ROUTES as nodes. Two routes connected if they share a stop. BFS on routes. |
| 864 | Shortest Path to Get All Keys | Hard | State = (row, col, keys_bitmask). BFS on states. Pick up key → set bit. Need all bits set = done. |
| 3629 | Min Jumps via Prime Teleportation | Med | BFS where nodes are positions. Edges: adjacent positions + teleport to positions sharing a prime factor. Precompute prime factors. |

**Key insight**: define what a "state" is. BFS = shortest path in unweighted graph.

---

## 3. Topological Sort (2) — "ordering with dependencies"
**Pattern**: directed graph + need ordering → topological sort (BFS with indegree / DFS with cycle detection)

| # | Problem | Diff | How to think |
|---|---------|------|-------------|
| 207 | Course Schedule | Med | Build directed graph. Detect cycle = impossible. BFS: start from indegree=0 nodes, reduce neighbors' indegree, repeat. If processed all nodes → no cycle. |
| 269 | Alien Dictionary | Hard | Compare adjacent words to extract ordering rules (first different char → edge). Build graph → topological sort. Edge case: "abc" before "ab" = invalid. |

---

## 4. Union Find (3) — "dynamic connectivity"
**Pattern**: elements being grouped over time. Need to know: are X and Y connected? How many groups?

| # | Problem | Diff | How to think |
|---|---------|------|-------------|
| 305 | Number of Islands II | Hard | Grid starts as water. Add land one by one. Each new land = new island. Check 4 neighbors — if neighbor is land, union them (island count decreases). |
| 1101 | Earliest Moment Everyone Friends | Med | Sort events by time. Union people. After each union, check if one component remains → return that time. |
| 2092 | Find All People With Secret | Hard | Sort meetings by time. Process all meetings at same time together: union participants. After each time step, anyone NOT connected to person 0 → reset them. |

**Key insight**: use Union Find when groups merge over time. Need `find()` with path compression + `union()` with rank.

---

## 5. Tree (4)
| # | Problem | Diff | Pattern | How to think |
|---|---------|------|---------|-------------|
| 230 | Kth Smallest in BST | Med | Inorder traversal | BST inorder = sorted. Do inorder, count to k, return. |
| 545 | Boundary of Binary Tree | Med | DFS | Three parts: left boundary (go left-first, skip leaves) + all leaves (DFS) + right boundary (go right-first, reverse). |
| 2791 | Palindrome Paths in Tree | Hard | Bitmask + DFS | Path is palindrome if at most 1 char has odd count. Use XOR bitmask. DFS from root, count prefix XOR values. Two paths form palindrome if XOR differs by 0 or 1 bit. |
| 2858 | Min Edge Reversals | Hard | Rerooting | DFS from node 0 to get answer for root. Then DFS again: when moving to child, if edge was forward → +1 reversal, if backward → -1 reversal. |

---

## 6. Binary Search (3) — "search space thinking"
**Pattern**: answer has monotonic property → binary search on the answer

| # | Problem | Diff | How to think |
|---|---------|------|-------------|
| 162 | Find Peak Element | Med | Classic binary search. If nums[mid] < nums[mid+1] → peak is to the right. Else → peak is to the left (or at mid). |
| 410 | Split Array Largest Sum | Hard | Binary search on answer! Search range: [max(nums), sum(nums)]. For each guess, greedily check: can we split into ≤k subarrays all ≤ guess? |
| 1428 | Leftmost Column with a One | Med | Binary search per row (sorted rows). Or smarter: start top-right, go left on '1', go down on '0'. |

**Key insight**: "minimize the maximum" or "maximize the minimum" → binary search on answer.

---

## 7. Sliding Window / Two Pointers (2)
| # | Problem | Diff | How to think |
|---|---------|------|-------------|
| 977 | Squares of Sorted Array | Easy | Two pointers at both ends. Compare abs values. Larger one goes to result (fill from the end). |
| 1438 | Longest Subarray Abs Diff ≤ Limit | Med | Sliding window. Need to track min AND max in window. Use two monotonic deques: one for max (decreasing), one for min (increasing). Shrink window when max-min > limit. |

---

## 8. Stack (2)
| # | Problem | Diff | How to think |
|---|---------|------|-------------|
| 227 | Basic Calculator II | Med | Stack for numbers. Scan left to right, track previous operator. On * or / → pop and compute immediately. On + or - → push (+ or negative). Sum stack at end. |
| 1475 | Final Prices with Discount | Easy | Monotonic stack. For each price, find next smaller or equal price to the right. That's the discount. Classic "next smaller element" pattern. |

---

## 9. Heap / Priority Queue (4)
| # | Problem | Diff | How to think |
|---|---------|------|-------------|
| 253 | Meeting Rooms II | Med | Sort by start time. Min-heap of end times. For each meeting: if heap top ≤ start → reuse room (pop). Push new end. Heap size = rooms needed. |
| 347 | Top K Frequent Elements | Med | Count frequencies. Then either: min-heap of size k, OR bucket sort (index = frequency). |
| 502 | IPO | Hard | Greedy + two heaps. Sort projects by capital needed. Max-heap of profits for affordable projects. Pick most profitable, increase capital, repeat k times. |
| 2163 | Min Diff After Removal | Hard | Split array. Left: remove elements to minimize sum (use max-heap to track what to remove). Right: remove to maximize sum (use min-heap). Prefix/suffix approach. |

---

## 10. DP (1)
| # | Problem | Diff | How to think |
|---|---------|------|-------------|
| 139 | Word Break | Med | dp[i] = can s[:i] be segmented? For each i, check all j < i: if dp[j] and s[j:i] in wordDict → dp[i] = True. |

---

## 11. Backtracking / Trie (1)
| # | Problem | Diff | How to think |
|---|---------|------|-------------|
| 212 | Word Search II | Hard | Build Trie from all words. DFS on grid, walk Trie simultaneously. Prune branches when no Trie match. Much faster than running Word Search for each word separately. |

---

## 12. Design (4) — "pick the right data structures"
| # | Problem | Diff | Core DS | How to think |
|---|---------|------|---------|-------------|
| 146 | LRU Cache | Med | HashMap + Doubly Linked List | Map for O(1) lookup. DLL for O(1) move-to-front and evict-last. |
| 362 | Design Hit Counter | Med | Queue or circular array | Store timestamps. getHits: count timestamps in last 300s. Queue: pop old ones. Array: mod 300. |
| 981 | Time Based Key-Value Store | Med | HashMap + Binary Search | Map key → list of (timestamp, value). Get: binary search for largest timestamp ≤ target. |
| 1429 | First Unique Number | Med | HashMap + Doubly Linked List (or OrderedDict) | Like LRU. Track count. When count > 1, remove from DLL. First unique = head of DLL. |

---

## 13. Divide and Conquer (1)
| # | Problem | Diff | How to think |
|---|---------|------|-------------|
| 427 | Construct Quad Tree | Med | Recursive. If all values same → leaf. Else split into 4 quadrants, recurse on each. |

---

## 14. Math / Greedy (5)
| # | Problem | Diff | How to think |
|---|---------|------|-------------|
| 204 | Count Primes | Med | Sieve of Eratosthenes. Array of bools. For each prime p, mark p*p, p*p+p, ... as not prime. |
| 399 | Evaluate Division | Med | Build weighted graph: a/b=2 → edge a→b weight 2, b→a weight 0.5. Query a/c = DFS from a to c, multiply weights along path. |
| 564 | Closest Palindrome | Hard | Generate candidates: mirror first half, mirror first half ±1, edge cases (999→1001, 1000→999). Check which candidate is closest. |
| 2561 | Rearranging Fruits | Hard | Find mismatched fruits between baskets. Pair them up. Each swap costs min of the two. Trick: can use smallest element as intermediary (2 swaps cheaper than 1 direct). |
| 2571 | Min Ops to Reduce to 0 | Med | Greedy with bit manipulation. Process highest set bit. Either subtract power of 2 or add to next power. Think in binary. |
| 2503 | Max Points From Grid Queries | Hard | Sort queries. BFS/Union Find: process cells in order of value. For each query threshold, count reachable cells from (0,0). |

---

## Priority Order for Study

**Tier 1 — Most likely to appear, must know:**
1. 200 Number of Islands (DFS grid template)
2. 207 Course Schedule (topo sort template)
3. 146 LRU Cache (design classic)
4. 253 Meeting Rooms II (heap intervals)
5. 139 Word Break (DP)
6. 347 Top K Frequent (heap/bucket)
7. 200 → 305 Islands II (union find)
8. 162 Find Peak Element (binary search)
9. 127 Word Ladder (BFS)

**Tier 2 — Common patterns:**
10. 227 Basic Calculator II
11. 269 Alien Dictionary
12. 79 Word Search
13. 981 Time Based KV Store
14. 752 Open the Lock
15. 934 Shortest Bridge
16. 399 Evaluate Division
17. 977 Squares of Sorted Array

**Tier 3 — Less common but possible:**
18+ remaining problems