from typing import List

from collections import defaultdict, deque


class Solution:
    def numBusesToDestination(self, routes: List[List[int]], source: int, target: int) -> int:

        if source == target:
            return 0

        # STEP 1: Build stop → routes map
        stop_to_routes = defaultdict(set)
        for route_id, stops in enumerate(routes):
            for stop in stops:
                stop_to_routes[stop].add(route_id)

        # STEP 2: BFS at the route level
        # Start with all routes that serve the source stop
        visited_routes = set()
        queue = deque()

        for route_id in stop_to_routes[source]:
            queue.append(route_id)
            visited_routes.add(route_id)

        bus_count = 1  # we boarded one bus
        while queue:
            # Process one BFS level (all routes at current bus_count)
            for _ in range(len(queue)):
                route_id = queue.popleft()

                # Check every stop on this route
                for stop in routes[route_id]:
                    # Found target!
                    if stop == target:
                        return bus_count

                    # Find new routes reachable from this stop
                    for next_route in stop_to_routes[stop]:
                        if next_route not in visited_routes:
                            visited_routes.add(next_route)
                            queue.append(next_route)

            bus_count += 1

        return -1


if __name__ == "__main__":
    sol = Solution()
    routes = [[1, 2, 7], [3, 6, 7]]
    source = 1
    target = 6
    print(sol.numBusesToDestination(routes, source, target))
