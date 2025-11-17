from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
	model_config = SettingsConfigDict(env_prefix="SLACKBOT_", env_file=".env", case_sensitive=False)

	# General
	env_name: str = "dev"
	port: int = 8000

	# GitHub
	github_webhook_secret: SecretStr
	github_token: SecretStr | None = None  # optional for enrichment
	github_repo_fullname: str | None = None  # e.g. "org/repo" (optional filter)

	# Slack
	slack_bot_token: SecretStr
	slack_default_channel: str

	# LLM
	openai_api_key: SecretStr
	openai_model: str = "gpt-4o-mini"
