import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from lessongen.checks_code import run_code_checks  # noqa: E402
from lessongen.config import Config  # noqa: E402
from lessongen.llm import MockLLM  # noqa: E402
from lessongen.pipeline import run_pipeline  # noqa: E402

RUBRIC = json.loads((ROOT / "data/rubric.json").read_text())
GOOD = (ROOT / "data/sample_lesson.md").read_text()


def failed(md):
    return {r["id"] for r in run_code_checks(md, RUBRIC) if not r["passed"]}


def test_good_lesson_passes_code_checks():
    assert failed(GOOD) == set()


def test_missing_section_fails():
    assert "S1" in failed(GOOD.replace("## 5. A full example", "## 5. Story"))


def test_undefined_jargon_fails():
    bad = GOOD.replace("An LLM is a computer program that reads and writes text. ", "").replace(
        "Large Language Model, or LLM", "LLM")
    assert "J1" in failed(bad)


def test_long_sentence_fails():
    long = " ".join(["word"] * 35) + "."
    assert "R2" in failed(GOOD.replace("## Words to know", long + "\n\n## Words to know"))


def test_loop_recovers_from_sabotage_and_terminates(tmp_path):
    cfg = Config()
    cfg.runs_dir = tmp_path / "runs"
    cfg.memory_dir = tmp_path / "mem"
    res = run_pipeline("RAG", MockLLM(), cfg, sabotage=True)
    assert res["status"] == "shipped"
    assert len(res["log"]) == 2 and not res["log"][0]["passed"]


def test_loop_stops_at_max_retries(tmp_path):
    class Stubborn(MockLLM):  # regenerate keeps returning the sabotaged text
        def complete(self, role, system, user, model, max_tokens=4000):
            if role == "generator" and "FAILED CHECKS" in user:
                return self.lesson.replace("## Words to know", "RAG permanently retrains the LLM's weights.\n\n## Words to know")
            return super().complete(role, system, user, model, max_tokens)
    cfg = Config(); cfg.runs_dir = tmp_path / "runs"; cfg.memory_dir = tmp_path / "mem"; cfg.max_retries = 2
    res = run_pipeline("RAG", Stubborn(), cfg, sabotage=True)
    assert res["status"] == "needs_human_review" and len(res["log"]) == 3
