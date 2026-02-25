# ML Architecture Prep — Dropbox Dash MLE
## Framework: ByteByteGo ML System Design

---

## THE FRAMEWORK (memorize this)

| Step | What to do | Time | Key question to answer |
|------|-----------|------|----------------------|
| 1. **Clarify Requirements** | Business objective, scale, data, latency | 2 min | "What are we optimizing?" |
| 2. **Frame as ML Task** | ML objective, input/output, ML category | 3 min | "What does the model predict?" |
| 3. **Data Preparation** | Data schema, feature engineering, dataset construction | 5 min | "How do we get training data?" |
| 4. **Model Development** | Architecture, loss function, training | 10 min | "Why this model? What loss?" |
| 5. **Evaluation** | Offline metrics + online metrics | 5 min | "How do we know it works?" |
| 6. **Serving** | 3 pipelines: training, indexing, prediction | 10 min | "How do we deploy at scale?" |

---

## Scenario 1: Design Multimodal File Search for Dropbox Dash

*"Design a system where users can search across all their files (docs, images, PDFs, slides) with a single text query."*

### Step 1: Clarify Requirements (2 min)

**Ask these questions:**
- What's the business objective? → Increase file discovery, reduce time to find files
- What file types? → Docs, PDFs, images, slides, spreadsheets, code
- Scale? → ~100M files across all users, ~500M chunks
- Latency? → Real-time, <200ms end-to-end
- Personalized? → Yes, for logged-in users (boost recently accessed files)
- How do we define "good" results? → User clicks the file they were looking for

**Functional requirements:**
- User types a text query → system returns ranked list of files
- Works across all file types (multimodal)
- Respects access control (users only see their own files)

**Non-functional requirements:**
- p99 latency <200ms
- High availability (prioritize over consistency — stale index OK for minutes)
- Support ~1000 QPS

### Step 2: Frame as ML Task (3 min)

**ML objective:** Given a user query, predict which files the user will click/open.

**Input/Output:**
- Input: text query + user context
- Output: ranked list of files, sorted by probability of click

**ML category:** This is a **retrieval + ranking** problem.
- Stage 1: Retrieve candidates (fast, approximate) — embedding similarity
- Stage 2: Re-rank candidates (accurate, slow) — cross-encoder or learned ranker

This is analogous to Airbnb's "similar listings" — we learn file embeddings from user interaction sessions, then retrieve nearest neighbors.

### Step 3: Data Preparation (5 min)

**Available data:**

| Data | Schema | Example |
|------|--------|---------|
| Files | file_id, owner_id, type, name, content, created_at | PDF, "Q4 report", 2024-01 |
| Users | user_id, team, role, timezone | user_42, engineering |
| Interactions | user_id, file_id, action, timestamp, source | user_42, file_7, click, from search |
| Search logs | user_id, query, results_shown, results_clicked | "Q4 report", [file_7, file_12], [file_7] |

**Feature engineering:**

For embeddings (Stage 1 — retrieval):
- Extract text from each file type (OCR for images, parser for PDFs)
- Chunk into ~512 tokens with 50-token overlap
- Each chunk → embedding vector (768-dim)

