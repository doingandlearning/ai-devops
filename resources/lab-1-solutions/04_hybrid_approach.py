#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hybrid Approach: Deterministic filtering + LLM analysis (production-ready)

Improvements:
- Robust error extraction (no accidental skip of ERROR lines; ANSI stripped)
- Clusters nearby errors into sections to avoid duplicate/low-signal chunks
- Safer categorisation (compiler/linker/config buckets)
- Hard caps on sections + characters sent to the LLM
- Strict JSON schema check + graceful fallback
- Backend selection via CLI/env; sensible defaults
- Writes machine-readable artefacts for later comparison
"""

import os
import re
import json
import sys
import argparse
from collections import Counter, defaultdict
from pathlib import Path
from typing import List, Dict, Any, Tuple

ANSI_RE = re.compile(r"\x1B[@-_][0-?]*[ -/]*[@-~]")

ERROR_PATTERNS = [
    r"\berror:\s+(.+)",                      # gcc/clang style
    r"\bfatal:\s+(.+)",
    r"\bundefined reference to\s+(.+)",
    r"\bundefined symbol:\s+(.+)",
    r"\bld:\s+cannot find\s+(.+)",
    r"\bcannot find\s+(-l\S+|\S+)",
    r"\bno rule to make target\b.*",
    r"\bcmake error\b[:]?\s*(.+)",
    r"\bconfiguration error\b[:]?\s*(.+)",
]

# Category matchers (order matters)
CATEGORY_RULES = [
    ("linker_missing", re.compile(r"\b(ld: )?cannot find\b|\b-l[A-Za-z0-9_\-]+\b")),
    ("linker_undefined", re.compile(r"\bundefined reference\b|\bundefined symbol\b")),
    ("cmake_config", re.compile(r"\bcmake error\b|\bno rule to make target\b|\bconfiguration error\b")),
    ("compilation", re.compile(r"\berror:\b|^\s*\d+\s*errors? generated\b")),
]

SCHEMA = {
    "root_causes": list,
    "summary": list,
}

def strip_ansi(s: str) -> str:
    return ANSI_RE.sub("", s)

def read_lines(path: Path) -> List[str]:
    if not path.exists():
        print(f"Error: {path} not found", file=sys.stderr)
        sys.exit(1)
    try:
        raw = path.read_text(errors="replace").splitlines()
    except UnicodeDecodeError:
        raw = path.read_bytes().decode("utf-8", errors="replace").splitlines()
    # Strip ANSI + keep original indices 1-based
    return [strip_ansi(line) for line in raw]

def match_error(line: str) -> bool:
    ls = line.strip()
    for pat in ERROR_PATTERNS:
        if re.search(pat, ls, flags=re.IGNORECASE):
            return True
    # Also catch common CI markers
    if re.search(r"\bFAILED\b|\bFAILURE\b", ls) and re.search(r"test|target|build|link", ls, re.I):
        return True
    return False

def find_error_indices(lines: List[str]) -> List[int]:
    idxs = []
    for i, line in enumerate(lines, 1):
        if match_error(line):
            idxs.append(i)
    return idxs

def cluster_indices(indices: List[int], window: int = 8) -> List[List[int]]:
    """Group nearby error lines into clusters by proximity."""
    if not indices:
        return []
    clusters = [[indices[0]]]
    for n in indices[1:]:
        if n - clusters[-1][-1] <= window:
            clusters[-1].append(n)
        else:
            clusters.append([n])
    return clusters

def slice_with_context(lines: List[str], start: int, end: int) -> List[str]:
    start = max(1, start) - 1
    end = min(len(lines), end)
    return [lines[i] for i in range(start, end)]

def extract_sections(lines: List[str], clusters: List[List[int]], ctx: int = 5,
                     max_sections: int = 10, max_chars: int = 12000) -> Tuple[List[Dict[str, Any]], int]:
    """Make contextual sections; enforce hard caps."""
    sections = []
    total_chars = 0
    for c in clusters[:max_sections]:
        lo = min(c) - ctx
        hi = max(c) + ctx
        chunk = slice_with_context(lines, lo, hi)
        chunk_text = "\n".join(chunk).strip()
        # capture headline
        head_line_no = min(c)
        head_line = lines[head_line_no - 1].strip()
        sec = {
            "line_number": head_line_no,
            "headline": head_line,
            "lines": chunk,
        }
        # cap by total char budget
        if total_chars + len(chunk_text) > max_chars:
            # try truncated version
            truncated = "\n".join(chunk[: max(1, len(chunk)//2)])
            if total_chars + len(truncated) > max_chars:
                break
            sec["lines"] = chunk[: max(1, len(chunk)//2)]
            total_chars += len(truncated)
        else:
            total_chars += len(chunk_text)
        sections.append(sec)
    return sections, total_chars

def categorise_section(text: str) -> str:
    for name, rx in CATEGORY_RULES:
        if rx.search(text):
            return name
    return "other"

def categorise_sections(sections: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    buckets: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for s in sections:
        body = "\n".join(s["lines"])
        cat = categorise_section(body)
        buckets[cat].append(s)
    return buckets

def extract_build_info(lines: List[str]) -> Dict[str, str]:
    info = {}
    header = lines[:40]
    pairs = {
        "component": r"\bcomponent:\s*(.+)",
        "build_id": r"\bbuild id:\s*(.+)",
        "compiler": r"\bcompiler:\s*(.+)",
        "branch": r"\bbranch:\s*(.+)",
        "runner": r"\brunner:\s*(.+)",
    }
    for line in header:
        for k, pat in pairs.items():
            m = re.search(pat, line, re.I)
            if m and k not in info:
                info[k] = m.group(1).strip()
    return info

def make_prompt(sections: List[Dict[str, Any]], build_info: Dict[str, str]) -> str:
    header = [
        "ROLE: You are assisting the RDK CMF team with CI build failures.",
        "",
        "TASK: Analyse the provided error sections (already filtered deterministically).",
        "",
        "OUTPUT (valid JSON ONLY):",
        "{",
        '  "root_causes": [',
        '    { "cause": "string",',
        '      "evidence": [ { "line": number, "snippet": "string" } ],',
        '      "confidence": "high|medium|low",',
        '      "next_action": "string" }',
        "  ],",
        '  "summary": ["• bullet 1", "• bullet 2", "• bullet 3"]',
        "}",
        "",
        "REQUIREMENTS:",
        "- Cite at least one exact line number + snippet per root cause.",
        "- Prefer concrete commands/flags over generic advice.",
        "- If uncertain, set confidence to low and state what’s missing.",
        "- Do not invent symbols/functions/libraries.",
        "",
        "BUILD INFO:",
    ]
    if build_info:
        for k, v in build_info.items():
            header.append(f"- {k}: {v}")
    header += ["", "ERROR SECTIONS:", "=" * 60]

    body_lines = []
    for i, sec in enumerate(sections, 1):
        body_lines.append(f"\n--- Error Section {i} ---")
        body_lines.append(f"Line {sec['line_number']}: {sec['headline']}")
        body_lines.append("\nContext:")
        for ln, t in enumerate(sec["lines"], start=sec["line_number"] - len(sec["lines"])//2):
            # The above ln indexing is an approximation; we’ll embed explicit evidence later anyway.
            body_lines.append(f"  {t}")

    footer = [
        "\n" + "=" * 60,
        "IMPORTANT: Respond with VALID JSON ONLY. No additional commentary.",
    ]
    return "\n".join(header + body_lines + footer)

def choose_backend_env_cli(args) -> Tuple[str, str]:
    backend = args.backend or os.getenv("HYBRID_BACKEND", "ollama").lower()
    model = args.model or os.getenv("HYBRID_MODEL", ("codellama:7b" if backend == "ollama" else "gpt-4o"))
    return backend, model

def call_ollama(prompt: str, model: str) -> str:
    import requests
    url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
    payload = {"model": model, "prompt": prompt, "stream": False, "format": "json"}
    r = requests.post(url, json=payload, timeout=180)
    r.raise_for_status()
    data = r.json()
    return data.get("response", "")

def call_openai(prompt: str, model: str) -> str:
    try:
        from openai import OpenAI
    except Exception:
        import openai  # fallback older SDK
        client = openai
        if hasattr(client, "OpenAI"):
            client = client.OpenAI()  # type: ignore
            # Unlikely path; prefer new SDK
    try:
        client = OpenAI()
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful DevOps engineer. Respond with VALID JSON ONLY."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            response_format={"type": "json_object"},
        )
        return resp.choices[0].message.content or ""
    except Exception as e:
        print(f"[openai] {e}", file=sys.stderr)
        return ""

def call_anthropic(prompt: str, model: str) -> str:
    try:
        from anthropic import Anthropic
        client = Anthropic()
        resp = client.messages.create(
            model=model,
            max_tokens=2000,
            temperature=0.2,
            messages=[{"role": "user", "content": prompt}],
        )
        # Claude returns text blocks; extract as a single string
        parts = []
        for blk in resp.content:
            if getattr(blk, "type", "") == "text":
                parts.append(getattr(blk, "text", "") or "")
        return "".join(parts)
    except Exception as e:
        print(f"[anthropic] {e}", file=sys.stderr)
        return ""

def call_backend(prompt: str, backend: str, model: str) -> str:
    if backend == "ollama":
        return call_ollama(prompt, model)
    if backend == "openai":
        return call_openai(prompt, model)
    if backend == "anthropic":
        return call_anthropic(prompt, model)
    print(f"Unknown backend: {backend}", file=sys.stderr)
    return ""

def extract_json_block(s: str) -> str:
    """Extract the first top-level JSON object/array from a string."""
    start = s.find("{")
    if start == -1:
        start = s.find("[")
    if start == -1:
        return ""
    # naive bracket match
    stack = []
    for i in range(start, len(s)):
        ch = s[i]
        if ch in "{[":
            stack.append("}" if ch == "{" else "]")
        elif ch in "}]":
            if not stack or ch != stack[-1]:
                continue
            stack.pop()
            if not stack:
                return s[start : i + 1]
    return ""

def valid_schema(obj: Any) -> bool:
    if not isinstance(obj, dict):
        return False
    for k, t in SCHEMA.items():
        if k not in obj or not isinstance(obj[k], t):
            return False
    # basic element checks
    for rc in obj.get("root_causes", []):
        if not isinstance(rc, dict):
            return False
        if "cause" not in rc or "confidence" not in rc or "next_action" not in rc:
            return False
        if "evidence" not in rc or not isinstance(rc["evidence"], list) or not rc["evidence"]:
            return False
    return True

def parse_llm_response(raw: str) -> Tuple[Dict[str, Any], str]:
    """Return (json_obj, error_msg). error_msg empty on success."""
    if not raw:
        return {}, "empty response"
    candidate = raw.strip()
    if not (candidate.startswith("{") or candidate.startswith("[")):
        candidate = extract_json_block(candidate)
    if not candidate:
        return {}, "no json block found"
    try:
        obj = json.loads(candidate)
    except json.JSONDecodeError as e:
        return {}, f"json decode error: {e}"
    if not valid_schema(obj):
        return {}, "schema validation failed"
    return obj, ""

def write_artifact(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, indent=2))

def estimate_tokens(chars: int) -> int:
    # Rough, conservative: 1 token ≈ 3.5 chars (English+code average)
    return max(1, int(round(chars / 3.5)))

def run(args: argparse.Namespace) -> int:
    log_path = Path(args.log)
    lines = read_lines(log_path)
    print("=" * 60)
    print("Hybrid Approach: Deterministic Filtering + LLM Analysis")
    print("=" * 60)
    print(f"Read {len(lines)} lines from: {log_path}")

    build_info = extract_build_info(lines)
    if build_info:
        print(f"Build info: {build_info}")

    err_idxs = find_error_indices(lines)
    print(f"Detected {len(err_idxs)} error lines")

    clusters = cluster_indices(err_idxs, window=args.cluster_window)
    print(f"Clustered into {len(clusters)} sections (window={args.cluster_window})")

    sections, sent_chars = extract_sections(
        lines, clusters, ctx=args.context, max_sections=args.max_sections, max_chars=args.max_chars
    )
    if not sections:
        print("No error sections after filtering. Exiting.")
        return 0

    cat = categorise_sections(sections)
    counts = {k: len(v) for k, v in cat.items() if v}
    print(f"Categories: {counts or 'n/a'}")

    # Prompt
    prompt = make_prompt(sections, build_info)
    full_chars = sum(len(l) + 1 for l in lines)
    saved_chars = max(0, full_chars - len(prompt))

    print(f"Original log chars: ~{full_chars}")
    print(f"Filtered prompt chars: ~{len(prompt)}")
    print(f"Estimated token savings: ~{estimate_tokens(saved_chars)} tokens "
          f"({int(100 * saved_chars / max(1, full_chars))}% reduction)")

    # Backend
    backend, model = choose_backend_env_cli(args)
    print(f"Backend: {backend} | Model: {model}")

    raw = call_backend(prompt, backend, model)
    if not raw:
        print("LLM call failed or returned empty response.")
        results = {
            "root_causes": [],
            "summary": ["No AI summary available.", "See deterministic sections.", "Check CI artefacts."],
        }
        # Artefacts
        out_dir = Path(args.outdir)
        out_dir.mkdir(parents=True, exist_ok=True)
        write_artifact(out_dir / "hybrid_result.json", results)
        write_artifact(out_dir / "sections.json", sections)
        write_artifact(out_dir / "categories.json", counts)
        print(json.dumps(results, indent=2))
        return 1

    obj, err = parse_llm_response(raw)
    if err:
        print(f"LLM response parse error: {err}")
        # Fallback minimal object using deterministic hints
        top_causes = []
        # naive headline frequency
        heads = [s["headline"] for s in sections if s.get("headline")]
        freq = Counter(heads).most_common(3)
        for cause, _ in freq:
            # pick first evidence line from that section
            sec = next((s for s in sections if s.get("headline") == cause), None)
            ev = []
            if sec:
                # try to find a line with 'error' or 'undefined'
                for offset, t in enumerate(sec["lines"], start=0):
                    if re.search(r"\berror\b|undefined|cannot find|cmake", t, re.I):
                        ev.append({"line": sec["line_number"] + offset, "snippet": t.strip()[:200]})
                        break
            top_causes.append({
                "cause": cause[:120],
                "evidence": ev or [{"line": sec["line_number"], "snippet": sec["headline"][:200]}] if sec else [],
                "confidence": "low",
                "next_action": "Re-run with stricter prompt or inspect deterministic section.",
            })
        obj = {
            "root_causes": top_causes,
            "summary": ["AI output invalid; using deterministic fallback.",
                        "Inspect sections.json for evidence.",
                        "Re-run with a JSON-enforcing model or smaller prompt."],
        }

    # Present + write artefacts
    print("\n" + "=" * 60)
    print("Top 3 Root Causes:")
    for i, rc in enumerate(obj.get("root_causes", [])[:3], 1):
        print(f"{i}. {rc.get('cause', 'Unknown')}")
        ev = rc.get("evidence", [])
        if ev:
            e0 = ev[0]
            print(f"   Evidence: line {e0.get('line', '?')}: {e0.get('snippet', '')[:160]}")
        print(f"   Confidence: {rc.get('confidence', 'n/a')}")
        print(f"   Next Action: {rc.get('next_action', 'n/a')}\n")

    print("Summary (for PR/Slack):")
    for b in obj.get("summary", []):
        print(f"  • {b}")

    out_dir = Path(args.outdir)
    out_dir.mkdir(parents=True, exist_ok=True)
    # Save artefacts for auditing
    write_artifact(out_dir / "hybrid_result.json", obj)
    write_artifact(out_dir / "sections.json", sections)
    write_artifact(out_dir / "categories.json", counts)
    meta = {
        "backend": backend,
        "model": model,
        "full_chars": full_chars,
        "prompt_chars": len(prompt),
        "saved_chars": saved_chars,
        "estimated_token_savings": estimate_tokens(saved_chars),
        "section_count": len(sections),
        "categories": counts,
        "build_info": build_info,
        "log_file": str(log_path),
    }
    write_artifact(out_dir / "meta.json", meta)

    print("\nFull JSON Response:\n" + json.dumps(obj, indent=2))
    print(f"\nArtefacts written to: {out_dir.resolve()}")
    return 0

def main():
    p = argparse.ArgumentParser(description="Hybrid build-log triage")
    p.add_argument("--log", default="build.log", help="Path to build log")
    p.add_argument("--backend", choices=["ollama", "openai", "anthropic"], help="LLM backend (env HYBRID_BACKEND)")
    p.add_argument("--model", help="Model name (env HYBRID_MODEL)")
    p.add_argument("--context", type=int, default=5, help="Lines of context before/after")
    p.add_argument("--cluster-window", type=int, default=8, help="Proximity (lines) to cluster errors")
    p.add_argument("--max-sections", type=int, default=10, help="Max error sections to send")
    p.add_argument("--max-chars", type=int, default=12000, help="Max characters to include in prompt")
    p.add_argument("--outdir", default=".hybrid_out", help="Directory for JSON artefacts")
    args = p.parse_args()
    sys.exit(run(args))

if __name__ == "__main__":
    main()
