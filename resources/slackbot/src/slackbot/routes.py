import hmac
import json
import logging
from hashlib import sha256
from typing import Any, Dict
from urllib.parse import unquote, parse_qs

from flask import Blueprint, Response, current_app, request

from .config import AppSettings
from .github import extract_pr_info, fetch_pr_file_summaries
from .llm import summarize_pull_request, send_message_to_llm
from .slack_client import SlackMessenger
from .build_analysis import analyze_build_log


bp = Blueprint("routes", __name__)
logger = logging.getLogger(__name__)


@bp.get("/healthz")
def healthz() -> Response:
	return Response("ok", status=200)


def _verify_signature(secret: str, signature: str, payload: bytes) -> bool:
	"""Verify GitHub webhook signature."""
	if not signature:
		logger.debug("No signature provided")
		return False
	if not signature.startswith("sha256="):
		logger.debug(f"Signature doesn't start with 'sha256=': {signature[:20]}...")
		return False
	
	computed = "sha256=" + hmac.new(
		secret.encode("utf-8"),
		payload,
		sha256,
	).hexdigest()
	
	# Log for debugging (only first few chars to avoid exposing secrets)
	logger.debug(f"Received signature: {signature[:20]}...")
	logger.debug(f"Computed signature: {computed[:20]}...")
	logger.debug(f"Payload length: {len(payload)} bytes")
	logger.debug(f"Secret length: {len(secret)} chars")
	
	match = hmac.compare_digest(signature, computed)
	if not match:
		logger.warning(f"Signature mismatch! Received: {signature[:20]}... Computed: {computed[:20]}...")
		logger.warning(f"Payload preview: {payload[:100]}...")
	
	return match


