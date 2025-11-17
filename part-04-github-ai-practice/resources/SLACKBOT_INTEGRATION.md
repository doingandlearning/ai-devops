# Slackbot Integration Guide - Part 4

## Where the Slackbot Fits

**Part 4: GitHub & AI in Practice (12:15-13:00)**

**Demo 4: Slackbot Integration - Lab 1 Output in Action (10 minutes)**

**Timing:** After Demo 3 (Log Analysis), before GitHub AI Integrations overview

## Why Here?

1. **Connects Lab 1 to Production:** Shows Lab 1's hybrid approach in action
2. **Shows Automation:** Demonstrates automated vs. manual (Copilot Chat)
3. **Completes the Story:** Lab 1 → Part 4 → Production automation
4. **Practical Example:** Real working code they can use

## What the Slackbot Demonstrates

### Feature 1: Build Failure Notifications
- **Input:** Build log (via API)
- **Process:** Lab 1's hybrid log analysis (`build_analysis.py`)
- **Output:** Formatted Slack message with root causes
- **Connection:** Uses same code as Lab 1

### Feature 2: PR Summaries
- **Input:** GitHub PR webhook
- **Process:** LLM summarizes PR changes
- **Output:** Formatted Slack message
- **Connection:** Automated version of Copilot Chat

## Demo Flow

### Step 1: Show Architecture (2 min)
```
GitHub Webhook → Flask App → LLM → Slack
Build Log API → Flask App → Lab 1 Code → Slack
```

**Say:** "This is Lab 1 output, automated."

### Step 2: Demo Build Failure (3 min)
- Use `build_test.http` to trigger endpoint
- Show Slack message
- Point out: "Same hybrid approach as Lab 1"

### Step 3: Show Code Connection (3 min)
- Open `build_analysis.py` - same as Lab 1
- Show `routes.py` - webhook handling
- **Key:** "You built this in Lab 1. This is it in production."

### Step 4: Demo PR Summary (2 min)
- Show GitHub webhook → Slack flow
- **Key:** "Automated PR summaries - no manual Copilot Chat"

## Key Messages

1. **Same Pattern:** Extract → Prompt → Structure (Lab 1)
2. **Automated:** Runs on webhooks, no manual intervention
3. **Cost-Effective:** Uses hybrid approach (70-90% savings)
4. **Production-Ready:** Error handling, logging, security

## Connection Points

### To Lab 1:
- **Lab 1:** Extract errors → LLM → JSON
- **Slackbot:** Same code → Format → Slack

### To Part 2:
- **Part 2 argument:** "Most AI tools are LLM wrappers"
- **Slackbot:** You built your own LLM wrapper

### To Part 3:
- **Part 3:** Evidence required
- **Slackbot:** Includes evidence in messages

### To Part 5:
- **Part 5:** Track costs
- **Slackbot:** Logs token usage

## Setup Instructions

### Prerequisites:
1. Slackbot running (`uv run slackbot`)
2. Environment variables set
3. Slack bot invited to channel
4. `build_test.http` ready

### Quick Test:
```bash
# Test build failure endpoint
curl -X POST http://localhost:8000/build/failure \
  -H "Content-Type: application/json" \
  -d @build_test.json
```

## Files to Reference

- `slackbot/src/slackbot/build_analysis.py` - Lab 1 hybrid approach
- `slackbot/src/slackbot/routes.py` - Webhook handling
- `slackbot/build_test.http` - Test endpoint
- `slackbot/README.md` - Setup instructions

## Talking Points

**Opening:**
> "You've seen Lab 1's hybrid log analysis. Now let's see it in production - automated Slack notifications."

**During Demo:**
> "This uses Lab 1's hybrid approach. Same code, different output format."

**Closing:**
> "Lab 1 output → Slack notification. That's the connection. You can automate anything with this pattern."

