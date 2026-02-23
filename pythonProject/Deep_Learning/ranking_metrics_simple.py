"""
RANKING METRICS — from scratch.

Search engines / retrieval systems return a RANKED LIST of results.
We need metrics to measure: "how good is this ranking?"

KEY METRICS:
  1. Precision@K:  of the top K results, how many are relevant?
  2. Recall@K:     of ALL relevant items, how many are in top K?
  3. MRR:          how far down is the FIRST relevant result?
  4. nDCG@K:       are the MOST relevant results ranked HIGHEST?

These are THE metrics asked about in ML interviews for search/retrieval.
"""
import numpy as np


# ================================================================
# THE DATA: search results with relevance scores
# ================================================================
print("=" * 60)
print("RANKING METRICS — measuring search quality")
print("=" * 60)

print("""
  Scenario: user searches "python tutorial"
  System returns 6 documents, ranked 1-6:

    Rank 1: "Learn Python Basics"       → relevant (1)
    Rank 2: "Java Tutorial"             → not relevant (0)
    Rank 3: "Python Advanced Guide"     → relevant (1)
    Rank 4: "C++ for Beginners"         → not relevant (0)
    Rank 5: "Python Data Science"       → relevant (1)
    Rank 6: "Cooking Recipes"           → not relevant (0)

  Total relevant documents in the collection: 4
  (one relevant doc wasn't retrieved at all)
""")

# 1 = relevant, 0 = not relevant
relevance = [1, 0, 1, 0, 1, 0]
total_relevant = 4  # total relevant docs in the entire collection


# ================================================================
# 1. PRECISION@K
# ================================================================
print("─" * 60)
print("1. PRECISION@K — what fraction of top-K results are relevant?")
print("─" * 60)


def precision_at_k(relevance, k):
    """
    Precision@K = (# relevant in top K) / K

    "Of what I showed the user, how much was useful?"
    """
    top_k = relevance[:k]
    n_relevant = sum(top_k)
    precision = n_relevant / k
    return precision


for k in [1, 2, 3, 5, 6]:
    p = precision_at_k(relevance, k)
    top_k = relevance[:k]
    print(f"  P@{k} = {sum(top_k)} relevant / {k} shown = {p:.2f}")

print(f"""
  Interpretation:
    P@1 = 1.00 → top result is relevant (great!)
    P@3 = 0.67 → 2 out of 3 top results are relevant
    P@6 = 0.50 → half of all results are relevant
""")


# ================================================================
# 2. RECALL@K
# ================================================================
print("─" * 60)
print("2. RECALL@K — what fraction of ALL relevant docs are in top-K?")
print("─" * 60)


def recall_at_k(relevance, k, total_relevant):
    """
    Recall@K = (# relevant in top K) / (total relevant in collection)

    "Of everything useful that exists, how much did I find?"
    """
    top_k = relevance[:k]
    n_relevant = sum(top_k)
    recall = n_relevant / total_relevant
    return recall


for k in [1, 2, 3, 5, 6]:
    r = recall_at_k(relevance, k, total_relevant)
    top_k = relevance[:k]
    print(f"  R@{k} = {sum(top_k)} found / {total_relevant} exist = {r:.2f}")

print(f"""
  Interpretation:
    R@1 = 0.25 → found 1 of 4 relevant docs
    R@6 = 0.75 → found 3 of 4 (missed 1 relevant doc entirely)

  Precision vs Recall tradeoff:
    ↑ K → recall ↑ (find more) but precision ↓ (more junk)
    ↓ K → precision ↑ (less junk) but recall ↓ (miss stuff)
""")


# ================================================================
# 3. MRR — Mean Reciprocal Rank
# ================================================================
print("─" * 60)
print("3. MRR — how far down is the first relevant result?")
print("─" * 60)


def reciprocal_rank(relevance):
    """
    RR = 1 / (rank of first relevant result)

    If first relevant result is rank 1 → RR = 1.0 (perfect)
    If first relevant result is rank 5 → RR = 0.2 (bad)
    """
    for i, rel in enumerate(relevance):
        if rel == 1:
            return 1.0 / (i + 1)
    return 0.0


def mrr(queries_relevance):
    """
    MRR = average RR across multiple queries.
    """
    rrs = [reciprocal_rank(rel) for rel in queries_relevance]
    return np.mean(rrs)


# Multiple queries
queries = {
    "python tutorial": [1, 0, 1, 0, 1, 0],   # first relevant at rank 1
    "machine learning": [0, 0, 1, 1, 0, 0],   # first relevant at rank 3
    "data science":     [0, 1, 0, 0, 1, 0],   # first relevant at rank 2
}

print(f"\n  Three queries and their results:\n")
rrs = []
for query, rel in queries.items():
    rr = reciprocal_rank(rel)
    first_rel = rel.index(1) + 1
    rrs.append(rr)
    print(f"    '{query}':")
    print(f"      Results: {rel}")
    print(f"      First relevant at rank {first_rel} → RR = 1/{first_rel} = {rr:.4f}")

mean_rr = np.mean(rrs)
print(f"\n  MRR = mean({[round(r, 4) for r in rrs]}) = {mean_rr:.4f}")
print(f"\n  MRR close to 1 → first relevant result is usually at the top")
print(f"  MRR close to 0 → user has to scroll far to find anything useful")


# ================================================================
# 4. nDCG — Normalized Discounted Cumulative Gain
# ================================================================
print(f"\n{'─' * 60}")
print("4. nDCG@K — are the MOST relevant results ranked highest?")
print("─" * 60)

print("""
  Unlike P@K (binary: relevant/not), nDCG handles GRADED relevance:
    3 = highly relevant
    2 = relevant
    1 = somewhat relevant
    0 = not relevant

  A highly relevant doc at rank 1 is MUCH better than at rank 5.
  nDCG captures this with a LOG DISCOUNT.
""")


