from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import httpx

from .config import AppSettings


@dataclass
class PullRequestInfo:
	url: str
	title: str
	body: str
	author: str
	base_ref: str
	head_ref: str
	number: int
	html_url: str
	draft: bool


def extract_pr_info(payload: Dict[str, Any]) -> PullRequestInfo:
	pr = payload["pull_request"]
	return PullRequestInfo(
		url=pr.get("url", ""),
		title=pr.get("title", ""),
		body=pr.get("body", "") or "",
		author=(pr.get("user") or {}).get("login", "unknown"),
		base_ref=(pr.get("base") or {}).get("ref", ""),
		head_ref=(pr.get("head") or {}).get("ref", ""),
		number=pr.get("number", 0),
		html_url=pr.get("html_url", ""),
		draft=bool(pr.get("draft", False)),
	)


def fetch_pr_file_summaries(payload: Dict[str, Any]) -> str:
	"""Return a concise text of changed files for the PR, if possible.

	If a GitHub token is configured, fetch the changed files for additional context.
	Truncates to keep within prompt limits.
	"""
	settings = AppSettings()
	pr = payload.get("pull_request") or {}
	files_url: Optional[str] = pr.get("url")
	if not files_url:
		return ""
	files_url = files_url + "/files"

	headers = {}
	if settings.github_token:
		headers["Authorization"] = f"Bearer {settings.github_token.get_secret_value()}"
	headers["Accept"] = "application/vnd.github+json"

	try:
		with httpx.Client(timeout=httpx.Timeout(10.0, connect=5.0)) as client:
			resp = client.get(files_url, headers=headers)
			if resp.status_code != 200:
				return ""
			files: List[Dict[str, Any]] = resp.json()
			parts: List[str] = []
			for f in files[:50]:
				filename = f.get("filename")
				status = f.get("status")
				additions = f.get("additions")
				deletions = f.get("deletions")
				parts.append(f"- {filename} ({status}, +{additions}/-{deletions})")
			return "\n".join(parts[:100])
	except Exception:
		return ""
