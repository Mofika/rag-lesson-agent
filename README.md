# Self-Evaluating Lesson Content Generator

An agentic **generate → evaluate → regenerate** loop that writes a beginner lesson, judges it against a
hard pass/fail rubric, and only ships it if every checkpoint passes. Topic for submission: **Introduction to RAG**.
Target learner: 12th-grade graduate from India, limited English, no AI background.

## Architecture

```
            ┌──────────── memory/ (persists across runs) ────────────┐
            │ guidance.json  stats.json  failure_log.jsonl  feedback │
            └───────▲────────────────────────────────────▲───────────┘
                    │ learned rules injected             │ failures logged
 topic ─► GENERATOR ─► draft ─► EVALUATOR ──pass──► ship lesson_final.md
 (Sonnet)     ▲                 ├─ 8 code checks   │
              │                 └─ 10 LLM-judge    fail (≤ MAX_RETRIES=2)
              │                    checks (Opus)    │
              └──── reasons + evidence + fix ◄──────┘
                                                    └─ retries exhausted ► lesson_NEEDS_HUMAN_REVIEW.md
                          every run ► rejection_log.md / .json
```

| Component | File | Role |
|---|---|---|
| Rubric | `data/rubric.json` | 18 hard pass/fail checkpoints across 6 dimensions |
| Grounding facts | `data/grounding_facts.md` | The only source of truth the judge uses |
| Generator | `lessongen/generator.py` | Writes / rewrites the lesson using feedback |
| Code checks | `lessongen/checks_code.py` | Readability, structure, jargon, length, glossary, questions |
| LLM judge | `lessongen/judge.py` | Semantic checks: accuracy, grounding, examples, flow |
| Loop | `lessongen/pipeline.py` | Orchestration, retry cap, logs |
| Memory | `lessongen/memory.py` | Stats, failure log, learned rules, human feedback |
| Reflector | `lessongen/reflector.py` | Turns repeated failures into prompt rules |

## Setup

```bash
git clone <your-repo> && cd rag-lesson-agent
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # then add a key. FREE option: Google Gemini key from https://aistudio.google.com/apikey (no card)
```

## Models / providers
Set `LLM_PROVIDER` in `.env`: `gemini` (free tier, default in `.env.example`), `anthropic`, or `openai_compat` (Groq, OpenRouter, local Ollama).
Generator and judge use different models where the provider allows it (see design decision 2).

## Run

```bash
python run.py generate                         # real run: generate -> evaluate -> regenerate
python run.py generate --sabotage              # DEMO: injects a deliberate error into draft 1; watch it get rejected & fixed
python run.py evaluate --file data/sample_lesson.md --inject-error   # DEMO: evaluator alone catches an error
python run.py feedback --note "Use a railway ticket example"          # human feedback -> memory
python run.py evolve                           # learn rules from failure log
python run.py generate --mock                  # offline dry run (plumbing only, no API key)
pytest -q                                      # tests
```

Outputs go to `runs/<timestamp>/`: `attempt_N.md`, `lesson_final.md` (or `lesson_NEEDS_HUMAN_REVIEW.md`),
`rejection_log.md/.json`, `run_summary.json`.

## The rubric (all must pass, no partial credit)

| Dimension | Code checks | LLM-judge checks |
|---|---|---|
| Accurate & grounded | – | A1 no factual errors · A2 no invented specifics · A3 correct pipeline order |
| Beginner-friendly language | R1 FK grade ≤ 8 & avg sentence ≤ 15 words · R2 no sentence > 28 words · R4 ≤ 4% long words | L2 suits non-native reader (no idioms, "e.g.", rare words) |
| Teaches by example | – | E1 worked example through every step · E2 accurate, relatable analogy |
| Clear, no unexplained jargon | J1 listed terms defined within 3 sentences · G1 glossary ≥ 6 | L1 every technical term explained at first use |
| Covers key points | R3 length 600–1400 words | C1 what/why/how · C2 every MUST_COVER item |
| Coherent flow | S1 required sections · Q1 ≥ 4 self-check questions | F1 simple→complex, nothing used before taught |

## Design decisions and trade-offs

1. **Hybrid evaluator (code + LLM).** Anything measurable is a code check: free, repeatable, cannot be argued with.
   Only semantic things (is this claim true? is this analogy misleading?) go to an LLM. Trade-off: code heuristics
   (syllable counter, definition-cue regex) are approximate, so they are tuned conservatively and unit-tested.
2. **Separate judge model and prompt.** Generator is Sonnet; judge is a stronger model (Opus) with an adversarial
   prompt ("find reasons to FAIL"). A model grading its own output tends to be lenient. Trade-off: higher cost per run.
3. **Grounding file, not model memory.** The judge may only approve claims that match `grounding_facts.md`.
   This makes "accurate" checkable and auditable. Trade-off: the facts file must be curated by a human (done once per topic).
4. **Judge cannot hallucinate evidence.** Each verdict needs a verbatim quote; code verifies the quote exists in the lesson
   (`quote_not_found_in_lesson` flag). A missing verdict **fails closed**.
5. **Hard binary checks.** No scores means no threshold-gaming and a clear, loggable reason for every rejection.
6. **All checks run every attempt**, so one retry can fix every problem together rather than one per retry.
7. **Targeted regeneration.** The writer gets the previous draft + each failure's reason, evidence quote and fix, and must
   keep passing parts. It also reports what it changed, which feeds the rejection log (plus a line-diff for proof).
8. **Guaranteed termination, no silent shipping.** `MAX_RETRIES=2` (3 attempts total). If still failing, output is named
   `lesson_NEEDS_HUMAN_REVIEW.md`, picking the attempt with the fewest failures.

## Self-evolving + memory

- Every run appends failures to `memory/failure_log.jsonl` and counts them in `stats.json`.
- When one check fails on the **first attempt in ≥ 2 runs**, the reflector writes a short imperative rule
  (e.g. "Define every term in the same sentence it first appears") into `guidance.json`. These rules are injected into
  the generator's system prompt on every later run. The cap is 10 rules, so the prompt cannot grow forever.
- Human notes (`run.py feedback`) are also injected.
- **Rubric changes are suggested, not applied.** If a check fails in ≥ 60% of runs, or never fails over 10 runs,
  `rubric_suggestions.md` is written for a human. The system must not loosen its own quality bar (Goodhart risk).
- Demo runs (`--sabotage`) do not write to memory, so deliberate errors don't teach the system bad habits.

## Known limitations / next steps
- Rule effectiveness isn't yet tracked (compare first-attempt fail rate before vs after a rule; retire rules that don't help).
- Readability formula is English-generic; a custom word-frequency list for Indian ESL learners would be better.
- Judge noise: for high stakes, run the judge twice and require agreement.
- Add a small human-labeled set of good/bad lessons to measure the evaluator itself (precision/recall).
- Faithfulness to sources is only as good as the grounding file; add retrieval from real docs for new topics.

## Note on sample content
`data/sample_lesson.md` is a hand-checked reference lesson used for tests and `--mock`. Your real submission lesson
and rejection log should come from `python run.py generate` (see `runs/`).
