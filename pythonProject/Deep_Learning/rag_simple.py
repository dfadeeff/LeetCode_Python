"""
RAG (Retrieval-Augmented Generation) — from scratch.

LLM alone: answers from training data only (can hallucinate, stale info).
RAG: RETRIEVE relevant documents first, then feed them to the LLM.

  Without RAG:
    User: "What's Dropbox Dash?"
    LLM: "I don't know" or hallucinated answer

  With RAG:
    User: "What's Dropbox Dash?"
    → Retrieve: find docs about Dash from Dropbox's knowledge base
    → Augment: "Given these docs: [doc1, doc2], answer: What's Dropbox Dash?"
    → Generate: LLM answers using the retrieved context

THE RAG PIPELINE:
  1. OFFLINE: embed all documents → store in vector DB
  2. ONLINE:
     a. Embed query
     b. Retrieve top-K relevant docs (vector search)
     c. Augment: combine query + retrieved docs into a prompt
     d. Generate: LLM produces answer from augmented prompt

This is EXACTLY what Dropbox Dash does — search across all your tools
(Google Docs, Slack, GitHub, etc.) and answer questions using RAG.
"""
import numpy as np

np.random.seed(42)


# ================================================================
# HELPER: cosine similarity
# ================================================================
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# ================================================================
# STEP 1: DOCUMENT STORE (simulate a knowledge base)
# ================================================================
print("=" * 60)
print("RAG PIPELINE — step by step")
print("=" * 60)

# Simulate a company's internal knowledge base
knowledge_base = [
    {
        "id": 0,
        "title": "Dropbox Dash Overview",
        "content": "Dropbox Dash is an AI-powered universal search tool that connects "
                   "all your apps and content in one place. It uses semantic search to "
                   "find information across Google Docs, Slack, GitHub, and more."
    },
    {
        "id": 1,
        "title": "How Dash Search Works",
        "content": "Dash uses embedding models to convert documents into dense vectors. "
                   "When a user searches, the query is embedded and compared against all "
                   "document vectors using approximate nearest neighbor search (HNSW). "
                   "Results are re-ranked using a cross-encoder for relevance."
    },
    {
        "id": 2,
        "title": "Dash Multimodal Search",
        "content": "Dash supports searching across images, PDFs, and videos. "
                   "It uses CLIP-based embeddings for image understanding and OCR for "
                   "text extraction from PDFs. Video search uses frame-level embeddings."
    },
    {
        "id": 3,
        "title": "Embedding Models",
        "content": "We use fine-tuned sentence transformers for text embedding. "
                   "Models are trained with contrastive learning on query-document pairs. "
                   "Embedding dimension is 768. We use FAISS for vector indexing."
    },
    {
        "id": 4,
        "title": "Company Vacation Policy",
        "content": "Employees get 20 days paid vacation per year. Unused days can be "
                   "carried over to next year up to a maximum of 5 days. Please submit "
                   "vacation requests at least 2 weeks in advance."
    },
    {
        "id": 5,
        "title": "Onboarding Guide",
        "content": "New employees should set up their development environment on day 1. "
                   "Install Python 3.10+, Docker, and clone the main repository. "
                   "Attend the engineering orientation session on your first Monday."
    },
]

print(f"\n  Knowledge base: {len(knowledge_base)} documents")
for doc in knowledge_base:
    print(f"    [{doc['id']}] {doc['title']}")


# ================================================================
# STEP 2: EMBED DOCUMENTS (offline, done once)
# ================================================================
print(f"\n{'─' * 60}")
print("STEP 2: Embed all documents (offline)")
print("─" * 60)


def fake_embed(text, dim=16):
    """
    Simulate an embedding model.
    In production: use sentence-transformers, OpenAI embeddings, etc.

    We fake it by hashing words into a vector so similar texts
    get somewhat similar vectors.
    """
    vector = np.zeros(dim)
    words = text.lower().split()
    for i, word in enumerate(words):
        # Simple hash: each word contributes to specific dimensions
        idx = hash(word) % dim
        vector[idx] += 1.0
        # Also add to neighboring dimensions for "softness"
        vector[(idx + 1) % dim] += 0.3
    # Normalize
    norm = np.linalg.norm(vector)
    if norm > 0:
        vector = vector / norm
    return vector


# Embed all documents
doc_embeddings = []
for doc in knowledge_base:
    text = doc['title'] + " " + doc['content']
    emb = fake_embed(text)
    doc_embeddings.append(emb)

