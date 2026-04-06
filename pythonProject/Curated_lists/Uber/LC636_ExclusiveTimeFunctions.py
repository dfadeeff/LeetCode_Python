from typing import List


class Solution:
    def exclusiveTime(self, n: int, logs: List[str]) -> List[int]:

        """
        Why +1 on end but not start?
        Timestamps are INCLUSIVE on end:

        "1:end:5" means function 1 runs THROUGH end of timestamp 5
          occupies timestamps 2,3,4,5 = 4 units

        duration = end - start + 1 = 5-2+1 = 4
        """
        execution_times = [0] * n

        call_stack = []
        prev_start_time = 0  # ← tracks start of current segment
        for log in logs:
            func_id, call_type, timestamp = log.split(":")

            func_id = int(func_id)
            timestamp = int(timestamp)

            if call_type == 'start':
                if call_stack:
                    execution_times[call_stack[-1]] += timestamp - prev_start_time

                call_stack.append(func_id)
                prev_start_time = timestamp

            else:
                execution_times[call_stack.pop()] += timestamp - prev_start_time + 1
                prev_start_time = timestamp + 1

        return execution_times


if __name__ == "__main__":
    sol = Solution()
    """
        n=2, logs=["0:start:0","1:start:2","1:end:5","0:end:6"]

        result = [0, 0]
        stack  = []
        prev   = 0        ← tracks start of current segment
        
        ━━━ "0:start:0" ━━━
        stack empty → just push
        stack = [0]
        prev  = 0
        
        ━━━ "1:start:2" ━━━
        func 0 was running from prev=0 to now=2
        result[0] += 2-0 = 2
        push func 1
        stack = [0,1]
        prev  = 2
        
        result = [2,0]
        
        ━━━ "1:end:5" ━━━
        func 1 was running from prev=2 to now=5
        result[1] += 5-2+1 = 4   ← +1 because end is inclusive
        pop func 1
        stack = [0]
        prev  = 5+1 = 6           ← next segment starts after end
        
        result = [2,4]
        
        ━━━ "0:end:6" ━━━
        func 0 was running from prev=6 to now=6
        result[0] += 6-6+1 = 1
        pop func 0
        stack = []
        prev  = 7
        
        result = [3,4] ✅
    """
    n = 2
    logs = ["0:start:0", "1:start:2", "1:end:5", "0:end:6"]
    print(sol.exclusiveTime(n, logs))
