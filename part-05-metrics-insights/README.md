# Part 5: Metrics, Insights & Reporting

**Duration:** 45 minutes (15:00-15:45)  
**Format:** Lab 4 - Hands-on

## Learning Objectives

By the end of this section, participants will:
- Understand what can be measured (DORA metrics, team productivity)
- Use AI and LLM scripting to generate actionable insights
- Compile GitHub PR and ticket data into concise summaries
- Track costs (tokens, runtime) for AI operations
- Create reproducible reporting workflows

## Key Topics

- What can be measured: DORA metrics and team productivity
- Using AI and LLM scripting to generate actionable insights
- Hands-on: compiling GitHub PR and ticket data into concise summaries for decision-makers

## Lab 4: Metrics & Reporting (45 minutes)

### Objectives
- Pull data from GitHub and Jira
- Use AI to generate a single-page decision brief for managers
- Include cost tracking for AI operations
- Create a reproducible workflow

### Materials Provided
- Sample GitHub PR/issue data (CSV/JSON)
- Sample Jira export (CSV/JSON)
- Sample Slack message data (optional)
- Python script templates

### Exercise 5.1: Data Extraction (15 minutes)

**Task:** Pull relevant data from GitHub and Jira.

**GitHub Data (via API or export):**
```python
# Example: Extract PR data
import requests
import json

# GitHub API call (or use exported data)
def get_pr_data(repo, token):
    url = f"https://api.github.com/repos/{repo}/pulls"
    headers = {"Authorization": f"token {token}"}
    response = requests.get(url, headers=headers, params={"state": "all"})
    return response.json()

# Extract key fields
prs = get_pr_data("org/repo", "your-token")
pr_summary = []
for pr in prs[:10]:  # Last 10 PRs
    pr_summary.append({
        "number": pr["number"],
        "title": pr["title"],
        "state": pr["state"],
        "created": pr["created_at"],
        "merged": pr.get("merged_at"),
        "labels": [l["name"] for l in pr["labels"]],
        "files_changed": pr["changed_files"],
        "additions": pr["additions"],
        "deletions": pr["deletions"]
    })

print(json.dumps(pr_summary, indent=2))
```

**Jira Data (from export):**
```python
import pandas as pd

# Read Jira export (CSV)
jira_df = pd.read_csv("jira_export.csv")

# Extract key fields
jira_summary = jira_df[[
    "Issue key",
    "Summary",
    "Status",
    "Created",
    "Resolved",
    "Priority",
    "Assignee"
]].to_dict("records")

print(json.dumps(jira_summary[:10], indent=2, default=str))
```

**Deliverable:** Structured data (JSON) with:
- PR titles, states, labels, file counts
- Jira ticket keys, status, priority, assignee
- Timeline data (created, merged, resolved)

### Exercise 5.2: AI-Generated Weekly Summary (20 minutes)

**Task:** Use an LLM to produce a concise weekly summary with risks and next actions.

**Prompt Template:**
```
You are analyzing engineering metrics for a weekly report to managers.

GitHub PR Data:
{pr_data}

Jira Ticket Data:
{jira_data}

Generate a single-page weekly engineering brief that includes:

1. **Summary** (2-3 sentences)
   - Overall team velocity
   - Key accomplishments
   - Any blockers

2. **Metrics** (bullet points)
   - PRs opened/merged this week
   - Average PR size (files changed)
   - PR cycle time (if available)
   - Open tickets by priority

3. **Risks & Blockers** (bullet points)
   - Anything blocking progress
   - High-priority items needing attention
   - Security/license concerns

4. **Next Actions** (bullet points)
   - What to focus on next week
   - Any decisions needed from managers

Keep it concise (one page, <500 words). Use data-driven language.
Format for Slack/Teams (can paste directly).
```

**Implementation:**
```python
import openai  # or ollama, anthropic, etc.

def generate_weekly_summary(pr_data, jira_data, model="gpt-4"):
    prompt = f"""
    [PASTE PROMPT TEMPLATE HERE]
    """.format(pr_data=json.dumps(pr_data), jira_data=json.dumps(jira_data))
    
    # Track tokens for cost
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3  # Lower temperature for consistent output
    )
    
    summary = response.choices[0].message.content
    tokens_used = response.usage.total_tokens
    
    # Calculate cost (example for GPT-4)
    cost = tokens_used * 0.03 / 1000  # $0.03 per 1K tokens (example)
    
    return summary, tokens_used, cost

# Generate summary
summary, tokens, cost = generate_weekly_summary(pr_summary, jira_summary)
print(summary)
print(f"\n---\nTokens used: {tokens}\nEstimated cost: ${cost:.4f}")
```

