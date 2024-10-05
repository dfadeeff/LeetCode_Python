def finalPrices(prices: list[int]) -> list[int]:
    stack = []
    # Result array initialized with the original prices
    result = prices[:]

    # Iterate through the prices
    for i in range(len(prices)):
        # While stack is not empty and the current price is less than or equal to the price at the top of the stack
        # If current price is smaller than the price from index of the top of the stack, stack[-1] the rightmost element
        while stack and prices[i] <= prices[stack[-1]]:
            # Pop the top index from the stack and apply the discount
            top_index = stack.pop()
            result[top_index] = prices[top_index] - prices[i]

        # Push the current index onto the stack
        stack.append(i)

    # Return the result array with final prices after discount
    return result



if __name__ == '__main__':
    prices = [8, 4, 6, 2, 3]
    print(finalPrices(prices))