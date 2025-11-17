from __future__ import annotations

import logging
import ssl
from typing import Optional

import certifi
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

logger = logging.getLogger(__name__)


class SlackMessenger:
	def __init__(self, token: str) -> None:
		# Create SSL context with certifi certificates
		ssl_context = ssl.create_default_context(cafile=certifi.where())
		self.client = WebClient(token=token, ssl=ssl_context)

	def post_message(self, *, channel: str, text: str) -> Optional[str]:
		"""Post a message to Slack channel.
		
		Args:
			channel: Channel name (e.g., '#rdk-builds') or channel ID
			text: Message text to send
			
		Returns:
			Message timestamp if successful, None otherwise
		"""
		try:
			resp = self.client.chat_postMessage(channel=channel, text=text)
			if resp.get("ok"):
				ts = resp.get("ts")
				logger.info(f"Message posted to {channel}: {ts}")
				return ts
			else:
				error = resp.get("error", "unknown error")
				logger.error(f"Failed to post message to {channel}: {error}")
				return None
		except SlackApiError as e:
			logger.error(f"Slack API error posting to {channel}: {e.response.get('error', str(e))}")
			return None
		except Exception as e:
			logger.error(f"Unexpected error posting to {channel}: {e}")
			return None

	def post_pr_summary(self, *, channel: str, summary: str) -> Optional[str]:
		"""Post a PR summary to Slack channel (legacy method name).
		
		Args:
			channel: Channel name (e.g., '#rdk-builds') or channel ID
			summary: PR summary text to send
			
		Returns:
			Message timestamp if successful, None otherwise
		"""
		return self.post_message(channel=channel, text=summary)