doc_embeddings = np.array(doc_embeddings)
print(f"\n  Embedded {len(knowledge_base)} documents → shape: {doc_embeddings.shape}")
print(f"  Each document is now a {doc_embeddings.shape[1]}D vector")


# ================================================================
# STEP 3: RETRIEVAL (online, per query)
# ================================================================
print(f"\n{'─' * 60}")
print("STEP 3: Retrieve relevant documents for a query")
print("─" * 60)


def retrieve(query, doc_embeddings, knowledge_base, top_k=3, verbose=False):
    """
    Embed query → find top-K most similar documents.
    """
    query_vec = fake_embed(query)

    # Compute similarity to all documents
    scores = []
    for i, doc_emb in enumerate(doc_embeddings):
        sim = cosine_similarity(query_vec, doc_emb)
        scores.append((sim, i))

    # Sort by similarity (descending)
    scores.sort(key=lambda x: x[0], reverse=True)

    # Return top-K
    results = []
    if verbose:
        print(f"\n  Query: \"{query}\"")
        print(f"  Similarities to all documents:")
        for sim, idx in scores:
            marker = " ←" if idx in [s[1] for s in scores[:top_k]] else ""
            print(f"    [{sim:.4f}] {knowledge_base[idx]['title']}{marker}")

    for sim, idx in scores[:top_k]:
        results.append((sim, knowledge_base[idx]))

    return results


# Demo retrieval
query1 = "How does Dash search work?"
results1 = retrieve(query1, doc_embeddings, knowledge_base, top_k=3, verbose=True)


# ================================================================
# STEP 4: AUGMENT (build the prompt)
# ================================================================
print(f"\n{'─' * 60}")
print("STEP 4: Augment — build prompt with retrieved context")
print("─" * 60)


def build_rag_prompt(query, retrieved_docs):
    """
    Combine query + retrieved documents into an LLM prompt.
    This is the "augmented" part of RAG.
    """
    context_parts = []
    for i, (score, doc) in enumerate(retrieved_docs, 1):
        context_parts.append(f"Document {i} (relevance: {score:.2f}):\n"
                             f"Title: {doc['title']}\n"
                             f"{doc['content']}")

    context = "\n\n".join(context_parts)

    prompt = f"""Answer the question based ONLY on the provided context.
If the context doesn't contain the answer, say "I don't have enough information."

Context:
{context}

Question: {query}

Answer:"""

    return prompt


prompt1 = build_rag_prompt(query1, results1)
print(f"\n  Built prompt ({len(prompt1)} chars):\n")
for line in prompt1.split('\n'):
    print(f"    {line}")


# ================================================================
# STEP 5: GENERATE (simulate LLM response)
# ================================================================
print(f"\n{'─' * 60}")
print("STEP 5: Generate — LLM answers using the context")
print("─" * 60)


def fake_generate(prompt, query, retrieved_docs):
    """
    Simulate LLM generation.
    In production: call OpenAI/Anthropic/local LLM with the prompt.

    Here we just extract relevant sentences from retrieved docs.
    """
    # Simple extractive "generation": find sentences mentioning query keywords
    keywords = [w.lower() for w in query.split() if len(w) > 3]
    relevant_sentences = []

    for _, doc in retrieved_docs:
        sentences = doc['content'].split('. ')
        for sent in sentences:
            if any(kw in sent.lower() for kw in keywords):
                relevant_sentences.append(sent.strip())

    if relevant_sentences:
        return " ".join(relevant_sentences[:3])
    return "I don't have enough information to answer this question."


# ================================================================
# FULL RAG PIPELINE
# ================================================================
print(f"\n{'=' * 60}")
print("FULL RAG PIPELINE — end to end")
print("=" * 60)


def rag(query, doc_embeddings, knowledge_base, top_k=3, verbose=True):
    """
    Complete RAG pipeline:
    1. Retrieve relevant documents
    2. Build augmented prompt
    3. Generate answer
    """
    if verbose:
        print(f"\n  Query: \"{query}\"")

    # Step 1: Retrieve
    results = retrieve(query, doc_embeddings, knowledge_base, top_k=top_k)
    if verbose:
        print(f"\n  Retrieved {len(results)} documents:")
        for score, doc in results:
            print(f"    [{score:.4f}] {doc['title']}")

    # Step 2: Augment
    prompt = build_rag_prompt(query, results)
    if verbose:
        print(f"\n  Prompt length: {len(prompt)} chars")

    # Step 3: Generate
    answer = fake_generate(prompt, query, results)
    if verbose:
        print(f"\n  Answer: {answer}")

    return answer


