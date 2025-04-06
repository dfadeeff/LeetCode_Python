from typing import List


class Solution:
    def matchPlayersAndTrainers(self, players: List[int], trainers: List[int]) -> int:
        players.sort()
        trainers.sort()

        ans = 0
        playerPointer = 0
        trainerPointer = 0

        while playerPointer < len(players) and trainerPointer < len(trainers):
            if trainers[trainerPointer] >= players[playerPointer]:
                ans += 1
                trainerPointer += 1
                playerPointer += 1
            else:
                trainerPointer += 1

        return ans


if __name__ == '__main__':
    players = [4, 7, 9]
    trainers = [8, 2, 5, 8]
    print(Solution().matchPlayersAndTrainers(players, trainers))
