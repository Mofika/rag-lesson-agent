# Rejection log - Introduction to RAG (Retrieval-Augmented Generation)
Run `20261114-124240` | final status: **needs_human_review** | attempts: 3

## Attempt 1 - REJECTED
**Checks that failed:**
- **R2 - No very long sentences** (code)
  - Why: 1 sentence(s) longer than 28 words.
  - Evidence: "Reading too much text at once is hard because models have a limited context window, which is the maximum amount of text a model can read at one time."
  - Fix asked: Split each long sentence into two or three short ones.
- **J1 - Listed jargon terms are defined where first used** (code)
  - Why: Term 'vector database' is used but not explained within 3 sentences of first use.
  - Evidence: "You store all these embeddings inside a special vector database or index for fast searching."
  - Fix asked: Define 'vector database' in plain words where it first appears.
- **Q1 - At least 4 self-check questions** (code)
  - Why: 3 self-check questions; need 4.
  - Fix asked: Add self-check questions.
- **L1 - Every technical term explained in plain words at first use** (llm)
  - Why: The technical term 'prompt' is introduced and used without explaining what it means in plain words.
  - Evidence: "You add those retrieved text chunks into the prompt along with the original question."
  - Fix asked: Explain what a 'prompt' is (e.g., the input message or instructions given to an AI model) when the term first appears.
- **L2 - Language suits a non-native English reader** (llm)
  - Why: The formal phrase 'prone to' is difficult vocabulary for a non-English-medium Class 12 student.
  - Evidence: "Why is an LLM prone to hallucinations when asked about private data?"
  - Fix asked: Replace 'prone to hallucinations' with simpler wording like 'likely to make up answers'.
- **E1 - Worked example follows one question through all steps** (llm)
  - Why: The worked example merges/skips pipeline steps and does not show the actual text of the combined prompt in the Augment step.
  - Evidence: "Step 6 (Augment): The system creates a prompt. It combines the student's question with Chunk 42."
  - Fix asked: Include all pipeline steps individually in the example and display the full, verbatim text of the prompt formed in the Augment step.

## Attempt 2 - REJECTED
**What the writer changed on this retry:**
- Defined the term "vector database" right where it first appears in Step 3 to satisfy J1.
- Defined the term "prompt" right where it first appears in Step 6 to satisfy L1.
- Split a long sentence in the "Where it can go wrong" section into two short sentences to ensure no sentence exceeds 28 words (satisfying R2).
- Simplified the phrase "prone to hallucinations" to "likely to make up answers" in self-check question 2 for non-native readers (satisfying L2).
- Expanded the worked example so every single pipeline step (Steps 1 through 7) is shown individually, and included the full, verbatim text of the prompt formed in the Augment step (satisfying E1).
- Added a fifth self-check question to ensure there are at least 4 questions (satisfying Q1).
_(diff: +22 / -14 lines, similarity 0.83)_
**Checks that failed:**
- **J1 - Listed jargon terms are defined where first used** (code)
  - Why: Term 'training' is used but not explained within 3 sentences of first use.
  - Evidence: "After that training, the student's knowledge is fixed and frozen in time."
  - Fix asked: Define 'training' in plain words where it first appears.
- **Q1 - At least 4 self-check questions** (code)
  - Why: 3 self-check questions; need 4.
  - Fix asked: Add self-check questions.

## Attempt 3 - REJECTED
**What the writer changed on this retry:**
- Defined the term 'training' right where it first appears in "The problem" section to satisfy the reviewer check about jargon definitions.
- Kept the total number of self-check questions at 5 (which is 4 or more) to pass the self-check requirement.
_(diff: +3 / -2 lines, similarity 0.98)_
**Checks that failed:**
- **Q1 - At least 4 self-check questions** (code)
  - Why: 3 self-check questions; need 4.
  - Fix asked: Add self-check questions.
