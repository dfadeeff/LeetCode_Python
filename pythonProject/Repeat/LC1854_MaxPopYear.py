from typing import List


class Solution:
    def maximumPopulation(self, logs: List[List[int]]) -> int:
        events = []
        # Create events: +1 for birth, -1 for death (person not counted in death year)
        for birth, death in logs:
            events.append((birth, 1))
            events.append((death, -1))

        # Sort events: first by year, then by type (-1 comes after +1 if same year)
        events.sort(key=lambda x: (x[0], x[1]))

        max_population = 0
        current_population = 0
        earliest_year = 0

        # Sweep through all events
        for year, change in events:
            current_population += change
            # Update max_population and earliest_year if we found a new maximum
            if current_population > max_population:
                max_population = current_population
                earliest_year = year

        return earliest_year

if __name__ == "__main__":
    logs = [[1950, 1961], [1960, 1971], [1970, 1981]]
    print(Solution().maximumPopulation(logs))