**Deliverable:** 
- Weekly summary (text, ready for Slack/Teams)
- Token usage and cost estimate

### Exercise 5.3: Sanity Check & Refinement (10 minutes)

**Task:** Verify AI summary against raw data and refine.

**Sanity check:**
1. **Verify numbers:** Do PR counts match raw data?
2. **Check accuracy:** Are risks/blockers actually present in data?
3. **Completeness:** Did AI miss important items?

**Example check:**
```python
# Count PRs manually
manual_pr_count = len([p for p in prs if p["state"] == "merged"])
# Verify AI mentioned this number correctly

# Check for mentioned risks in data
mentioned_risks = ["security", "blocker", "urgent"]
found_risks = []
for pr in prs:
    if any(risk in pr["title"].lower() for risk in mentioned_risks):
        found_risks.append(pr["number"])

print(f"AI mentioned risks. Found in data: {found_risks}")
```

**Refinement:**
- If numbers don't match, adjust prompt to request citations
- If risks are missed, add explicit instruction to check all data
- If summary is too verbose, add length constraint

**Deliverable:** Refined prompt that produces more accurate summaries.

## Discussion: What Can Be Measured

### DORA Metrics (DevOps Research and Assessment)

**The Four Key Metrics:**
1. **Deployment Frequency:** How often do you deploy?
2. **Lead Time:** Time from commit to production
3. **Mean Time to Recovery (MTTR):** How quickly can you fix failures?
4. **Change Failure Rate:** What percentage of changes cause failures?

**How AI can help measure:**
- **Deployment Frequency:** Analyze GitHub releases/deployments
- **Lead Time:** Calculate time from PR creation to merge to deploy
- **MTTR:** Analyze incident response times from logs/issues
- **Change Failure Rate:** Track PRs that required hotfixes

**Example calculation:**
```python
# Calculate lead time
def calculate_lead_time(pr):
    created = datetime.fromisoformat(pr["created_at"])
    merged = datetime.fromisoformat(pr["merged_at"])
    lead_time = (merged - created).total_seconds() / 3600  # hours
    return lead_time

lead_times = [calculate_lead_time(pr) for pr in prs if pr.get("merged_at")]
avg_lead_time = sum(lead_times) / len(lead_times)
print(f"Average lead time: {avg_lead_time:.1f} hours")
```

### Team Productivity Metrics

**From callnotes:** Team wants to extract meaningful information from GitHub/Jira.

**What to measure:**
- **PR throughput:** PRs opened/merged per week
- **Code review time:** Time from PR creation to approval
- **Ticket resolution:** Average time to close Jira tickets
- **Component health:** Identify components with many issues (from callnotes)

**AI can help identify:**
- Components with high failure rates
- Trends (improving vs. degrading)
- Anomalies (sudden spikes in issues)

**Example from callnotes:**
> "Sucking a lot of metrics from Github - a great amount of info, an AI to make sense -> this component is not healthy"

**AI prompt:**
```
Analyze GitHub PR and issue data to identify unhealthy components.

Data: [PR/issues with component labels]

For each component, calculate:
1. Number of PRs/issues in last 30 days
2. Average time to resolution
3. Number of failed builds
4. Number of security issues

Flag components as "unhealthy" if they exceed thresholds:
- >10 issues in 30 days
- >7 days average resolution time
- >3 failed builds
- >1 security issue

Rank components by health score.
```

### Component Health Analysis

**From callnotes:** 
- Team manages codebase for Comcast/Sky with community users
- Need to identify which components are not healthy

**AI-assisted health analysis:**

**Data sources:**
- GitHub: PRs, issues, build failures
- Jira: Tickets by component
- CI/CD: Build success rates

**Health indicators:**
- High issue count
- Slow resolution times
- Frequent build failures
- Security vulnerabilities
- Low test coverage

**AI prompt:**
```
Analyze component health from the following data:

Components and their metrics:
- Component A: 15 issues, avg resolution 5 days, 2 build failures
- Component B: 3 issues, avg resolution 2 days, 0 build failures
...

For each component, provide:
1. Health score (0-100)
2. Health status (Healthy/At Risk/Unhealthy)
3. Top 3 concerns
4. Recommended actions

Format as a dashboard-ready summary.
```

## Discussion Questions

1. **Metrics that Matter:**
   - What metrics would be most valuable for your team?
   - DORA metrics? Component health? Something else?

2. **Reporting Frequency:**
   - How often would you generate these reports? (Daily? Weekly? Monthly?)
   - Who is the audience? (Team? Managers? Executives?)

3. **Data Sources:**
   - What data do you have access to? (GitHub? Jira? Slack? Other?)
   - How would you combine multiple sources?

4. **Cost vs. Value:**
   - Is the cost of AI-generated reports worth the time saved?
   - How would you justify the cost to management?

