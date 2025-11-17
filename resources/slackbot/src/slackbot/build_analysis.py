"""Build log analysis using hybrid approach."""

import json
import logging
import re
from collections import defaultdict
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# Import OpenAI for LLM analysis
from openai import OpenAI

from .config import AppSettings

ANSI_RE = re.compile(r"\x1B[@-_][0-?]*[ -/]*[@-~]")

ERROR_PATTERNS = [
	r"\berror:\s+(.+)",
	r"\bfatal:\s+(.+)",
	r"\bundefined reference to\s+(.+)",
	r"\bundefined symbol:\s+(.+)",
	r"\bld:\s+cannot find\s+(.+)",
	r"\bcannot find\s+(-l\S+|\S+)",
	r"\bno rule to make target\b.*",
	r"\bcmake error\b[:]?\s*(.+)",
	r"\bconfiguration error\b[:]?\s*(.+)",
]

CATEGORY_RULES = [
	("linker_missing", re.compile(r"\b(ld: )?cannot find\b|\b-l[A-Za-z0-9_\-]+\b")),
	("linker_undefined", re.compile(r"\bundefined reference\b|\bundefined symbol\b")),
	("cmake_config", re.compile(r"\bcmake error\b|\bno rule to make target\b|\bconfiguration error\b")),
	("compilation", re.compile(r"\berror:\b|^\s*\d+\s*errors? generated\b")),
]


def strip_ansi(text: str) -> str:
	"""Remove ANSI escape codes."""
	return ANSI_RE.sub("", text)


def find_error_lines_with_context(
	lines: List[str], context_lines: int = 5
) -> List[Dict[str, Any]]:
	"""Find error lines with surrounding context."""
	errors = []
	
	for i, line in enumerate(lines):
		line_clean = strip_ansi(line)
		for pattern in ERROR_PATTERNS:
			if re.search(pattern, line_clean, re.IGNORECASE):
				# Get context
				start = max(0, i - context_lines)
				end = min(len(lines), i + context_lines + 1)
				context = lines[start:end]
				
				errors.append({
					"line_number": i + 1,
					"error_line": line_clean.strip(),
					"context": [strip_ansi(l).strip() for l in context],
				})
				break  # Only match once per line
	
	return errors


def categorize_errors(errors: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
	"""Categorize errors by type."""
	categories: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
	
	for error in errors:
		error_text = error["error_line"].lower()
		categorized = False
		
		for category, pattern in CATEGORY_RULES:
			if pattern.search(error_text):
				categories[category].append(error)
				categorized = True
				break
		
		if not categorized:
			categories["other"].append(error)
	
	return categories


def create_focused_prompt(
	errors: List[Dict[str, Any]], build_info: Optional[Dict[str, Any]] = None
) -> str:
	"""Create a focused prompt with only error sections."""
	build_section = ""
	if build_info:
		build_section = f"Build: {build_info.get('component', 'unknown')} ({build_info.get('build_id', 'unknown')})\n\n"
	
	error_sections = []
	for error in errors[:20]:  # Limit to top 20 errors
		context_str = "\n".join(error["context"])
		error_sections.append(f"Line {error['line_number']}:\n{context_str}\n")
	
	prompt = f"""Analyze this build log failure. Focus on the error sections below.

{build_section}Error sections:
{chr(10).join(error_sections)}

Provide a JSON response with:
1. "root_causes": Array of top 3 root causes, each with:
   - "cause": Brief description
   - "evidence": Line number and snippet
   - "confidence": "high" | "medium" | "low"
   - "next_action": What to do to fix it
2. "summary": Array of 3 bullet points summarizing the failure

Be concise and actionable."""
	
	return prompt


def analyze_with_llm(prompt: str) -> Dict[str, Any]:
	"""Analyze build log using LLM."""
	settings = AppSettings()
	client = OpenAI(api_key=settings.openai_api_key.get_secret_value())
	
	try:
		resp = client.chat.completions.create(
			model=settings.openai_model,
			messages=[{"role": "user", "content": prompt}],
			temperature=0.3,
			max_tokens=1000,
		)
		
		if resp.choices and len(resp.choices) > 0:
			content = resp.choices[0].message.content
			if content:
				# Try to extract JSON from response
				json_match = re.search(r"\{.*\}", content, re.DOTALL)
				if json_match:
					return json.loads(json_match.group())
				# Fallback: try parsing entire content
				return json.loads(content)
	except Exception as e:
		logger.error(f"LLM analysis failed: {e}")
	
	return {"root_causes": [], "summary": ["Analysis unavailable"]}


def analyze_build_log(log_content: str, build_info: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
	"""Analyze build log using hybrid approach."""
	lines = log_content.split("\n")
	
	# Step 1: Find errors with context
	errors = find_error_lines_with_context(lines, context_lines=5)
	logger.info(f"Found {len(errors)} error sections")
	
	if not errors:
		return {
			"root_causes": [],
			"summary": ["No errors found in build log"],
			"error_count": 0,
		}
	
	# Step 2: Categorize errors
	categories = categorize_errors(errors)
	logger.info(f"Error categories: {dict((k, len(v)) for k, v in categories.items())}")
	
	# Step 3: Create focused prompt
	prompt = create_focused_prompt(errors, build_info)
	logger.debug(f"Prompt length: {len(prompt)} chars")
	
	# Step 4: LLM analysis
	analysis = analyze_with_llm(prompt)
	
	# Add metadata
	analysis["error_count"] = len(errors)
	analysis["categories"] = {k: len(v) for k, v in categories.items()}
	
	return analysis

