# Slackbot Demo Guide - Part 4

This guide shows how to demonstrate the Slackbot in Part 4, connecting Lab 1 output to production automation.

## What the Slackbot Does

The Slackbot demonstrates **two key features**:

1. **PR Summaries** (GitHub webhook → Slackbot → Slack)
   - Receives GitHub PR webhooks
   - Summarizes PRs with LLM
   - Posts formatted summaries to Slack

2. **Build Failure Notifications** (Build log → Slackbot → Slack)
   - Receives build logs via API
   - Uses Lab 1's hybrid log analysis approach
   - Posts formatted analysis to Slack

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

## Demo Setup

### Prerequisites

1. **Slackbot running:**
   ```bash
   cd slackbot
   uv run slackbot
   # Or: uv run flask --app slackbot.app run --host 0.0.0.0 --port 8000
   ```

2. **Environment variables set:**
   - `SLACKBOT_SLACK_BOT_TOKEN`
   - `SLACKBOT_SLACK_DEFAULT_CHANNEL`
   - `SLACKBOT_OPENAI_API_KEY`
   - `SLACKBOT_GITHUB_WEBHOOK_SECRET` (for PR webhooks)

3. **Slack bot invited to channel:**
   - `/invite @YourBotName` in Slack

### Demo 1: Build Failure Notification (5 min)

**Show:** Lab 1 output → Slackbot → Slack

**Steps:**
1. Show `build_analysis.py` - "Same hybrid approach as Lab 1"
2. Use `build_test.http` to send build log
3. Show Slack message with formatted analysis
4. Point out: "This is Lab 1's JSON output, formatted for Slack"

**Key Points:**
- Same pattern: Extract → Prompt → Structure
- Automated: Runs on webhook/API call
- Cost-effective: Uses hybrid approach (70-90% savings)
- Production-ready: Error handling, logging

### Demo 2: PR Summary (5 min)

**Show:** GitHub webhook → Slackbot → Slack

**Steps:**
1. Show GitHub webhook configuration
2. Create test PR (or use existing)
3. Show Slack message with PR summary
4. Point out: "Automated PR summaries - no manual Copilot Chat"

**Key Points:**
- Automated vs. manual (Copilot Chat)
- Webhook-based integration
- Same LLM, different context

## Code Walkthrough

### `build_analysis.py` - Lab 1 Connection

**Show them:**
```python
# Same hybrid approach as Lab 1
def extract_errors(log_content):
    # Deterministic filtering
    ...

def analyze_build_log(log_content, build_info):
    # Extract errors
    # Send to LLM
    # Return structured JSON
    # Same as Lab 1!
```

**Say:** "This is Lab 1's hybrid approach, in production."

### `routes.py` - Webhook Handling

**Show them:**
```python
@bp.post("/build/failure")
def build_failure():
    # Receive build log
    # Call build_analysis.py (Lab 1 code!)
    # Format for Slack
    # Post message
```

**Say:** "Lab 1 output → Slack notification. Automated."

### `slack_client.py` - Message Formatting

**Show them:**
```python
# Formats Lab 1 JSON output for Slack
# Adds emojis, formatting
# Posts to channel
```

**Say:** "Same data, different format. Slack instead of console."

## Key Talking Points

### Connection to Lab 1:
- "Lab 1 showed you how to extract errors and analyze with LLM"
- "Slackbot uses the same code (`build_analysis.py`)"
- "Lab 1 output → Slack notification. That's the connection."

### Automated vs. Manual:
- **Copilot Chat:** Manual, one-off analysis
- **Slackbot:** Automated, runs on webhooks
- **Both use LLMs:** Same pattern, different context

### Production Considerations:
- Error handling (what if LLM fails?)
- Logging (audit trail)
- Cost control (hybrid approach)
- Security (webhook signature verification)

## Exercise: Test Slackbot

**Task:** Test the Slackbot endpoints.

**Option A: Build Failure**
```bash
# Use build_test.http
# Or curl:
curl -X POST http://localhost:8000/build/failure \
  -H "Content-Type: application/json" \
  -d '{
    "log": "error: unknown type name...",
    "repo": "rdk/telemetry",
    "branch": "main"
  }'
```

**Option B: PR Summary**
- Configure GitHub webhook
- Create test PR
- Show Slack message

## Troubleshooting

**Slackbot not running?**
- Check port 8000 is available
- Verify environment variables
- Check logs: `logs/slackbot.log`

**No Slack message?**
- Verify bot is invited to channel
- Check `SLACKBOT_SLACK_DEFAULT_CHANNEL` is correct
- Check Slack API token is valid

**Webhook not working?**
- Verify signature secret matches
- Check webhook URL is correct
- Use ngrok for local testing

## Integration Points

### With Lab 1:
- **Lab 1:** Extract errors → LLM → JSON
- **Slackbot:** Same code → Format → Slack

### With Part 2:
- **Part 2 argument:** "Most AI tools are LLM wrappers"
- **Slackbot:** You built your own LLM wrapper

### With Part 3:
- **Part 3:** Evidence required
- **Slackbot:** Includes evidence in Slack messages

### With Part 5:
- **Part 5:** Track costs
- **Slackbot:** Logs token usage for cost tracking

## Next Steps

After demo, discuss:
1. What other webhooks could you add?
2. How would you integrate this into Jenkins?
3. What other Slack notifications would be useful?
4. How would you track costs for automated webhooks?

