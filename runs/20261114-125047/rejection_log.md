# Rejection log - Introduction to RAG (Retrieval-Augmented Generation)
Run `20261114-125047` | final status: **shipped** | attempts: 2

## Attempt 1 - REJECTED
**Checks that failed:**
- **L2 - Language suits a non-native English reader** (llm)
  - Why: The lesson uses the English idiom 'misses the point', which is unsuitable for a learner with limited English vocabulary.
  - Evidence: "too little text misses the point, and too much text confuses the model."
  - Fix asked: Replace 'misses the point' with plain language, such as 'leaves out important details'.

## Attempt 2 - PASSED
**What the writer changed on this retry:**
- Replaced the idiom "misses the point" in the "Where it can go wrong" section with plain language ("leaves out important details") to match the non-native English reader requirement.
_(diff: +1 / -1 lines, similarity 0.99)_
