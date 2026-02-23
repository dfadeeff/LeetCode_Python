import numpy as np

from pythonProject.Deep_Learning.ranking_metrics_simple import top_k

"""
    Rank 1: "Learn Python Basics"     → relevant  (1)
    Rank 2: "Java Tutorial"           → junk      (0)
    Rank 3: "Python Advanced Guide"   → relevant  (1)
    Rank 4: "C++ for Beginners"       → junk      (0)
    Rank 5: "Python Data Science"     → relevant  (1)
    Rank 6: "Cooking Recipes"         → junk      (0)

"""
relevance = [1, 0, 1, 0, 1, 0]


def precision_K(relevance, k):
    top_k = relevance[:k]
    n_relevant = sum(top_k)
    return n_relevant / k

def recall_k(relevance, k):
    top_k = relevance[:k]
    n_relevant = sum(top_k)
    return n_relevant / sum(relevance)


if __name__ == "__main__":
    print(precision_K(relevance, 2))
    print(recall_k(relevance, 2))
