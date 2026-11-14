#!/usr/bin/env python3
"""CLI:  generate | evaluate | feedback | evolve"""
import argparse
import json
import sys
from pathlib import Path

from lessongen.config import Config
from lessongen.evaluator import evaluate
from lessongen.generator import inject_error
from lessongen.llm import MockLLM, make_llm
from lessongen.memory import Memory
from lessongen.pipeline import _print_report, load_inputs, run_pipeline
from lessongen.reflector import evolve


def get_llm(mock):
    return MockLLM() if mock else make_llm()


def main():
    ap = argparse.ArgumentParser(description="Self-evaluating lesson generator")
    sub = ap.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("generate", help="generate -> evaluate -> regenerate loop")
    g.add_argument("--topic", default="Introduction to RAG (Retrieval-Augmented Generation)")
    g.add_argument("--sabotage", action="store_true", help="inject a deliberate error into draft 1 (demo)")
    g.add_argument("--mock", action="store_true", help="offline dry run, no API key")

    e = sub.add_parser("evaluate", help="evaluate an existing lesson file only")
    e.add_argument("--file", required=True)
    e.add_argument("--inject-error", action="store_true", help="corrupt the file in memory first (demo)")
    e.add_argument("--mock", action="store_true")

    f = sub.add_parser("feedback", help="add a human reviewer note to memory")
    f.add_argument("--note", required=True)

    v = sub.add_parser("evolve", help="learn rules from the failure log now")
    v.add_argument("--mock", action="store_true")

    a = ap.parse_args()
    cfg = Config()
    if a.cmd == "generate":
        run_pipeline(a.topic, get_llm(a.mock), cfg, sabotage=a.sabotage)
    elif a.cmd == "evaluate":
        rubric, facts = load_inputs(cfg)
        lesson = Path(a.file).read_text()
        if a.inject_error:
            lesson = inject_error(lesson, (cfg.data_dir / "sabotage.md").read_text())
            print("[demo] Deliberate error injected.")
        rep = evaluate(lesson, rubric, facts, get_llm(a.mock), cfg.judge_model)
        _print_report(1, rep)
        sys.exit(0 if rep["passed"] else 1)
    elif a.cmd == "feedback":
        Memory(cfg.memory_dir).add_feedback(a.note)
        print("Saved. It will be injected into the next generation prompt.")
    elif a.cmd == "evolve":
        rubric, _ = load_inputs(cfg)
        print(evolve(Memory(cfg.memory_dir), rubric, get_llm(a.mock), cfg.generator_model, cfg.evolve_threshold) or "Nothing new to learn.")


if __name__ == "__main__":
    main()
