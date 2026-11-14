from .checks_code import run_code_checks
from .judge import run_judge


def evaluate(lesson, rubric, facts, llm, judge_model):
    """Code checks first (cheap). LLM judge always runs too so the log shows ALL failures at once,
    which lets one retry fix everything instead of one failure per retry."""
    results = run_code_checks(lesson, rubric) + run_judge(lesson, rubric, facts, llm, judge_model)
    failed = [r for r in results if not r["passed"]]
    return {"passed": not failed, "n_checks": len(results), "n_failed": len(failed), "results": results}
