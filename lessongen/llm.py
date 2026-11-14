"""Thin LLM wrapper. One real client (Anthropic) and one offline mock for dry runs/tests."""
import json
import re
import time

from .config import ROOT


def extract_json(text: str) -> dict:
    text = text.strip()
    m = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.S)
    if m:
        text = m.group(1)
    else:
        s, e = text.find("{"), text.rfind("}")
        if s != -1 and e != -1:
            text = text[s:e + 1]
    return json.loads(text)


class AnthropicLLM:
    def __init__(self):
        import anthropic
        self.client = anthropic.Anthropic()

    def complete(self, role, system, user, model, max_tokens=4000):
        last = None
        for i in range(3):
            try:
                r = self.client.messages.create(
                    model=model, max_tokens=max_tokens, system=system,
                    messages=[{"role": "user", "content": user}])
                return "".join(b.text for b in r.content if b.type == "text")
            except Exception as e:  # network / rate limit
                last = e
                time.sleep(2 * (i + 1))
        raise RuntimeError(f"LLM call failed after retries: {last}")


class OpenAICompatLLM:
    """Works with any OpenAI-style /chat/completions API: Google Gemini (free tier), Groq, OpenRouter, Ollama.
    Uses only the standard library (no extra package to install)."""

    GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/openai"

    def __init__(self, base_url, api_key):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key or "none"  # Ollama needs no key

    def complete(self, role, system, user, model, max_tokens=4000):
        import urllib.error
        import urllib.request
        body = json.dumps({
            "model": model,
            # "thinking" models count hidden reasoning inside this limit, so leave generous room
            "max_tokens": max(max_tokens, 8000),
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        }).encode()
        req = urllib.request.Request(self.base_url + "/chat/completions", data=body, headers={
            "Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"})
        last = None
        for i in range(5):
            try:
                with urllib.request.urlopen(req, timeout=180) as r:
                    data = json.loads(r.read())
                return data["choices"][0]["message"]["content"] or ""
            except urllib.error.HTTPError as e:
                last = f"HTTP {e.code}: {e.read().decode()[:300]}"
                if e.code in (429, 500, 502, 503, 504):  # free tiers rate-limit: wait and retry
                    print(f"   (rate limit / server busy, waiting {15 * (i + 1)}s...)")
                    time.sleep(15 * (i + 1))
                    continue
                break
            except Exception as e:
                last = str(e)
                time.sleep(3)
        raise RuntimeError(f"LLM call failed: {last}")


def make_llm():
    import os
    prov = os.getenv("LLM_PROVIDER", "anthropic").lower()
    if prov == "anthropic":
        return AnthropicLLM()
    key = os.getenv("LLM_API_KEY") or os.getenv("GEMINI_API_KEY", "")
    if prov == "gemini":
        if not key:
            raise SystemExit("Set LLM_API_KEY in .env (free key from https://aistudio.google.com/apikey)")
        return OpenAICompatLLM(OpenAICompatLLM.GEMINI_URL, key)
    if prov == "openai_compat":
        url = os.getenv("LLM_BASE_URL")
        if not url:
            raise SystemExit("Set LLM_BASE_URL in .env for LLM_PROVIDER=openai_compat")
        return OpenAICompatLLM(url, key)
    raise SystemExit(f"Unknown LLM_PROVIDER: {prov}")


class MockLLM:
    """Offline stand-in so the whole loop can be tested without an API key.
    NOT a quality signal - it only exercises the plumbing."""

    def __init__(self):
        self.lesson = (ROOT / "data" / "sample_lesson.md").read_text()

    def complete(self, role, system, user, model, max_tokens=4000):
        if role == "generator":
            if "FAILED CHECKS" in user:
                return self.lesson + "\n=====CHANGES=====\n- Removed the incorrect paragraph.\n- Re-wrote it in plain words."
            return self.lesson
        if role == "judge":
            ids = re.findall(r"^- (\w+) \|", user, re.M)
            bad = "permanently retrains" in user
            res = []
            for i in ids:
                fail = bad and i in ("A1", "A2", "L2")
                res.append({"id": i, "pass": not fail,
                            "evidence_quote": "RAG permanently retrains the LLM's weights" if fail else "",
                            "reason": "Contradicts grounding facts: RAG does not change model weights." if fail else "ok",
                            "fix": "Remove or correct the statement." if fail else ""})
            return json.dumps({"results": res})
        if role == "reflector":
            return "Explain every technical term in plain words in the same sentence where it first appears."
        return ""