For re-ranking (Stage 2):
- Query-document features: BM25 score, embedding similarity
- File features: recency, file type, popularity (# opens)
- User features: did user open this file before? same team as owner?
- Interaction features: CTR of this file for similar queries

**Constructing the training dataset:**

**For embedding model (contrastive learning):**
- Extract user file-access sessions (sequence of files opened in one sitting)
- Positive pairs: files co-accessed in same session (like Airbnb's co-clicked listings)
- Negative pairs: random files + hard negatives (same folder but not accessed)
- Eventually opened file = global context (like Airbnb's "booked listing")

```
Session: [file_1, file_3, file_7, file_12(opened)]

Positive pairs: (file_1, file_3), (file_1, file_7), (file_3, file_7)
Global context: (file_1, file_12), (file_3, file_12), (file_7, file_12)
Negative pairs: (file_1, file_random), (file_3, file_random)
Hard negatives: (file_1, file_same_folder_not_accessed)
```

**For re-ranker (from search logs):**
- Query + clicked file = positive (label 1)
- Query + shown-but-not-clicked file = negative (label 0)

### Step 4: Model Development (10 min)

**Stage 1: Embedding model (retrieval)**

Architecture: Bi-encoder (encode query and file separately)
- Text files: E5-large or BGE → 768-dim
- Images: CLIP vision encoder → same 768-dim space
- Multimodal alignment: CLIP-style contrastive training maps all modalities into shared space

Loss function (adapted from Airbnb):
```
L = Σ log σ(E_c · E_p)           # push co-accessed files together
  + Σ log σ(-E_c · E_n)          # push random files apart
  + Σ log σ(E_c · E_booked)      # push toward eventually opened file
  + Σ log σ(-E_c · E_hard_neg)   # push same-folder negatives apart
```

Why this loss?
- Random negatives alone → embeddings separate by file type/folder but not within
- Hard negatives (same folder) → forces model to learn fine-grained differences
- Global context (opened file) → optimizes for actual user goal, not just clicks

Training:
- Pre-trained base: sentence-transformers or E5
- Fine-tune on domain data (Dropbox file access sessions)
- Daily retraining to adapt to new files and interactions
- Embedding dim: 768 (can truncate to 384 with Matryoshka for speed)

**Stage 2: Re-ranker**

Architecture: Cross-encoder OR feature-based (LightGBM)

Option A — Cross-encoder:
- Input: [query + [SEP] + file_chunk] → single score
- Much more accurate (sees query and doc together via attention)
- But slow: must compute per (query, doc) pair → only on top-100

Option B — Feature-based (LambdaMART / LightGBM):
- Features: BM25 score, embedding cosine sim, file recency, file popularity, user-file affinity
- Fast, interpretable, easy to add new features
- Good when you have rich click logs

Recommendation: Start with cross-encoder, add feature-based signals later.

**Why not just one model?**
- Bi-encoder: can search 500M vectors in 10ms (pre-computed embeddings)
- Cross-encoder: 100x more accurate but would take hours on 500M vectors
- Two-stage gives you the best of both: speed + accuracy

### Step 5: Evaluation (5 min)

**Offline metrics:**

| Metric | What it measures | Target |
|--------|-----------------|--------|
| nDCG@10 | Ranking quality (graded relevance) | Main metric |
| MRR | Position of first relevant result | Navigational queries |
| Recall@100 | Does the right file appear in top-100? | Retrieval stage |
| Avg rank of opened file | How high do we rank the file user actually opened? | Like Airbnb's metric |

How to build golden eval set:
1. Sample 1000 diverse queries from search logs
2. Pool top-20 results from multiple models
3. Have 3 annotators rate (query, file) pairs: 0-3 relevance
4. Compute inter-annotator agreement (Fleiss kappa > 0.6)

**Online metrics:**

| Metric | What it measures | Why |
|--------|-----------------|-----|
| CTR | Do users click results? | Engagement |
| File open rate | Do users actually open the file? | Stronger than CTR |
| Abandonment rate | Do users give up without clicking? | Bad signal |
| Reformulation rate | Do users rephrase the query? | Bad signal |
| Session success rate | Does session end with file opened? | Business metric |

**A/B testing:**
- Interleaving: mix results from model A and B, measure click preference
- Need ~1 week for statistical significance at 95% confidence
- Guard rails: if abandonment rate increases >5%, auto-rollback

### Step 6: Serving (10 min)

**Three pipelines (like ByteByteGo/Airbnb):**

```
┌─────────────────────────────────────────────────┐
│  TRAINING PIPELINE (offline, daily)             │
│                                                 │
│  New interactions → Construct sessions →        │
│  Build pos/neg pairs → Fine-tune model →        │
│  Evaluate on golden set → Deploy if better      │
└─────────────────────────────────────────────────┘
          │ trained model
          ▼
┌─────────────────────────────────────────────────┐
│  INDEXING PIPELINE (offline/near-real-time)      │
│                                                 │
│  New/updated files → Extract text/OCR →         │
│  Chunk → Compute embeddings → Store in          │
│  vector index (HNSW) + keyword index (ES)       │
│  + metadata store (PostgreSQL)                  │
└─────────────────────────────────────────────────┘
          │ index ready
          ▼
┌─────────────────────────────────────────────────┐
│  PREDICTION PIPELINE (online, <200ms)           │
│                                                 │
│  Query → Embedding Fetcher Service              │
│    → encode query (20ms, GPU)                   │
│                                                 │
│  → Retrieval Service (parallel):                │
│    ├─ ANN search in HNSW (10ms, CPU)            │
│    ├─ BM25 search in Elasticsearch (15ms, CPU)  │
│    └─ Merge via RRF (k=60)                      │
│    → ~1000 candidates                           │
│                                                 │
│  → Re-ranking Service                           │
│    ├─ Cross-encoder on top-100 (50ms, GPU)      │
│    └─ Boost: recency, user affinity             │
│    → ~50 results                                │
│                                                 │
│  → Post-processing                              │
│    ├─ Access control filter (ACL)               │
│    ├─ Dedup (same file, different chunks)        │
│    └─ Snippet extraction + highlighting          │
│    → 10 results to user                         │
└─────────────────────────────────────────────────┘
```

**Handling cold-start (new files):**
- File uploaded → immediately chunked and embedded → added to index
- No interaction data yet → use content-based embedding only
- Like Airbnb: use embedding of geographically nearby listing → we use embedding of similar file in same folder
- After enough interactions collected, re-train incorporates the file

**Scale numbers:**
| Component | Size/Speed |
|-----------|-----------|
| Files | ~100M documents |
| Chunks | ~500M (5 chunks/doc avg) |
| Vector index | ~500M vectors x 768-dim x 4 bytes = ~1.4TB |
| HNSW search | ~10ms for top-100 |
| Embedding inference | ~20ms per query (GPU, batched) |
| Cross-encoder rerank | ~50ms for 100 candidates (GPU) |
| End-to-end | <200ms p99 |

---

## Scenario 2: Design a RAG System for Dropbox Dash

*"Design a system that answers questions about a user's files using AI."*

### Step 1: Clarify Requirements
- Input: natural language question
- Output: AI-generated answer with citations to specific files
- Must be grounded in user's files (no hallucination)
- Latency: streaming OK (first token <500ms)

### Step 2: Frame as ML Task
- ML objective: generate accurate, cited answer given retrieved context
- This is retrieval + generation (not just retrieval + ranking)
- Category: RAG (Retrieval-Augmented Generation)

### Step 3: Data Preparation
- Reuse the same embedding index from Scenario 1
- Chunk size: 512 tokens (balance: too small = no context, too big = noise)
- For evaluation: curate QA pairs (question + correct answer + source file)

### Step 4: Model Development

**Retrieval (same as Scenario 1):**
- Hybrid: BM25 + dense → RRF → top-k chunks
- Cross-encoder rerank → top-5 chunks

**Generation:**
- LLM (Claude/GPT-4) with prompt:
```
Given these document excerpts, answer the user's question.
Cite your sources using [1], [2], etc.
If the answer is not in the documents, say "I don't know."

[1] {chunk_1_text} (from: file_name_1)
[2] {chunk_2_text} (from: file_name_2)
...

Question: {user_question}
```

**Key decisions:**

| Decision | Options | Choice | Why |
|----------|---------|--------|-----|
| k (chunks) | 3 / 5 / 10 | 5 | Balance context length vs noise |
| LLM | GPT-4 / Claude / Llama | Depends on budget | GPT-4 best quality, Llama cheapest |
| Streaming | Yes / No | Yes | Better UX, first token <500ms |

### Step 5: Evaluation
- **Retrieval**: Recall@5 (is the right chunk in top 5?)
- **Faithfulness**: does answer only use info from chunks? (LLM-as-judge)
- **Relevance**: does answer address the question? (human eval)
- **Citation accuracy**: are citations correct? (automated check)
- **Online**: thumbs up/down, follow-up question rate

### Step 6: Serving
- Same prediction pipeline as Scenario 1 for retrieval
- Add LLM service: receives top-5 chunks + question → streams answer
- Cache: frequent questions with same file context → cache response (TTL 1hr)
- Hallucination guard: if all retrieval scores < threshold → "I don't know"

---

## Scenario 3: Improve Search Ranking Quality

*"Our search results aren't great. What would you do?"*

Follow ByteByteGo framework but focus on diagnosis:

### Step 1: Measure current quality
- Compute nDCG@10, MRR on golden eval set
- Segment failures: which query types fail? (keyword, NL, multimodal)

### Step 2: Diagnose — is it retrieval or ranking?
- Compute Recall@1000: is the right file even retrieved?
  - NO → retrieval problem (improve embeddings, add BM25, query expansion)
  - YES → ranking problem (improve re-ranker, add features)

### Step 3: Improve retrieval
- Add BM25 if only using dense → hybrid search with RRF
- Fine-tune embeddings on domain data (file access sessions)
- Hard negative mining: same-folder files not accessed
- Query expansion: LLM rewrites query with synonyms

### Step 4: Improve ranking
- Add cross-encoder re-ranker on top-100
- Feature-based ranker (LightGBM): BM25 score, cosine sim, recency, popularity, user affinity
- Train on click logs: clicked = positive, shown-not-clicked = negative

### Step 5: Iterate
- A/B test each change independently
- Monitor online metrics: CTR, abandonment, session success
- Feedback loop: click data → retrain embeddings → redeploy

---

## Key Follow-Up Questions & Answers

**Q: How do you handle new file types (e.g., audio)?**
> Add encoder (Whisper for audio → text → embed). Same retrieval infra.
> Like Airbnb adding a new listing type — just need a new feature extractor.

**Q: How do you handle file updates?**
> Event-driven: file change → re-chunk → re-embed → update index.
> Stale reads OK for minutes (availability > consistency).

**Q: How do you handle access control?**
> Post-retrieval filtering by user ACL. Never leak files.
> Option: pre-filter during ANN search with metadata constraints.

**Q: Bi-encoder vs cross-encoder?**
> Bi-encoder: encode separately, fast, stage 1 (500M vectors in 10ms).
> Cross-encoder: encode together, accurate, stage 2 (100 candidates in 50ms).
> Bi-encoder alone: good recall. Cross-encoder: good precision. Need both.

**Q: How do you get training data?**
> Click logs: (query, clicked_file) = positive pair.
> Hard negatives: BM25 top results not clicked.
> File access sessions: co-accessed files = positive pairs (Airbnb-style).
> Human annotations: for golden eval set only (expensive).

**Q: How to handle personalization?**
> Add user signals to re-ranker (not retrieval stage).
> Features: recently opened files, team, frequently accessed folders.
> Like Airbnb's in-session personalization.

**Q: What would you do first 30 days?**
> Week 1: Understand codebase, existing metrics, data pipelines.
> Week 2: Reproduce current metrics, identify biggest failure modes.
> Week 3: Propose 1 high-impact improvement (e.g., add cross-encoder).
> Week 4: Implement, offline eval, launch A/B test.

---

## Quick Reference: ByteByteGo vs Dropbox Mapping

| ByteByteGo (Airbnb) | Dropbox Dash |
|---------------------|-------------|
| Listing | File / document chunk |
| Listing embedding (word2vec) | File embedding (E5/CLIP) |
| User click session | User file access session |
| Co-clicked listings = positive | Co-accessed files = positive |
| Eventually booked = global context | Eventually opened = global context |
| Random negative | Random file negative |
| Same-region hard negative | Same-folder hard negative |
| Nearest neighbor service (ANN) | HNSW / Faiss |
| Re-ranking: price, city filters | Re-ranking: file type, ACL, recency |
| Offline: avg rank of booked listing | Offline: nDCG@10, MRR |
| Online: CTR, session book rate | Online: CTR, file open rate, session success |