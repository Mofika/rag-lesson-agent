"""Deterministic (code) checkpoints. No LLM involved: cheap, repeatable, impossible to 'talk round'."""
import re

HEAD = re.compile(r"^(#{1,6})\s+(.*)$")
SKIP_READING = ("words to know", "check yourself")
DEF_CUES = re.compile(
    r"\b(means|mean|is called|are called|called|is known as|stands for|refers to|in simple words|"
    r"is a|is an|is the|are the|is when|are small)\b", re.I)


def split_sections(md):
    sections, cur, in_code = [], ["", 0, []], False
    for line in md.splitlines():
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        m = HEAD.match(line)
        if m:
            sections.append(cur)
            cur = [m.group(2).strip(), len(m.group(1)), []]
        else:
            cur[2].append(line)
    sections.append(cur)
    return [(h, lvl, "\n".join(b)) for h, lvl, b in sections if h or "".join(b).strip()]


def _clean(line):
    line = line.strip()
    line = re.sub(r"^(?:[-*]\s+|\d+\.\s+|>\s*)", "", line)
    line = re.sub(r"\*\*|__|`", "", line)
    line = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", line)
    return line.strip()


def sentences(text):
    out = []
    for line in text.splitlines():
        line = _clean(line)
        if not line:
            continue
        out += [s.strip() for s in re.split(r'(?<=[.!?])\s+|(?<=[.!?]["\u201d])\s+', line) if s.strip()]
    return out


def words(s):
    return re.findall(r"[A-Za-z0-9][A-Za-z0-9'’\-]*", s)


def syllables(word):
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 1
    n = len(re.findall(r"[aeiouy]+", w))
    if w.endswith("e") and not w.endswith(("le", "ee")) and n > 1:
        n -= 1
    return max(n, 1)


def _reading_text(md):
    return "\n".join(b for h, _, b in split_sections(md)
                     if not any(k in h.lower() for k in SKIP_READING))


def fk_stats(md):
    sents = sentences(_reading_text(md))
    ws = [w for s in sents for w in words(s)]
    if not sents or not ws:
        return {"grade": 99, "avg_len": 99, "sentences": sents, "words": 0}
    syl = sum(syllables(w) for w in ws)
    avg = len(ws) / len(sents)
    grade = 0.39 * avg + 11.8 * (syl / len(ws)) - 15.59
    return {"grade": round(grade, 1), "avg_len": round(avg, 1), "sentences": sents, "words": len(ws)}


def _ok():
    return True, "ok", "", ""


# ---- individual checks: each returns (passed, reason, evidence, fix) ----

def check_sections(md, p):
    heads = [h.lower() for h, _, _ in split_sections(md) if h]
    missing = [k for k in p["required_headings"]
               if not any(re.search(r"\b" + re.escape(k) + r"\b", h) for h in heads)]
    if missing:
        return False, f"Missing required section(s): {missing}", "", f"Add a heading containing: {missing}"
    return _ok()


def check_readability(md, p):
    st = fk_stats(md)
    if st["grade"] > p["max_fk_grade"] or st["avg_len"] > p["max_avg_sentence_words"]:
        return (False, f"Reading grade {st['grade']} (max {p['max_fk_grade']}), "
                       f"avg sentence {st['avg_len']} words (max {p['max_avg_sentence_words']}).",
                "", "Use shorter sentences and shorter, everyday words.")
    return _ok()


def check_long_sentences(md, p):
    longs = [s for s in fk_stats(md)["sentences"] if len(words(s)) > p["max_sentence_words"]]
    if longs:
        return (False, f"{len(longs)} sentence(s) longer than {p['max_sentence_words']} words.",
                longs[0][:160], "Split each long sentence into two or three short ones.")
    return _ok()


def check_complex_words(md, p):
    ws = [w for sent in fk_stats(md)["sentences"] for w in words(sent)]
    parts = [x for w in ws for x in re.split(r"[-\u2019']", w) if x]
    hard = [w for w in ws if sum(syllables(x) for x in re.split(r"-", w)) >= 4]
    pct = 100 * len(hard) / max(len(ws), 1)
    if pct > p["max_pct"]:
        return (False, f"{pct:.1f}% of words have 4+ syllables (max {p['max_pct']}%).",
                ", ".join(sorted(set(hard))[:8]), "Replace long, rare words with short everyday words.")
    return _ok()


def check_length(md, p):
    n = fk_stats(md)["words"]
    if not p["min_words"] <= n <= p["max_words"]:
        return False, f"{n} words; allowed {p['min_words']}-{p['max_words']}.", "", "Adjust length."
    return _ok()


def check_jargon(md, p):
    sents = sentences(_reading_text(md))
    for term in p["terms"]:
        pat = re.compile(r"\b" + re.escape(term) + r"s?\b", re.I)
        idx = next((i for i, s in enumerate(sents) if pat.search(s)), None)
        if idx is None:
            continue
        window = sents[idx: idx + p["window"]]
        if not any(DEF_CUES.search(s) for s in window):
            return (False, f"Term '{term}' is used but not explained within {p['window']} sentences of first use.",
                    sents[idx][:160], f"Define '{term}' in the same or next sentence where it first appears, using a cue such as "
                    f"'means', 'is called' or 'is a' (example: \"{term} means ...\").")
    return _ok()


def check_glossary(md, p):
    body = next((b for h, _, b in split_sections(md) if "words to know" in h.lower()), "")
    n = len([l for l in body.splitlines() if re.match(r"^\s*(?:[-*]|\d+\.)\s+", l)])
    if n < p["min_terms"]:
        return False, f"Glossary has {n} terms; need {p['min_terms']}.", "", "Add more glossary entries."
    return _ok()


def check_questions(md, p):
    body = next((b for h, _, b in split_sections(md) if "check yourself" in h.lower()), "")
    n = body.count("?")
    if n < p["min_questions"]:
        return (False, f"{n} self-check questions; need {p['min_questions']}.", "",
                f"Rewrite the 'Check yourself' section with at least {p['min_questions'] + 1} numbered questions. "
                "EVERY question must end with a question mark (?).")
    return _ok()


CODE_CHECKS = {
    "sections": check_sections, "readability": check_readability, "long_sentences": check_long_sentences,
    "length": check_length, "complex_words": check_complex_words, "jargon": check_jargon, "glossary": check_glossary, "questions": check_questions,
}


def run_code_checks(md, rubric):
    results = []
    for c in rubric["checks"]:
        if c["type"] != "code":
            continue
        passed, reason, evidence, fix = CODE_CHECKS[c["fn"]](md, c.get("params", {}))
        results.append({"id": c["id"], "title": c["title"], "dimension": c["dimension"], "type": "code",
                        "passed": passed, "reason": reason, "evidence": evidence, "fix": fix, "flags": []})
    return results
