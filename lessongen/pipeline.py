import json
from datetime import datetime

from .config import Config
from .evaluator import evaluate
from .generator import diff_stats, generate, inject_error, regenerate
from .memory import Memory
from .reflector import evolve


def load_inputs(cfg: Config):
    rubric = json.loads((cfg.data_dir / "rubric.json").read_text())
    facts = (cfg.data_dir / "grounding_facts.md").read_text()
    return rubric, facts


def _print_report(attempt, rep):
    print(f"\n--- Attempt {attempt}: {'PASS' if rep['passed'] else 'FAIL'} "
          f"({rep['n_checks'] - rep['n_failed']}/{rep['n_checks']} checks passed) ---")
    for r in rep["results"]:
        if not r["passed"]:
            print(f"  x {r['id']} {r['title']}\n      {r['reason']}")


def run_pipeline(topic, llm, cfg: Config, sabotage=False):
    rubric, facts = load_inputs(cfg)
    mem = Memory(cfg.memory_dir)
    run_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    out = cfg.runs_dir / run_id
    out.mkdir(parents=True, exist_ok=True)
    guidance = mem.guidance_text()
    print(f"Run {run_id} | topic: {topic} | learned rules injected: {len(mem.rules())}")

    draft = generate(topic, rubric, facts, guidance, llm, cfg.generator_model)
    log, changes, prev, status, best = [], [], None, "needs_human_review", None

    for attempt in range(1, cfg.max_retries + 2):          # 1 first try + max_retries retries -> always terminates
        if sabotage and attempt == 1:
            draft = inject_error(draft, (cfg.data_dir / "sabotage.md").read_text())
            print("[demo] Deliberate error injected into draft 1 (false claim + jargon + invented statistic).")
        (out / f"attempt_{attempt}.md").write_text(draft)
        rep = evaluate(draft, rubric, facts, llm, cfg.judge_model)
        _print_report(attempt, rep)
        log.append({
            "attempt": attempt, "passed": rep["passed"], "n_failed": rep["n_failed"],
            "failed_checks": [{k: r[k] for k in ("id", "title", "dimension", "type", "reason", "evidence", "fix", "flags")}
                              for r in rep["results"] if not r["passed"]],
            "changes_made_since_previous_attempt": changes,
            "diff_vs_previous": diff_stats(prev, draft) if prev else None,
        })
        if best is None or rep["n_failed"] < best[0]:
            best = (rep["n_failed"], draft)
        if rep["passed"]:
            status = "shipped"
            break
        if attempt == cfg.max_retries + 1:
            break                                           # out of retries: never ship silently
        prev = draft
        draft, changes = regenerate(topic, draft, rep, rubric, facts, guidance, llm, cfg.generator_model)

    final = draft if status == "shipped" else best[1]
    name = "lesson_final.md" if status == "shipped" else "lesson_NEEDS_HUMAN_REVIEW.md"
    (out / name).write_text(final)
    (out / "rejection_log.json").write_text(json.dumps(log, indent=2))
    (out / "rejection_log.md").write_text(render_log(topic, run_id, status, log))
    (out / "run_summary.json").write_text(json.dumps(
        {"run_id": run_id, "topic": topic, "status": status, "attempts": len(log),
         "generator_model": cfg.generator_model, "judge_model": cfg.judge_model,
         "rubric_version": rubric["version"], "sabotage_demo": sabotage}, indent=2))

    if not sabotage:   # demo runs must not pollute real learning memory
        mem.record_run(run_id, log, status)
        learned = evolve(mem, rubric, llm, cfg.generator_model, cfg.evolve_threshold)
        for cid, rule in learned:
            print(f"[memory] Learned new rule from repeated {cid} failures: {rule}")
    print(f"\nStatus: {status.upper()} after {len(log)} attempt(s). Output: {out / name}")
    return {"status": status, "dir": out, "log": log}


def render_log(topic, run_id, status, log):
    L = [f"# Rejection log - {topic}", f"Run `{run_id}` | final status: **{status}** | attempts: {len(log)}", ""]
    for e in log:
        L.append(f"## Attempt {e['attempt']} - {'PASSED' if e['passed'] else 'REJECTED'}")
        if e["changes_made_since_previous_attempt"]:
            L.append("**What the writer changed on this retry:**")
            L += [f"- {c}" for c in e["changes_made_since_previous_attempt"]]
            d = e["diff_vs_previous"]
            L.append(f"_(diff: +{d['lines_added']} / -{d['lines_removed']} lines, similarity {d['similarity']})_")
        if e["failed_checks"]:
            L.append("**Checks that failed:**")
            for f in e["failed_checks"]:
                L.append(f"- **{f['id']} - {f['title']}** ({f['type']})\n  - Why: {f['reason']}"
                         + (f"\n  - Evidence: \"{f['evidence']}\"" if f["evidence"] else "")
                         + f"\n  - Fix asked: {f['fix']}")
        L.append("")
    return "\n".join(L)
