import os
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _load_dotenv():
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


_load_dotenv()


PROVIDER = os.getenv("LLM_PROVIDER", "anthropic").lower()
_DEFAULT_MODELS = {
    "anthropic": ("claude-sonnet-5-5", "claude-opus-5-5"),
    "gemini": ("gemini-2.5-flash-lite", "gemini-2.5-flash"),  # free-tier models; check names in Google AI Studio
    "openai_compat": ("", ""),
}
_G, _J = _DEFAULT_MODELS.get(PROVIDER, ("", ""))


@dataclass
class Config:
    generator_model: str = os.getenv("GENERATOR_MODEL", _G)
    judge_model: str = os.getenv("JUDGE_MODEL", _J)
    max_retries: int = int(os.getenv("MAX_RETRIES", "2"))  # hard cap -> loop always terminates
    evolve_threshold: int = 2  # first-attempt failures of one check before a rule is learned
    data_dir: Path = ROOT / "data"
    memory_dir: Path = ROOT / "memory"
    runs_dir: Path = ROOT / "runs"
