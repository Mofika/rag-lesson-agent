"""LLM judge for the semantic checkpoints. Separate model + separate prompt from the generator.
Anti-hallucination for the judge itself: every verdict must carry a verbatim quote from the lesson,
and code verifies that the quote really exists."""
import json
import re

from .llm import extract_json

JUDGE_SYSTEM = """You are a strict content QA reviewer. You are NOT the writer.
Your job is to find reasons to FAIL a lesson. Pass a check only if it is clearly satisfied.
Rules:
- Each check is HARD pass/fail. No partial credit, no 'mostly'.
- Judge ONLY against the rubric text and GROUNDING FACTS given. Do not use outside knowledge to approve a claim.
- For every check give "evidence_quote": an EXACT, verbatim snippet (<=25 words) copied from the lesson that
  supports your verdict (for a missing item, quote the closest passage or use "" ).
- "reason": one short sentence. "fix": one concrete instruction for the writer (empty if pass).
- Output ONLY JSON: {"results":[{"id":"A1","pass":true|false,"evidence_quote":"...","reason":"...","fix":"..."}]}
- Return one result for EVERY check id listed."""


def _norm(s):
    return re.sub(r"\s+", " ", re.sub(r"[*_`#>]", "", s)).strip().lower()


def build_prompt(lesson, rubric, facts):
    llm_checks = [c for c in rubric["checks"] if c["type"] == "llm"]
    lines = "\n".join(f"- {c['id']} | {c['title']}: {c['pass_condition']}" for c in llm_checks)
    return (f"AUDIENCE: {rubric['audience']}\n\nGROUNDING FACTS:\n{facts}\n\nCHECKS:\n{lines}\n\n"
            f"LESSON TO REVIEW:\n<<<\n{lesson}\n>>>")


def run_judge(lesson, rubric, facts, llm, model):
    prompt = build_prompt(lesson, rubric, facts)
    data = None
    for _ in range(2):  # one retry if the JSON is malformed
        raw = llm.complete("judge", JUDGE_SYSTEM, prompt, model, max_tokens=4000)
        try:
            data = extract_json(raw)
            break
        except (json.JSONDecodeError, ValueError):
            continue
    got = {r.get("id"): r for r in (data or {}).get("results", [])}
    nlesson = _norm(lesson)
    out = []
    for c in (c for c in rubric["checks"] if c["type"] == "llm"):
        r = got.get(c["id"])
        if r is None:  # fail closed: a missing verdict is a failure
            out.append({"id": c["id"], "title": c["title"], "dimension": c["dimension"], "type": "llm",
                        "passed": False, "reason": "Judge returned no verdict (fail-closed).",
                        "evidence": "", "fix": "Re-run evaluation.", "flags": ["no_verdict"]})
            continue
        quote = r.get("evidence_quote", "") or ""
        flags = []
        if quote and _norm(quote) not in nlesson:
            flags.append("quote_not_found_in_lesson")
        passed = bool(r.get("pass"))
        out.append({"id": c["id"], "title": c["title"], "dimension": c["dimension"], "type": "llm",
                    "passed": passed, "reason": r.get("reason", ""), "evidence": quote,
                    "fix": r.get("fix", ""), "flags": flags})
    return out
