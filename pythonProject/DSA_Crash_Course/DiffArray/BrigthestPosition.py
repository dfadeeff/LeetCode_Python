from typing import List


def find_brightest_position(lights: List[List[int]]) -> int:
    change = []
    for position, radius in lights:
        change.append([position - radius, 1])
        change.append([position + radius + 1, -1])

    change.sort()
    ans = curr = brightest = 0
    for position, value in change:
        curr += value
        if curr > brightest:
            brightest = curr
            ans = position

    return ans
