import difflib

GEN_SYSTEM = """You are an expert teacher who writes beginner lessons for Indian learners.
AUDIENCE: {audience}.
Write ONE standalone lesson in Markdown. Rules:
- Short, plain sentences (aim for 8-14 words). Everyday words. No idioms, slang, or Latin abbreviations (e.g., i.e., etc.).
- Explain every technical term in plain words, in the same place where it first appears.
- Required sections (use these words in the headings): What you will learn, the problem, What is <topic>?, Why it matters,
  How it works (step by step), A full example, Where it can go wrong, Words to know, Check yourself.
- Teach with a relatable everyday analogy and at least one full worked example that follows ONE question through every step.
- Use ONLY the facts in GROUNDING FACTS for technical claims. Do not invent numbers, studies, or product claims. Mark made-up example data as made up.
- Cover every MUST_COVER item.
- The "Check yourself" section must have at least 5 numbered questions, and EVERY question must end with a question mark (?).
- Define each of these terms in the same sentence or the very next sentence where it FIRST appears, using a plain cue such as "means", "is called", or "is a": {jargon}.
- 700-1200 words. Output only the lesson.
{memory}"""

CHANGES_MARK = "=====CHANGES====="


def build_system(rubric, guidance):
    mem = f"\nLEARNED RULES FROM PAST RUNS (follow them):\n{guidance}" if guidance else ""
    jargon = next((c["params"]["terms"] for c in rubric["checks"] if c["id"] == "J1"), [])
    return GEN_SYSTEM.format(audience=rubric["audience"], memory=mem, jargon=", ".join(jargon))


def generate(topic, rubric, facts, guidance, llm, model):
    user = f"TOPIC: {topic}\n\nGROUNDING FACTS:\n{facts}\n\nWrite the lesson now."
    return llm.complete("generator", build_system(rubric, guidance), user, model, max_tokens=4000).strip()


def regenerate(topic, draft, report, rubric, facts, guidance, llm, model):
    fails = [r for r in report["results"] if not r["passed"]]
    fb = "\n".join(f"- [{r['id']}] {r['title']}\n  why failed: {r['reason']}\n  evidence: {r['evidence']}\n  fix: {r['fix']}"
                   for r in fails)
    user = (f"TOPIC: {topic}\n\nGROUNDING FACTS:\n{facts}\n\nPREVIOUS DRAFT:\n<<<\n{draft}\n>>>\n\n"
            f"FAILED CHECKS (a reviewer rejected the draft for these reasons):\n{fb}\n\n"
            "Rewrite the lesson so EVERY failed check passes. Keep all parts that already passed unchanged where possible. "
            f"After the lesson, add a line {CHANGES_MARK} followed by a short bullet list of what you changed and why.")
    raw = llm.complete("generator", build_system(rubric, guidance), user, model, max_tokens=4500)
    if CHANGES_MARK in raw:
        lesson, ch = raw.split(CHANGES_MARK, 1)
        changes = [l.strip("-* ").strip() for l in ch.strip().splitlines() if l.strip()]
    else:
        lesson, changes = raw, ["(generator did not report changes)"]
    return lesson.strip(), changes


def diff_stats(a, b):
    sm = difflib.SequenceMatcher(None, a.splitlines(), b.splitlines())
    added = removed = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag in ("replace", "delete"):
            removed += i2 - i1
        if tag in ("replace", "insert"):
            added += j2 - j1
    return {"lines_added": added, "lines_removed": removed, "similarity": round(sm.ratio(), 2)}


def inject_error(lesson, sabotage_text):
    """Deliberate error for the demo: a false claim + jargon wall + invented statistic."""
    marker = "## Words to know"
    return lesson.replace(marker, sabotage_text + marker, 1) if marker in lesson else lesson + "\n\n" + sabotage_text