# Test different queries
queries = [
    "How does Dash search work?",
    "What embedding models does Dash use?",
    "Can Dash search images and videos?",
    "What is the vacation policy?",
    "How do I set up my development environment?",
]

for q in queries:
    print(f"\n{'─' * 40}")
    rag(q, doc_embeddings, knowledge_base, top_k=2)


# ================================================================
# CHUNKING STRATEGIES
# ================================================================
print(f"""
{'=' * 60}
CHUNKING — how to split documents for RAG
{'=' * 60}

  Documents can be long. Embedding a whole document loses detail.
  Solution: split into CHUNKS, embed each chunk separately.

  Strategies:
  ┌────────────────────┬─────────────────────────────────────────┐
  │ Method             │ How                                     │
  ├────────────────────┼─────────────────────────────────────────┤
  │ Fixed-size         │ Every N characters (simple, can break   │
  │                    │ mid-sentence)                           │
  │ Sentence-based     │ Split on sentence boundaries            │
  │ Paragraph-based    │ Split on paragraph breaks               │
  │ Sliding window     │ Overlapping chunks (e.g., 500 chars     │
  │                    │ with 100 char overlap)                  │
  │ Semantic           │ Split where topic changes (using        │
  │                    │ embedding similarity between sections)  │
  └────────────────────┴─────────────────────────────────────────┘

  Best practice: 200-500 tokens per chunk, with 10-20% overlap.
""")


def chunk_text(text, chunk_size=100, overlap=20):
    """Simple sliding window chunking."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap  # slide with overlap
    return chunks


example_text = knowledge_base[1]['content']
chunks = chunk_text(example_text, chunk_size=80, overlap=15)
print(f"  Example: chunking a document (80 chars, 15 overlap):\n")
for i, chunk in enumerate(chunks):
    print(f"    Chunk {i}: \"{chunk}\"")


# ================================================================
# RAG FAILURE MODES & SOLUTIONS
# ================================================================
print(f"""
{'=' * 60}
RAG CHALLENGES (interview discussion points)
{'=' * 60}

  1. RETRIEVAL FAILURES:
     Problem: wrong documents retrieved → wrong answer
     Fix: better embeddings, hybrid search (keyword + semantic),
          query expansion, re-ranking

  2. CONTEXT WINDOW LIMITS:
     Problem: too many retrieved docs don't fit in LLM context
     Fix: better chunking, summarization, hierarchical retrieval

  3. HALLUCINATION:
     Problem: LLM ignores context and makes stuff up
     Fix: constrain generation, add "answer only from context" instruction,
          citation generation, faithfulness checks

  4. STALE DATA:
     Problem: documents change but embeddings aren't updated
     Fix: incremental re-indexing, timestamp-aware retrieval

  5. MULTI-HOP REASONING:
     Problem: answer requires info from MULTIPLE documents
     Fix: iterative retrieval (retrieve → reason → retrieve more),
          graph-based retrieval

{'=' * 60}
RAG ARCHITECTURE (what Dropbox Dash likely uses)
{'=' * 60}

  ┌──────────────────────────────────────────────────────────┐
  │                    USER QUERY                            │
  │                       │                                  │
  │                  ┌────▼────┐                             │
  │                  │  Query  │  (rewrite, expand,          │
  │                  │ Process │   embed)                    │
  │                  └────┬────┘                             │
  │                       │                                  │
  │            ┌──────────▼──────────┐                       │
  │            │   HYBRID RETRIEVAL  │                       │
  │            │  keyword + semantic │                       │
  │            └──────────┬──────────┘                       │
  │                       │ top ~100                         │
  │               ┌───────▼───────┐                          │
  │               │  RE-RANKER    │  (cross-encoder)         │
  │               └───────┬───────┘                          │
  │                       │ top ~5                           │
  │               ┌───────▼───────┐                          │
  │               │     LLM       │  (generate answer        │
  │               │  Generation   │   from context)          │
  │               └───────┬───────┘                          │
  │                       │                                  │
  │                  ANSWER + CITATIONS                      │
  └──────────────────────────────────────────────────────────┘
""")