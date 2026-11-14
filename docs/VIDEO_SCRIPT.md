# Loom plan (target 16-18 min, face visible)

| Time | What to show | What to say |
|---|---|---|
| 0:00-1:30 | Face on camera, intro | Who you are, the problem: "generating content is easy, deciding it is good enough to ship is the hard part." |
| 1:30-5:00 | Whiteboard / README diagram | Walk the loop: generator -> evaluator (code + LLM) -> retry cap -> memory. Explain WHY: hybrid evaluator, separate judge, grounding file, fail-closed, hard pass/fail. |
| 5:00-7:30 | Open `rubric.json` + `checks_code.py` | 6 dimensions, 18 checks. Show one code check and one LLM check. Explain "no partial credit". |
| 7:30-11:00 | Terminal: `python run.py generate` | Run end-to-end. Narrate each attempt, the pass/fail list, then open `runs/<id>/lesson_final.md` and `rejection_log.md`. |
| 11:00-14:30 | **Deliberate error**: `python run.py generate --sabotage` | Say what you injected (false claim: "RAG retrains the model", fake 99.9% stat, jargon wall). Show A1/A2/L2 failing with evidence quotes, the retry, the "changes made" list, then pass. Also run `evaluate --file data/sample_lesson.md --inject-error`. |
| 14:30-16:30 | `memory/` folder, `python run.py evolve`, `feedback` | Show failure_log, learned rule injected into next prompt, rubric_suggestions (human approval). Explain why demo runs don't write memory. |
| 16:30-18:00 | Face on camera, close | Trade-offs and limitations (README section), what you'd do next. |

Tips: do 2-3 real runs BEFORE recording so memory has data to show. Keep API key off-screen.
