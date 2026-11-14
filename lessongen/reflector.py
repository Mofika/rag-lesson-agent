"""Self-evolving step. Learns prompt rules automatically; only SUGGESTS rubric changes (human approves)."""
from .memory import Memory

REFLECT_SYSTEM = ("You improve a lesson-writing prompt. Given repeated failure reasons for ONE quality check, write ONE short "
                  "imperative rule (max 25 words) the writer must follow to avoid it. Output only the rule.")


def evolve(mem: Memory, rubric, llm, model, threshold=2):
    s = mem.stats()
    titles = {c["id"]: c["title"] for c in rubric["checks"]}
    learned = []
    for cid, n in s["first_attempt_fails"].items():
        if n >= threshold and not any(r["check_id"] == cid for r in mem.rules()):
            ev = "\n".join(f"- {r['reason']} | {r['evidence'][:120]}" for r in mem.recent_failures(cid))
            rule = llm.complete("reflector", REFLECT_SYSTEM, f"Check {cid}: {titles.get(cid, cid)}\nFailures:\n{ev}", model, 200).strip()
            if rule and mem.add_rule(cid, rule):
                learned.append((cid, rule))
    # rubric health signals -> written for a human, never auto-applied (avoids the system loosening its own bar)
    notes = []
    runs = s["runs"]
    for c in rubric["checks"]:
        f = s["total_fails"].get(c["id"], 0)
        if runs >= 5 and f / runs >= 0.6:
            notes.append(f"- {c['id']} fails in {f}/{runs} runs: threshold may be too strict or wording ambiguous. Review it.")
        if runs >= 10 and f == 0:
            notes.append(f"- {c['id']} never failed in {runs} runs: possibly too easy; consider tightening.")
    if notes:
        mem.sugg_p.write_text("# Rubric suggestions (need human approval)\n\n" + "\n".join(notes) + "\n")
    return learned
