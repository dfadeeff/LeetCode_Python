def dailyTemperatures(temperatures: list[int]) -> list[int]:
    stack = []
    answer = [0] * len(temperatures)

    for i in range(len(temperatures)):
        while stack and temperatures[stack[-1]] < temperatures[i]:
            j = stack.pop()
            answer[j] = i - j
        stack.append(i)

    return answer


if __name__ == '__main__':
    temperatures1 = [73, 74, 75, 71, 69, 72, 76, 73]
    print(dailyTemperatures(temperatures1))
    temperatures2 = [30, 40, 50, 60]
    print(dailyTemperatures(temperatures2))