def dcg_at_k(relevance, k):
    """
    DCG@K = Σ (relevance_i / log2(i + 1))  for i = 1..K

    Higher relevance + higher rank → more gain.
    Log discount: rank 1 counts most, rank 10 counts little.
    """
    dcg = 0
    for i in range(min(k, len(relevance))):
        gain = relevance[i]
        discount = np.log2(i + 2)  # i+2 because i starts at 0, rank starts at 1
        dcg += gain / discount
    return dcg


def ndcg_at_k(relevance, k):
    """
    nDCG@K = DCG@K / IDCG@K

    IDCG = DCG of the IDEAL ranking (sort by relevance, best first).
    Normalizes to [0, 1] so we can compare across queries.
    """
    dcg = dcg_at_k(relevance, k)

    # Ideal: sort relevance descending
    ideal = sorted(relevance, reverse=True)
    idcg = dcg_at_k(ideal, k)

    if idcg == 0:
        return 0
    return dcg / idcg


# Graded relevance example
graded_rel = [3, 2, 0, 1, 2, 0]

print(f"  Example with graded relevance:")
print(f"  Results: {graded_rel}")
print(f"  (3=highly relevant, 2=relevant, 1=somewhat, 0=not)\n")

print(f"  --- DCG@K calculation (step by step) ---\n")
print(f"  {'Rank':<6} {'Relevance':<12} {'log2(rank+1)':<14} {'Gain/Discount':<14} {'Cumulative':<10}")
print(f"  {'─'*56}")

cumulative = 0
for i in range(len(graded_rel)):
    gain = graded_rel[i]
    discount = np.log2(i + 2)
    contribution = gain / discount
    cumulative += contribution
    print(f"  {i+1:<6} {gain:<12} {discount:<14.4f} {contribution:<14.4f} {cumulative:<10.4f}")

print(f"\n  DCG@6 = {dcg_at_k(graded_rel, 6):.4f}")

# Ideal ranking
ideal = sorted(graded_rel, reverse=True)
print(f"\n  Ideal ranking: {ideal}")
print(f"  IDCG@6 = {dcg_at_k(ideal, 6):.4f}")

for k in [1, 3, 5, 6]:
    score = ndcg_at_k(graded_rel, k)
    print(f"\n  nDCG@{k} = DCG@{k} / IDCG@{k} = {dcg_at_k(graded_rel, k):.4f} / {dcg_at_k(ideal, k):.4f} = {score:.4f}")

print(f"""
  Interpretation:
    nDCG = 1.0 → perfect ranking (best results on top)
    nDCG = 0.0 → terrible ranking

    nDCG is THE standard metric for search ranking.
    Dropbox, Google, Bing all optimize for nDCG.
""")


# ================================================================
# 5. MAP — Mean Average Precision
# ================================================================
print("─" * 60)
print("5. AP & MAP — Average Precision across the ranking")
print("─" * 60)


def average_precision(relevance):
    """
    AP = average of Precision@k at each relevant position.

    Only compute P@k where result k IS relevant.
    Rewards having relevant results early.
    """
    precisions = []
    n_relevant = 0

    for i in range(len(relevance)):
        if relevance[i] == 1:
            n_relevant += 1
            precisions.append(n_relevant / (i + 1))

    if len(precisions) == 0:
        return 0
    return np.mean(precisions)


rel_example = [1, 0, 1, 0, 1, 0]
print(f"\n  Relevance: {rel_example}\n")
print(f"  Compute P@k only at relevant positions:")

n_rel = 0
precs = []
for i in range(len(rel_example)):
    if rel_example[i] == 1:
        n_rel += 1
        p = n_rel / (i + 1)
        precs.append(p)
        print(f"    Rank {i+1} (relevant): P@{i+1} = {n_rel}/{i+1} = {p:.4f}")
    else:
        print(f"    Rank {i+1} (not relevant): skip")

ap = average_precision(rel_example)
print(f"\n  AP = mean({[round(p, 4) for p in precs]}) = {ap:.4f}")

# MAP across queries
print(f"\n  MAP = mean AP across multiple queries:")
aps = []
for query, rel in queries.items():
    ap = average_precision(rel)
    aps.append(ap)
    print(f"    '{query}': AP = {ap:.4f}")
map_score = np.mean(aps)
print(f"\n  MAP = {map_score:.4f}")


# ================================================================
# SUMMARY
# ================================================================
print(f"""
{'=' * 60}
RANKING METRICS SUMMARY
{'=' * 60}

  ┌──────────────┬───────────────────────────────┬─────────────────────────┐
  │ Metric       │ What it measures              │ Formula                 │
  ├──────────────┼───────────────────────────────┼─────────────────────────┤
  │ P@K          │ Fraction relevant in top K    │ #relevant / K           │
  │ R@K          │ Fraction of all relevant      │ #found / #total_rel     │
  │              │ found in top K                │                         │
  │ MRR          │ Rank of first relevant result │ mean(1/rank_first_rel)  │
  │ nDCG@K       │ Graded relevance, position-   │ DCG / IDCG              │
  │              │ weighted (THE key metric)     │                         │
  │ MAP          │ Average precision at each     │ mean(P@k at relevant k) │
  │              │ relevant position             │                         │
  └──────────────┴───────────────────────────────┴─────────────────────────┘

  WHICH TO USE:
    Binary relevance (yes/no):    P@K, R@K, MRR, MAP
    Graded relevance (0,1,2,3):   nDCG@K (industry standard)

  INTERVIEW: "How would you evaluate a search system?"
    → "nDCG@K for ranking quality, MRR for how quickly users find
       what they need, P@K and R@K for coverage vs precision tradeoff."
""")