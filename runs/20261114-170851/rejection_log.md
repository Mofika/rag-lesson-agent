# Rejection log - Introduction to RAG (Retrieval-Augmented Generation)
Run `20261114-170851` | final status: **needs_human_review** | attempts: 3

## Attempt 1 - REJECTED
**Checks that failed:**
- **A1 - No factual errors** (llm)
  - Why: The lesson falsely claims RAG retrains model weights, directly contradicting Grounding Fact F6.
  - Evidence: "RAG permanently retrains the LLM's weights every time a user asks a question, so the model always becomes smarter."
  - Fix asked: Remove the claim that RAG retrains the model's weights and state clearly that weights are not changed.
- **A2 - No invented specifics** (llm)
  - Why: The lesson includes an invented statistic (99.9% accuracy) that is not in the Grounding Facts.
  - Evidence: "RAG reaches 99.9% accuracy on all tasks."
  - Fix asked: Remove the 99.9% accuracy statistic and any non-grounded technical claims.
- **L1 - Every technical term explained in plain words at first use** (llm)
  - Why: Multiple technical terms in the Extra note section are used without any plain-language explanation.
  - Evidence: "latent manifolds via bi-encoder cosine-similarity ANN indexing with HNSW graphs"
  - Fix asked: Remove or explain all advanced technical jargon introduced in the Extra note section.
- **L2 - Language suits a non-native English reader** (llm)
  - Why: The text uses overly formal vocabulary and idiomatic phrasing unsuitable for a non-English-medium 12th-grade graduate.
  - Evidence: "ameliorate the aforementioned stochastic parroting"
  - Fix asked: Remove formal academic terms like 'ameliorate' and 'aforementioned', and replace idioms like 'bold face' with simple words.

## Attempt 2 - REJECTED
**What the writer changed on this retry:**
- Removed the entire "Extra note" section containing ungrounded claims (weight retraining, 99.9% accuracy) and advanced technical jargon ("latent manifolds", "HNSW graphs", "ameliorate") to fix factual errors, remove ungrounded statistics, and ensure appropriate language for non-native readers.
- Replaced the idiom "bold face" with "bold voice" to keep the text simple and clear for learners.
_(diff: +21 / -24 lines, similarity 0.68)_
**Checks that failed:**
- **L1 - Every technical term explained in plain words at first use** (llm)
  - Why: The technical term 'model weights' is introduced and used without any plain-language explanation.
  - Evidence: "does not change the model weights."
  - Fix asked: Explain what 'model weights' means in simple words upon first use, or remove the term.

## Attempt 3 - REJECTED
**What the writer changed on this retry:**
- Added a plain-language definition for the technical term "model weights" right where it first appears in the "What is RAG?" section to fix the failed check.
_(diff: +1 / -1 lines, similarity 0.99)_
**Checks that failed:**
- **L1 - Every technical term explained in plain words at first use** (llm)
  - Why: The technical term 'index' is introduced without any simple-word explanation.
  - Evidence: "you update the documents and index."
  - Fix asked: Explain what an index is when it first appears, or change 'documents and index' to 'documents and stored chunks'.
- **L2 - Language suits a non-native English reader** (llm)
  - Why: The acronym 'AI' is used without being spelled out or explained first.
  - Evidence: "solves the main limits of AI models."
  - Fix asked: Spell out and explain acronyms like AI (Artificial Intelligence) upon first use.
