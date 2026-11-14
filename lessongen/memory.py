"""Persistent memory across runs (plain files, so it is easy to inspect, diff and commit)."""
import json
from datetime import datetime
from pathlib import Path


class Memory:
    def __init__(self, d: Path):
        self.d = Path(d)
        self.d.mkdir(exist_ok=True, parents=True)
        self.stats_p = self.d / "stats.json"
        self.fail_p = self.d / "failure_log.jsonl"
        self.guid_p = self.d / "guidance.json"
        self.fb_p = self.d / "human_feedback.jsonl"
        self.sugg_p = self.d / "rubric_suggestions.md"

    # ---- stats & failures ----
    def stats(self):
        if self.stats_p.exists():
            return json.loads(self.stats_p.read_text())
        return {"runs": 0, "first_attempt_fails": {}, "total_fails": {}, "retries_used": 0, "shipped": 0, "needs_review": 0}

    def record_run(self, run_id, log, status):
        s = self.stats()
        s["runs"] += 1
        s["retries_used"] += len(log) - 1
        s["shipped" if status == "shipped" else "needs_review"] += 1
        with self.fail_p.open("a") as f:
            for entry in log:
                for r in entry["failed_checks"]:
                    s["total_fails"][r["id"]] = s["total_fails"].get(r["id"], 0) + 1
                    if entry["attempt"] == 1:
                        s["first_attempt_fails"][r["id"]] = s["first_attempt_fails"].get(r["id"], 0) + 1
                    f.write(json.dumps({"run": run_id, "attempt": entry["attempt"], "id": r["id"],
                                        "reason": r["reason"], "evidence": r["evidence"]}) + "\n")
        self.stats_p.write_text(json.dumps(s, indent=2))

    def recent_failures(self, check_id, n=5):
        if not self.fail_p.exists():
            return []
        rows = [json.loads(l) for l in self.fail_p.read_text().splitlines() if l.strip()]
        return [r for r in rows if r["id"] == check_id][-n:]

    # ---- learned guidance ----
    def rules(self):
        return json.loads(self.guid_p.read_text()) if self.guid_p.exists() else []

    def add_rule(self, check_id, rule):
        rules = self.rules()
        if any(r["check_id"] == check_id for r in rules):
            return False
        rules.append({"check_id": check_id, "rule": rule, "created": datetime.now().isoformat(timespec="seconds")})
        self.guid_p.write_text(json.dumps(rules[-10:], indent=2))  # cap: prompt must not grow forever
        return True

    # ---- human feedback ----
    def add_feedback(self, note):
        with self.fb_p.open("a") as f:
            f.write(json.dumps({"ts": datetime.now().isoformat(timespec="seconds"), "note": note}) + "\n")

    def feedback(self, n=5):
        if not self.fb_p.exists():
            return []
        return [json.loads(l)["note"] for l in self.fb_p.read_text().splitlines() if l.strip()][-n:]

    def guidance_text(self):
        parts = [f"- {r['rule']}" for r in self.rules()]
        parts += [f"- (human reviewer note) {n}" for n in self.feedback()]
        return "\n".join(parts)
