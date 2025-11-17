from __future__ import annotations

from textwrap import shorten

from openai import OpenAI

from .config import AppSettings
from .github import PullRequestInfo


def summarize_pull_request(pr: PullRequestInfo, files_text: str) -> str:
	settings = AppSettings()
	client = OpenAI(api_key=settings.openai_api_key.get_secret_value())

	files_section = files_text.strip()
	if files_section:
		files_section = f"\nChanged files (top):\n{files_section}\n"

	prompt = (
		"You are a senior engineer helping summarize a GitHub Pull Request for Slack.\n"
		"Write a concise, helpful summary with:\n"
		"- What it does and why.\n- Risk level and notable changes.\n- Suggested reviewers or areas impacted.\n"
		"Keep it under 150 words.\n\n"
		f"Title: {pr.title}\n"
		f"Author: {pr.author}\n"
		f"Base -> Head: {pr.base_ref} -> {pr.head_ref}\n"
		f"Draft: {pr.draft}\n"
		f"PR URL: {pr.html_url}\n\n"
		f"Description:\n{shorten(pr.body or 'No description provided.', width=2000, placeholder='...')}\n"
		f"{files_section}"
	)

	resp = client.chat.completions.create(
		model=settings.openai_model,
		messages=[{"role": "user", "content": prompt}],
	)

	# Extract the text response
	if resp.choices and len(resp.choices) > 0:
		message = resp.choices[0].message
		if message and message.content:
			return message.content.strip()

	# Fallback for unexpected shapes
	return "PR Summary unavailable."
