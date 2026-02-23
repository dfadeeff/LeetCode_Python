# ML System Design Guide — Search, Retrieval & AI at Scale

> Curated for Dropbox Dash-style ML Engineer roles.
> Complements ByteByteGo with ML-specific depth.

---

## Table of Contents

1. [Framework: How to Answer ML System Design Questions](#1-framework)
2. [Core Building Blocks](#2-core-building-blocks)
3. [Design: Semantic Search System (Dropbox Dash)](#3-semantic-search)
4. [Design: RAG System at Scale](#4-rag-at-scale)
5. [Design: Multimodal Search (Images + Text)](#5-multimodal-search)
6. [Design: Recommendation / Ranking System](#6-recommendation-ranking)
7. [Design: Embedding Training Pipeline](#7-embedding-pipeline)
8. [Model Serving & Inference at Scale](#8-model-serving)
9. [Evaluation & Metrics](#9-evaluation)
10. [Common Interview Questions](#10-interview-questions)

---

## 1. Framework: How to Answer ML System Design Questions <a id="1-framework"></a>

Use this 4-step structure for every ML design question (25-30 min total):

### Step 1: Clarify Requirements (3-5 min)
- What's the user experience? (search box, feed, recommendations?)
- Scale: how many users, documents, queries/sec?
- Latency requirements? (search: <200ms, recommendations: <500ms)
- Online vs offline? Real-time vs batch?
- What data is available? (click logs, labels, user behavior)

### Step 2: High-Level Architecture (5 min)
- Draw the end-to-end pipeline
- Identify ML vs non-ML components
- Offline (training, indexing) vs Online (serving, inference)

### Step 3: Deep Dive into ML Components (15 min)
- Feature engineering / data representation
- Model choice and training
- Metrics and evaluation
- Iteration and improvement

### Step 4: Scaling, Failure Modes, Extensions (5 min)
- How to handle 10x scale?
- What can go wrong? How to monitor?
- A/B testing and deployment

---

## 2. Core Building Blocks <a id="2-core-building-blocks"></a>

Every ML system at scale uses combinations of these:

### 2.1 Embedding Models
```
Purpose: convert raw data (text, image, audio) → dense vectors

Text:  sentence-transformers, E5, BGE, OpenAI embeddings
Image: CLIP, SigLIP, DINOv2
Multi: CLIP (text+image), ImageBind (text+image+audio+video)

Key decisions:
  - Dimension: 384 (fast) vs 768 (accurate) vs 1536 (max quality)
  - Pre-trained vs fine-tuned (always fine-tune for your domain!)
  - Normalize? Yes → cosine similarity = dot product (faster)
```

### 2.2 Vector Index / ANN
```
Purpose: fast nearest-neighbor search over millions of vectors

Methods:
  IVF (FAISS):    cluster-based, good for large scale, GPU support
  HNSW:           graph-based, best recall/speed, higher memory
  ScaNN (Google): quantization-based, good balance

Key decisions:
  - nprobe (IVF): how many clusters to search (recall vs speed)
  - ef (HNSW): how many neighbors to explore (recall vs speed)
  - PQ (Product Quantization): compress vectors for memory savings

Production tools: FAISS, Pinecone, Weaviate, Qdrant, Milvus
```

### 2.3 Two-Stage Retrieval
```
Stage 1: RETRIEVAL (recall-focused, fast)
  - ANN search on embeddings → top 100-1000 candidates
  - BM25 keyword search (complement to semantic)
  - Hybrid: combine both with reciprocal rank fusion
  - Latency target: <10ms

Stage 2: RE-RANKING (precision-focused, slower)
  - Cross-encoder: takes (query, doc) pair → relevance score
  - Much more accurate than bi-encoder but O(n) per query
  - Only applied to candidates from Stage 1
  - Latency target: <50-100ms

Why two stages:
  Bi-encoder:    embed separately, dot product → fast, less accurate
  Cross-encoder: embed together, full attention → slow, very accurate
  Use bi-encoder to narrow, cross-encoder to pick best.
```

### 2.4 Feature Store
```
Purpose: serve pre-computed features at low latency

Components:
  - Offline store: batch features (user history, doc stats)
  - Online store: real-time features (session context, recent clicks)
  - Feature computation: Spark/Flink for batch, streaming for real-time

Tools: Feast, Tecton, home-grown (Redis + Spark)
```

### 2.5 Model Serving
```
Purpose: run ML model inference at scale

Options:
  - REST API: simple, high latency (Flask, FastAPI)
  - gRPC: lower latency, binary protocol
  - Triton Inference Server: batching, multi-model, GPU
  - TorchServe: PyTorch native
  - vLLM / TGI: for LLM serving specifically

Key patterns:
  - Batching: group requests for GPU efficiency
  - Model parallelism: split large models across GPUs
  - Caching: cache embeddings, cache frequent queries
  - Quantization: INT8/FP16 for faster inference
  - Distillation: train smaller model to mimic larger one
```

---

## 3. Design: Semantic Search System (Dropbox Dash) <a id="3-semantic-search"></a>

> "Design a universal search system that searches across multiple apps
> (Google Docs, Slack, GitHub, email) and returns relevant results."

### Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        OFFLINE PIPELINE                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Connectors          Document Processing       Indexing         │
│  ┌─────────┐        ┌──────────────────┐      ┌────────────┐  │
│  │ G.Docs  │───┐    │ Extract text      │      │ Embedding  │  │
│  │ Slack   │───┤    │ Chunk (500 tok)   │      │ Model      │  │
│  │ GitHub  │───┼───►│ Clean / normalize │─────►│ (bi-encoder│──►│ Vector
│  │ Email   │───┤    │ Extract metadata  │      │  768D)     │  │  Index
│  │ Dropbox │───┘    │ OCR for images    │      └────────────┘  │ (FAISS/
│  └─────────┘        └──────────────────┘                       │  HNSW)
│                                                                 │
│  Incremental sync: webhook/polling → re-embed changed docs     │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                        ONLINE PIPELINE                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  User Query → Query Processing → Hybrid Retrieval → Re-ranking │
│                                                                 │
│  ┌──────────┐   ┌───────────┐   ┌──────────────┐  ┌─────────┐ │
│  │ "merge   │   │ Query     │   │ Semantic     │  │ Cross-  │ │
│  │  PDFs"   │──►│ embed +   │──►│ (ANN) +      │─►│ encoder │─►│ Top 10
│  │          │   │ expand    │   │ Keyword(BM25)│  │ rerank  │ │ results
│  └──────────┘   └───────────┘   └──────────────┘  └─────────┘ │
│                                                                 │
│  Additional signals: recency, source authority, user history    │
└─────────────────────────────────────────────────────────────────┘
```

### Key Design Decisions

**Chunking strategy:**
- 500 tokens per chunk, 50 token overlap
- Keep metadata: source app, author, timestamp, file type
- Parent-child: store chunk → doc mapping for context expansion

**Hybrid search:**
- Semantic: bi-encoder embeddings + ANN (captures meaning)
- Keyword: BM25/Elasticsearch (captures exact terms, acronyms)
- Merge: Reciprocal Rank Fusion (RRF): score = 1/(k + rank_semantic) + 1/(k + rank_keyword)

**Personalization:**
- User's recent docs boosted
- Source app weighting (prefer Slack for recent, Docs for reference)
- Click-through feedback → fine-tune ranking model

**Freshness:**
- Webhook-based sync for real-time updates
- TTL on embeddings, re-embed periodically
- Recency decay in ranking score

**Scale numbers (Dropbox-level):**
- 700M+ registered users
- Billions of documents
- Embedding index: sharded across machines
- Query latency target: <200ms end-to-end

---

## 4. Design: RAG System at Scale <a id="4-rag-at-scale"></a>

> "Design a system where users ask questions and get answers
> grounded in their documents (like Dash AI answers)."

### Architecture

```
┌──────────────────────────────────────────────────────────┐
│  User: "When is the project deadline?"                   │
│                                                          │
│  1. Query Understanding                                  │
│     ├── Intent classification (search vs question)       │
│     ├── Query rewriting (expand, clarify)                │
│     └── Filter extraction (date range, source)           │
│                                                          │
│  2. Retrieval (same as search pipeline)                  │
│     ├── Semantic search → top 20 chunks                  │
│     ├── Keyword search → top 20 chunks                   │
│     └── Merge + re-rank → top 5 chunks                   │
│                                                          │
│  3. Context Assembly                                     │
│     ├── Select chunks that fit context window            │
│     ├── Add metadata (source, date, author)              │
│     └── Order by relevance                               │
│                                                          │
│  4. Generation                                           │
│     ├── Prompt: system + context + query                 │
│     ├── LLM generates answer with citations              │
│     └── Post-process: extract citations, format          │
│                                                          │
│  5. Safety & Quality                                     │
│     ├── Faithfulness check: is answer supported?         │
│     ├── PII detection: don't leak sensitive info         │
│     └── Fallback: "I don't have enough info"             │
└──────────────────────────────────────────────────────────┘
```

### Key Challenges at Scale

**Context window management:**
- Chunk size vs retrieval recall tradeoff
- Hierarchical retrieval: retrieve chunks → expand to surrounding context
- Map-reduce for long answers: summarize chunks → combine summaries

**Latency optimization:**
- Streaming: start generating while still retrieving
- Cache frequent queries and their answers
- Pre-compute embeddings for popular documents

**Quality measurement:**
- Faithfulness: does the answer match the source?
- Relevance: does the answer address the question?
- Completeness: does it cover all relevant info?
- Human evaluation + automated metrics (RAGAS framework)

**Multi-turn conversation:**
- Maintain conversation history
- Resolve coreferences ("What about the other project?")
- Progressive retrieval: each turn may need different docs

---

## 5. Design: Multimodal Search (Images + Text) <a id="5-multimodal-search"></a>

> "Design a system that can search across images, PDFs, and videos
> using text queries." (Dash multimedia search)

### Architecture

```
Document Processing per modality:

  Text docs  → text chunking → text encoder (BERT) → embedding
  Images     → CLIP image encoder → embedding
  PDFs       → OCR + layout parsing → text encoder → embedding
  Videos     → frame sampling → CLIP per frame → embeddings
               + audio → speech-to-text → text encoder → embedding

All embeddings live in the SAME vector space (thanks to CLIP alignment).

Query: "team photo from offsite"
  → CLIP text encoder → query embedding
  → ANN search across ALL modality embeddings
  → Returns: images, PDF pages, video frames that match
```

### Key Design Decisions

**Shared vs separate embedding spaces:**
- Shared (CLIP-style): one space for all modalities, simpler search
- Separate: per-modality index, merge results with fusion
- Hybrid: shared space + modality-specific refinement

**Video search:**
- Sample frames (1 per second or on scene change)
- Embed each frame with CLIP
- Query matches individual frames → return video + timestamp
- Alternative: aggregate frame embeddings per video segment

**PDF search:**
- OCR + layout analysis (detect tables, figures, headers)
- Chunk by logical sections (not fixed character count)
- Embed figures separately with CLIP
- Keep page-level context for display

---

## 6. Design: Recommendation / Ranking System <a id="6-recommendation-ranking"></a>

> "Design a system to rank search results or recommend files to users."

### Learning to Rank (LTR)

```
Training data: (query, document, relevance_label) from click logs

Features per (query, doc) pair:
  Query features:  query length, query type, query embeddings
  Doc features:    doc length, recency, popularity, source app
  Match features:  BM25 score, semantic similarity, term overlap
  User features:   past interactions, preferred sources

Models (in order of complexity):
  1. Pointwise: predict relevance score per doc (regression)
  2. Pairwise: predict which doc is more relevant (RankNet, LambdaRank)
  3. Listwise: optimize entire ranked list (LambdaMART, softmax loss)

Production choice: LambdaMART (XGBoost-based) or neural ranker (BERT)
Metric to optimize: nDCG@K
```

### Two-Tower Model (for retrieval)

```
┌──────────┐              ┌──────────┐
│  Query   │              │ Document │
│  Tower   │              │  Tower   │
│ (encoder)│              │ (encoder)│
└────┬─────┘              └────┬─────┘
     │                         │
  query_emb               doc_emb
     │                         │
     └────── dot product ──────┘
                  │
           similarity score

Train: contrastive loss on (query, positive_doc, negative_docs)
Serve: pre-compute doc embeddings, real-time query embedding + ANN
```

---

## 7. Design: Embedding Training Pipeline <a id="7-embedding-pipeline"></a>

> "How would you train and deploy custom embedding models?"

### Pipeline

```
┌────────────────────────────────────────────────────────┐
│  1. DATA COLLECTION                                    │
│     ├── Click logs: (query, clicked_doc) = positive    │
│     ├── Impression logs: (query, shown_not_clicked)    │
│     ├── Manual annotations: human relevance labels     │
│     └── Synthetic: LLM-generated query-doc pairs       │
│                                                        │
│  2. TRAINING                                           │
│     ├── Base model: pre-trained sentence-transformer   │
│     ├── Fine-tune with InfoNCE loss                    │
│     ├── Hard negative mining from previous model       │
│     ├── Multi-task: search + classification + cluster  │
│     └── Distillation: large model → small model        │
│                                                        │
│  3. EVALUATION                                         │
│     ├── Offline: retrieval recall@K on held-out queries │
│     ├── Online: A/B test on nDCG, click-through rate   │
│     └── Qualitative: inspect nearest neighbors         │
│                                                        │
│  4. DEPLOYMENT                                         │
│     ├── Quantize model (FP16/INT8) for speed           │
│     ├── Re-embed all documents (batch job, ~hours)     │
│     ├── Swap vector index atomically                   │
│     └── Monitor: embedding drift, latency, recall      │
└────────────────────────────────────────────────────────┘
```

### Training Details

**Data quality >> model architecture:**
- Clean, diverse query-doc pairs matter more than model size
- Hard negatives improve quality 10-30%
- Domain-specific fine-tuning beats general models

**Negative sampling strategies:**
- Random negatives: easy, works as baseline
- In-batch negatives: use other docs in the batch (efficient)
- Hard negatives: top-K from previous model that are NOT relevant
- Cross-batch negatives: negatives from other batches (MoCo-style)

---

## 8. Model Serving & Inference at Scale <a id="8-model-serving"></a>

### Latency Budget (search query, end-to-end <200ms)

```
Component             Latency Target    Technique
─────────────────────────────────────────────────────
Query embedding       <10ms             ONNX/TensorRT, batching
ANN search            <5ms              FAISS GPU, HNSW
BM25 keyword search   <10ms             Elasticsearch
Re-ranking (top 100)  <50ms             Cross-encoder, distilled
LLM generation (RAG)  <2000ms           Streaming, vLLM, caching
─────────────────────────────────────────────────────
Total (search)        <100ms
Total (RAG)           <2500ms (streaming helps UX)
```

### Scaling Patterns

**Embedding index sharding:**
- Shard by document ID range
- Query goes to ALL shards → merge top-K from each
- Replicate shards for throughput

**Model optimization:**
- Quantization: FP32 → FP16 (2x speed, ~0% quality loss)
- Quantization: FP32 → INT8 (4x speed, ~1% quality loss)
- Distillation: BERT-large → BERT-small (3x speed, ~2% quality loss)
- ONNX Runtime / TensorRT: compiler optimizations

**Caching:**
- Query embedding cache (LRU, TTL=1hr)
- Result cache for popular queries (TTL=5min)
- Document embedding cache (persist, invalidate on doc change)

---

## 9. Evaluation & Metrics <a id="9-evaluation"></a>

### Offline Metrics

| Metric | What it measures | When to use |
|--------|-----------------|-------------|
| nDCG@K | Ranking quality (graded) | Primary metric for search |
| MRR | Position of first relevant | Single-answer queries |
| Recall@K | Coverage of relevant docs | Retrieval stage |
| Precision@K | Relevance of shown results | User-facing quality |
| MAP | Average precision across ranking | Overall system quality |

### Online Metrics

| Metric | What it measures |
|--------|-----------------|
| Click-through rate (CTR) | Do users click results? |
| Mean time to click | How quickly do users find what they need? |
| Query abandonment rate | Do users give up? |
| Session success rate | Does the user complete their task? |
| Queries per session | Fewer = better (found it quickly) |

### A/B Testing for Search

```
Challenge: ranking changes affect ALL results, hard to isolate.

Approach:
  1. Interleaving: mix results from model A and B in one list
     User clicks → credit to whichever model produced that result
     More sensitive than side-by-side A/B with less traffic

  2. Online nDCG: use click data as implicit relevance labels
     Click = relevant, skip = not relevant (noisy but scalable)

  3. Long-term metrics: retention, engagement (not just clicks)
```

---

## 10. Common Interview Questions <a id="10-interview-questions"></a>

### Architecture / Deep Dive Questions

**Q: "How would you design search for Dropbox Dash?"**
→ Use the semantic search design from Section 3. Emphasize: hybrid retrieval
(semantic + keyword), two-stage (retrieve + re-rank), personalization,
multi-source connectors, freshness handling.

**Q: "How do you handle a new data source (e.g., adding Notion)?"**
→ Build a connector (API integration), extract text + metadata,
chunk and embed, add to existing index. Key challenge: incremental sync,
permission mapping (respect user access controls).

**Q: "Bi-encoder vs cross-encoder — when to use which?"**
→ Bi-encoder: fast, embed independently, good for retrieval (Stage 1).
Cross-encoder: slow, embed jointly, more accurate, good for re-ranking (Stage 2).
Always use both in a two-stage pipeline.

**Q: "How do you evaluate if your search is getting better?"**
→ Offline: nDCG on human-labeled query sets. Online: A/B test with
interleaving, measure CTR, time-to-click, abandonment rate.
Both matter — offline for fast iteration, online for real impact.

**Q: "How do you handle the cold start problem?"**
→ For new users: fall back to popularity-based ranking.
For new documents: embed immediately, use metadata features.
For new queries: query expansion, use similar known queries.

**Q: "How do you keep search results fresh?"**
→ Webhook-based sync (preferred), polling as fallback.
Re-embed changed docs incrementally. Recency boost in ranking.
TTL on cached results. Monitor staleness metrics.

**Q: "How would you add image search to a text search system?"**
→ Use CLIP to embed images and text into same space.
OCR for text-in-images. Same ANN index for both modalities.
Re-ranker may need modality-aware features.

**Q: "How do you scale the embedding index to billions of docs?"**
→ Shard by document ID, replicate for throughput.
Product Quantization (PQ) to compress vectors (768D → 64 bytes).
Use IVF+PQ in FAISS for memory-efficient search.
Tiered architecture: hot (recent, popular) in memory, cold on disk.

### Coding Round Expectations

Based on the JD, prepare to implement:
1. **Ranking metrics**: nDCG, MRR, Precision@K (see ranking_metrics_simple.py)
2. **Vector search**: cosine similarity, k-NN retrieval (see vector_retrieval_simple.py)
3. **Attention mechanism**: self-attention, multi-head (see transformer_simple.py)
4. **Embedding training**: contrastive/triplet loss (see contrastive_learning_simple.py)
5. **Standard DSA**: hashmaps, graphs, trees (LeetCode medium)
6. **Data processing**: pandas, numpy operations on large datasets

### Quick Reference: Dropbox Dash Tech Stack (likely)

```
Embeddings:     sentence-transformers (fine-tuned), CLIP for images
Vector index:   FAISS (IVF+HNSW+PQ)
Keyword search: Elasticsearch
Re-ranker:      cross-encoder (distilled BERT)
LLM:            Claude / GPT-4 (for RAG answers)
Serving:        Triton / vLLM
Data pipeline:  Spark + Kafka for batch + streaming
Feature store:  Redis (online) + Hive (offline)
Monitoring:     custom dashboards, nDCG tracking, latency p99
```