## Key Details to Explore

### Actionable Insights Generation

**What makes insights "actionable":**
- Specific: "Component X has 15 open issues" not "many issues"
- Prioritized: Focus on high-impact items first
- Contextual: Explain why it matters
- Time-bound: Include deadlines or urgency

**AI prompt structure:**
```
Generate actionable insights from this data:

[PASTE DATA]

For each insight, provide:
1. **What:** Specific finding
2. **Why:** Why it matters
3. **Impact:** High/Medium/Low
4. **Action:** What to do about it
5. **Owner:** Who should act (if known)
6. **Timeline:** When to address (if urgent)
```

### Cost Tracking

**From callnotes:** Team is "at the edge of AI becoming more expensive"

**What to track:**
- **Tokens per operation:** Log token usage for each AI call
- **Cost per report:** Calculate total cost for weekly/monthly reports
- **Cost per use case:** Compare costs across different AI tasks

**Example tracking:**
```python
# Track AI usage
ai_usage_log = []

def track_ai_usage(operation, tokens, cost, model):
    ai_usage_log.append({
        "timestamp": datetime.now().isoformat(),
        "operation": operation,  # "weekly_summary", "log_analysis", etc.
        "tokens": tokens,
        "cost": cost,
        "model": model
    })

# Generate weekly cost report
def weekly_cost_report():
    weekly_total = sum(entry["cost"] for entry in ai_usage_log 
                       if entry["timestamp"] > (datetime.now() - timedelta(days=7)).isoformat())
    
    print(f"Weekly AI cost: ${weekly_total:.2f}")
    print(f"Cost per operation:")
    for op in set(e["operation"] for e in ai_usage_log):
        op_cost = sum(e["cost"] for e in ai_usage_log if e["operation"] == op)
        print(f"  {op}: ${op_cost:.2f}")

# Add to weekly summary
weekly_summary += f"\n\nAI Cost This Week: ${weekly_total:.2f}"
```

**Cost optimization:**
- Use cheaper models for routine tasks (summaries, triage)
- Reserve expensive models for high-value tasks
- Cache results when possible (don't regenerate same report)

### Reproducible Workflows

**Make it scriptable:**
```bash
#!/bin/bash
# weekly-report.sh

# Pull data
python pull_github_data.py > github_data.json
python pull_jira_data.py > jira_data.json

# Generate summary
python generate_summary.py github_data.json jira_data.json > weekly_summary.txt

# Post to Slack (optional)
python post_to_slack.py weekly_summary.txt
```

**Make it scheduled:**
- GitHub Actions: Run weekly on Monday
- Cron: Local scheduling
- CI/CD: Integrate into existing pipelines

**Make it version-controlled:**
- Store scripts in repository
- Track prompt changes (version control for prompts)
- Log outputs (for audit/comparison)

### Integration with Existing Tools

**From callnotes:**
- Team uses **Jira** for tickets
- Team uses **Slack** for communication
- Team uses **GitHub** for code

**Workflow integration:**

**1. GitHub → Jira Mapping:**
```python
# Extract Jira references from PR titles/descriptions
import re

def extract_jira_keys(text):
    # Match patterns like PROJ-123, JIRA-456
    pattern = r'([A-Z]+-\d+)'
    return re.findall(pattern, text)

# Map PRs to Jira tickets
pr_jira_map = {}
for pr in prs:
    jira_keys = extract_jira_keys(pr["title"] + " " + pr.get("body", ""))
    pr_jira_map[pr["number"]] = jira_keys
```

**2. Slack Integration:**
```python
# Post summary to Slack
import requests

def post_to_slack(text, webhook_url):
    payload = {"text": text}
    response = requests.post(webhook_url, json=payload)
    return response.status_code == 200

# Format for Slack
slack_summary = f"*Weekly Engineering Brief*\n\n{summary}"
post_to_slack(slack_summary, SLACK_WEBHOOK_URL)
```

**3. Health Metrics to Slack:**
From callnotes: "Health metric - CMF?" and "AI Slack bot"

**Example:**
```python
# Component health alert to Slack
def alert_unhealthy_components(components):
    unhealthy = [c for c in components if c["health_status"] == "Unhealthy"]
    
    if unhealthy:
        message = "*🚨 Unhealthy Components Detected*\n\n"
        for comp in unhealthy:
            message += f"• *{comp['name']}*: {comp['issues']} issues, {comp['concerns'][0]}\n"
        
        post_to_slack(message, SLACK_WEBHOOK_URL)
```

## Transition to Part 6

Next: **Reflection & Planning**
- Key takeaways and opportunities
- Roadmap for responsible AI adoption
- Resources for experimenting with different LLMs

