import heapq
from typing import List
from collections import defaultdict


class Twitter:

    def __init__(self):
        self.count = 0
        self.tweetMap = defaultdict(list)  # userId -> list of [count, tweetIds]
        self.followMap = defaultdict(set)  # userId -> set of followeeId

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.tweetMap[userId].append([self.count, tweetId])
        self.count -= 1

    def getNewsFeed(self, userId: int) -> List[int]:
        res = []
        minheap = []

        # including themselves
        self.followMap[userId].add(userId)

        for followeeId in self.followMap[userId]:
            if followeeId in self.tweetMap:
                index = len(self.tweetMap[followeeId]) - 1  # last value
                count, tweetId = self.tweetMap[followeeId][index]
                minheap.append([count, tweetId, followeeId, index - 1])
        heapq.heapify(minheap)

        while minheap and len(res) < 10:
            count, tweetId, followeeId, index = heapq.heappop(minheap)
            res.append(tweetId)

            if index >= 0:
                count, tweetId = self.tweetMap[followeeId][index]
                heapq.heappush(minheap, [count, tweetId, followeeId, index - 1])

        return res

    def follow(self, followerId: int, followeeId: int) -> None:
        self.followMap[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        if followeeId in self.followMap[followerId]:
            self.followMap[followerId].remove(followeeId)

if __name__ == "__main__":
    twitter = Twitter()

    twitter.postTweet(1, 5)             # User 1 posts tweet 5
    print(twitter.getNewsFeed(1))       # [5]

    twitter.follow(1, 2)                # User 1 follows User 2
    twitter.postTweet(2, 6)             # User 2 posts tweet 6
    print(twitter.getNewsFeed(1))       # [6, 5]

    twitter.unfollow(1, 2)              # User 1 unfollows User 2
    print(twitter.getNewsFeed(1))       # [5]