@bp.post("/github/webhook")
def github_webhook() -> Response:
	"""Handle GitHub webhook events."""
	settings = AppSettings()
	
	# Get raw request data for signature verification (must be bytes)
	# IMPORTANT: Get raw bytes BEFORE Flask parses the request body
	# This ensures we have the exact bytes GitHub sent for signature verification
	raw_data = request.get_data(cache=False)
	if not raw_data:
		# Fallback to request.data if get_data() doesn't work
		raw_data = request.data
	
	# Get event type first (before signature check for ping events)
	event = request.headers.get("X-GitHub-Event", "")
	content_type = request.headers.get("Content-Type", "")
	logger.info(f"Received GitHub webhook event: {event}")
	logger.debug(f"Content-Type: {content_type}")
	logger.debug(f"Request data length: {len(raw_data)} bytes")
	logger.debug(f"Request data preview: {raw_data[:100] if raw_data else b'<empty>'}...")
	
	# Handle form-encoded payloads (ngrok or proxy might convert JSON to form-encoded)
	# GitHub sends JSON, but proxies might convert it to form-encoded with 'payload' field
	payload_data = None
	if content_type and "application/x-www-form-urlencoded" in content_type:
		# For form-encoded, the JSON is in the 'payload' form field (URL-encoded)
		# We need to parse it from the raw bytes since request.get_data() consumes the body
		logger.debug("Detected form-encoded payload, will extract JSON from 'payload' field")
		try:
			# Parse form data from raw bytes
			form_data = parse_qs(raw_data.decode('utf-8'), keep_blank_values=True)
			if 'payload' in form_data:
				# Get the first value (parse_qs returns lists)
				payload_data = form_data['payload'][0]
				# URL-decode the payload (it's URL-encoded in the form field)
				payload_data = unquote(payload_data)
				logger.debug(f"Extracted and URL-decoded payload from form field: {len(payload_data)} chars")
			else:
				logger.warning("Form-encoded payload but no 'payload' field found")
				logger.debug(f"Form fields: {list(form_data.keys())}")
		except Exception as e:
			logger.error(f"Failed to parse form-encoded data: {e}")
			payload_data = None
	
	# Handle ping event (GitHub sends this when webhook is registered)
	if event == "ping":
		# Ping events don't always have signatures, but verify if present
		signature = request.headers.get("X-Hub-Signature-256", "")
		logger.debug(f"Ping event signature: {signature[:20]}..." if signature else "No signature")
		
		if signature:
			if not _verify_signature(
				settings.github_webhook_secret.get_secret_value(),
				signature,
				raw_data
			):
				logger.warning("Ping event with invalid signature")
				return Response(
					json.dumps({"ok": False, "error": "invalid signature"}),
					status=401,
					mimetype="application/json"
				)
			logger.debug("Ping event signature verified")
		
		# Return proper JSON response for ping
		# Handle form-encoded payloads
		if payload_data:
			payload: Dict[str, Any] = json.loads(payload_data)
		else:
			payload: Dict[str, Any] = request.get_json(force=True, silent=True) or {}
		zen = payload.get("zen", "Design for failure")
		logger.info(f"Ping event received: {zen}")
		return Response(
			json.dumps({"ok": True, "event": "ping", "zen": zen}),
			status=200,
			mimetype="application/json"
		)
	
	# For all other events, verify signature
	signature = request.headers.get("X-Hub-Signature-256", "")
	logger.debug(f"Event signature: {signature[:20]}..." if signature else "No signature")
	logger.debug(f"All headers: {dict(request.headers)}")
	
	secret_value = settings.github_webhook_secret.get_secret_value()
	logger.debug(f"Secret configured: {'Yes' if secret_value else 'No'} (length: {len(secret_value) if secret_value else 0})")
	
	if not _verify_signature(
		secret_value,
		signature,
		raw_data
	):
		logger.warning("Invalid signature for webhook")
		logger.warning(f"Check that SLACKBOT_GITHUB_WEBHOOK_SECRET matches GitHub webhook secret")
		return Response(
			json.dumps({"ok": False, "error": "invalid signature"}),
			status=401,
			mimetype="application/json"
		)
	logger.debug("Signature verified")
	
	# Handle pull_request events
	if event == "pull_request":
		# Handle form-encoded payloads
		if payload_data:
			try:
				payload: Dict[str, Any] = json.loads(payload_data)
			except json.JSONDecodeError as e:
				logger.error(f"Failed to parse JSON from form-encoded payload: {e}")
				logger.debug(f"Payload data (first 200 chars): {payload_data[:200]}")
				return Response(
					json.dumps({"ok": False, "error": "invalid JSON in payload"}),
					status=400,
					mimetype="application/json"
				)
		else:
			payload: Dict[str, Any] = request.get_json(force=True, silent=True) or {}
		action = payload.get("action", "")
		logger.info(f"PR event action: {action}")
		if not action:
			logger.warning(f"PR event has no action field. Payload keys: {list(payload.keys())[:10]}")
		
		# Only process specific actions
		if action not in {"opened", "reopened", "synchronize", "ready_for_review"}:
			logger.info(f"Ignoring pull_request event with action: {action}")
			return Response(
				json.dumps({"ok": True, "event": "pull_request", "action": action, "status": "ignored"}),
				status=200,
				mimetype="application/json"
			)
		
		try:
			pr = extract_pr_info(payload)
			logger.info(f"Processing PR #{pr.number}: {pr.title}")
			
			# Optionally enrich with file summaries
			files_text = fetch_pr_file_summaries(payload)
			
			# Summarize via LLM
			summary = summarize_pull_request(pr, files_text)
			
			# Send to Slack
			slack = SlackMessenger(token=settings.slack_bot_token.get_secret_value())
			channel = settings.slack_default_channel
			message_ts = slack.post_pr_summary(channel=channel, summary=summary)
			
			logger.info(f"PR summary posted to Slack: {message_ts}")
			return Response(
				json.dumps({"ok": True, "ts": message_ts, "pr": pr.number}),
				status=200,
				mimetype="application/json"
			)
		except Exception as e:
			logger.error(f"Error processing PR webhook: {e}", exc_info=True)
			return Response(
				json.dumps({"ok": False, "error": str(e)}),
				status=500,
				mimetype="application/json"
			)
	
	# Ignore other event types
	logger.info(f"Ignoring event type: {event}")
	return Response(
		json.dumps({"ok": True, "event": event, "status": "ignored"}),
		status=200,
		mimetype="application/json"
	)


