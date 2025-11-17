# Slackbot: GitHub PR Summaries & Build Failure Notifications

A Flask-based Slackbot that demonstrates Lab 1 output in production.

## What It Does

1. **PR Summaries:** Receives GitHub PR webhooks → Summarizes with LLM → Posts to Slack
2. **Build Failures:** Receives build logs → Uses Lab 1 hybrid approach → Posts formatted summary to Slack

## Connection to Lab 1

**Lab 1 showed:**
- Extract errors deterministically
- Send filtered sections to LLM
- Get structured JSON output

**Slackbot uses:**
- Same hybrid approach (`build_analysis.py`)
- Same error extraction logic
- Same LLM analysis
- Output goes to Slack instead of console

**Key Message:** "Lab 1 output powers production automation"

## Quick Start

### Prerequisites

- Python 3.8+
- Slack workspace with bot app created
- GitHub repository (for webhooks)
- LLM API access (OpenAI, Anthropic, or Ollama)

### Setup

```bash
# Install dependencies
pip install flask slack-sdk openai anthropic requests certifi

# Or use uv (if available)
uv venv
uv sync
```

### Configuration

Set environment variables:

```bash
# Required
export SLACKBOT_SLACK_BOT_TOKEN="xoxb-your-token"
export SLACKBOT_SLACK_DEFAULT_CHANNEL="#your-channel"
export SLACKBOT_OPENAI_API_KEY="sk-your-key"
export SLACKBOT_GITHUB_WEBHOOK_SECRET="your-secret"

# Optional
export SLACKBOT_GITHUB_TOKEN="ghp-your-token"
export SLACKBOT_GITHUB_REPO_FULLNAME="org/repo"
export SLACKBOT_OPENAI_MODEL="gpt-4o-mini"
export SLACKBOT_ENV_NAME="dev"
export SLACKBOT_PORT="8000"
```

### Run

```bash
# Option A: Direct
python -m src.slackbot.app

# Option B: Flask
flask --app src.slackbot.app run --host 0.0.0.0 --port 8000

# Option C: Gunicorn (production)
gunicorn -w 2 -b 0.0.0.0:8000 'src.slackbot.app:create_app()'
```

## Endpoints

### `/healthz`
Health check endpoint.

### `/github/webhook`
Receives GitHub PR webhooks, summarizes PRs, posts to Slack.

**Setup:**
1. Create GitHub webhook pointing to `https://your-host/github/webhook`
2. Set secret to `SLACKBOT_GITHUB_WEBHOOK_SECRET`
3. Select "Pull requests" events

### `/build/failure`
Receives build logs, analyzes using Lab 1 hybrid approach, posts to Slack.

**Example:**
```bash
curl -X POST http://localhost:8000/build/failure \
  -H "Content-Type: application/json" \
  -d '{
    "log": "error: unknown type name...",
    "repo": "rdk/telemetry",
    "branch": "main",
    "build_url": "https://jenkins.example.com/build/123"
  }'
```

See `build_test.http` for more examples.

## Architecture

```
GitHub Webhook → Flask App → LLM → Slack
Build Log API → Flask App → Lab 1 Code → Slack
```

**Key Files:**
- `src/slackbot/build_analysis.py` - Lab 1 hybrid approach
- `src/slackbot/routes.py` - Webhook handling
- `src/slackbot/slack_client.py` - Slack integration
- `src/slackbot/llm.py` - LLM calls

## Local Development

### Testing with ngrok

```bash
# In one terminal: Run Flask app
flask --app src.slackbot.app run --port 8000

# In another terminal: Expose with ngrok
ngrok http 8000

# Use ngrok URL for GitHub webhook
```

### Testing Build Failure Endpoint

Use `build_test.http` or curl:

```bash
curl -X POST http://localhost:8000/build/failure \
  -H "Content-Type: application/json" \
  -d @build_test.json
```

## Key Features

- ✅ **Hybrid Approach:** Uses Lab 1's deterministic filtering + LLM
- ✅ **Cost-Effective:** 70-90% token savings vs. full log analysis
- ✅ **Production-Ready:** Error handling, logging, signature verification
- ✅ **Modular:** Easy to extend with new endpoints

## Customization

### Add New Endpoints

Edit `src/slackbot/routes.py`:

```python
@bp.post("/your/endpoint")
def your_endpoint():
    # Your logic here
    pass
```

### Modify Build Analysis

Edit `src/slackbot/build_analysis.py` - same code as Lab 1!

### Change Slack Formatting

Edit `src/slackbot/slack_client.py` or `src/slackbot/routes.py`

## Troubleshooting

**Slackbot not running?**
- Check port 8000 is available
- Verify environment variables
- Check logs: `logs/slackbot.log` (if configured)

**No Slack message?**
- Verify bot is invited to channel: `/invite @YourBotName`
- Check `SLACKBOT_SLACK_DEFAULT_CHANNEL` is correct
- Verify Slack API token is valid

**Webhook not working?**
- Verify signature secret matches
- Check webhook URL is correct
- Use ngrok for local testing

## Connection to Course

**Part 2 Lab 1:** You built log analysis with hybrid approach  
**Part 4 Demo 4:** You saw this Slackbot in action  
**Now:** You have the code to run it yourself!

**Same Pattern:**
- Extract → Prompt → Structure
- Lab 1: Console output
- Slackbot: Slack output
- Your use case: Your output format

---

**This is Lab 1 output, in production!** 🚀