@bp.post("/build/failure")
def build_failure() -> Response:
	"""Handle build failure notifications."""
	settings = AppSettings()
	
	try:
		# Get build log from request
		payload: Dict[str, Any] = request.get_json(force=True, silent=True) or {}
		
		log_content = payload.get("log", "")
		if not log_content:
			# Try to get from file path
			log_path = payload.get("log_path", "")
			if log_path:
				try:
					with open(log_path, "r", encoding="utf-8") as f:
						log_content = f.read()
				except Exception as e:
					logger.error(f"Failed to read log file {log_path}: {e}")
					return Response(
						json.dumps({"ok": False, "error": f"Failed to read log file: {e}"}),
						status=400,
						mimetype="application/json"
					)
		
		if not log_content:
			return Response(
				json.dumps({"ok": False, "error": "No log content provided"}),
				status=400,
				mimetype="application/json"
			)
		
		# Build info
		build_info = {
			"repo": payload.get("repo", "unknown"),
			"branch": payload.get("branch", "unknown"),
			"commit": payload.get("commit", "unknown"),
			"build_url": payload.get("build_url", ""),
		}
		
		logger.info(f"Analyzing build failure: {build_info['repo']}/{build_info['branch']}")
		
		# Analyze build log
		analysis = analyze_build_log(log_content, build_info)
		
		# Format for Slack
		summary_lines = analysis.get("summary", ["Build failure analysis unavailable"])
		root_causes = analysis.get("root_causes", [])
		
		# Create Slack message
		message_parts = [
			f"🔴 *Build Failed: {build_info['repo']}/{build_info['branch']}*",
			"",
			"*Summary:*",
		]
		
		for line in summary_lines[:3]:
			message_parts.append(f"• {line}")
		
		if root_causes:
			message_parts.append("")
			message_parts.append("*Top Root Causes:*")
			for i, cause in enumerate(root_causes[:3], 1):
				message_parts.append(f"{i}. *{cause.get('cause', 'Unknown')}*")
				if cause.get("evidence"):
					message_parts.append(f"   Evidence: {cause['evidence']}")
				if cause.get("next_action"):
					message_parts.append(f"   Fix: {cause['next_action']}")
		
		if build_info.get("build_url"):
			message_parts.append("")
			message_parts.append(f"<{build_info['build_url']}|View Build Log>")
		
		message = "\n".join(message_parts)
		
		# Send to Slack
		slack = SlackMessenger(token=settings.slack_bot_token.get_secret_value())
		channel = settings.slack_default_channel
		message_ts = slack.post_message(channel=channel, text=message)
		
		if message_ts:
			logger.info(f"Build failure notification posted to Slack: {message_ts}")
			return Response(
				json.dumps({"ok": True, "ts": message_ts, "analysis": analysis}),
				status=200,
				mimetype="application/json"
			)
		else:
			logger.error("Failed to post build failure notification to Slack")
			return Response(
				json.dumps({"ok": False, "error": "Failed to post to Slack"}),
				status=500,
				mimetype="application/json"
			)
			
	except Exception as e:
		logger.error(f"Error processing build failure: {e}", exc_info=True)
		return Response(
			json.dumps({"ok": False, "error": str(e)}),
			status=500,
			mimetype="application/json"
		)


@bp.post("/llm/chat")
def llm_chat() -> Response:
	"""Handle LLM chat messages."""
	try:
		# Get message from request
		payload: Dict[str, Any] = request.get_json(force=True, silent=True) or {}
		
		message = payload.get("message", "")
		if not message:
			return Response(
				json.dumps({"ok": False, "error": "No message provided"}),
				status=400,
				mimetype="application/json"
			)
		
		logger.info(f"Sending message to LLM: {message[:100]}...")
		
		# Send to LLM and get response
		response = send_message_to_llm(message)
		
		logger.info(f"Received LLM response: {response[:100]}...")
		
		return Response(
			json.dumps({"ok": True, "response": response}),
			status=200,
			mimetype="application/json"
		)
		
	except Exception as e:
		logger.error(f"Error processing LLM chat: {e}", exc_info=True)
		return Response(
			json.dumps({"ok": False, "error": str(e)}),
			status=500,
			mimetype="application/json"
		)
