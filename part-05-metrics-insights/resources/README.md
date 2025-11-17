# Part 5 Resources

This directory contains scripts and templates for Part 5: Metrics, Insights & Reporting.

## Files

### `pull_github_data.py`
Extract PR data from GitHub API or use sample data.

**Usage:**
```bash
# With GitHub API
python pull_github_data.py --repo org/repo --token YOUR_TOKEN --output github_data.json

# With sample data (for demo)
python pull_github_data.py --sample --output github_data.json
```

**Features:**
- Pulls PR data from GitHub API
- Calculates metrics (merge rate, lead time, etc.)
- Falls back to sample data if no API access
- Outputs structured JSON

**Demo Notes:**
- Use `--sample` flag if no GitHub API access
- Show structured output (JSON format)
- Point out metrics calculated automatically

### `pull_jira_data.py`
Extract ticket data from Jira CSV export or use sample data.

**Usage:**
```bash
# With Jira CSV export
python pull_jira_data.py --csv jira_export.csv --output jira_data.json

# With sample data (for demo)
python pull_jira_data.py --sample --output jira_data.json
```

**Features:**
- Reads Jira CSV exports
- Calculates metrics (resolution rate, avg resolution time)
- Groups by priority and component
- Falls back to sample data

**Demo Notes:**
- Use `--sample` flag if no Jira access
- Show component grouping (useful for health analysis)
- Point out resolution time calculations

### `generate_weekly_summary.py`
Generate weekly engineering summary using LLM.

**Usage:**
```bash
python generate_weekly_summary.py github_data.json jira_data.json --output weekly_summary.txt --track-usage
```

**Features:**
- Generates weekly summary with LLM
- Tracks token usage and costs
- Calculates ROI (time saved vs. cost)
- Outputs formatted summary

**Demo Notes:**
- Show token usage and cost tracking
- Demonstrate ROI calculation
- Point out structured output format
- Use `--track-usage` to log for cost analysis

### `sanity_check.py`
Verify AI-generated summary accuracy.

**Usage:**
```bash
python sanity_check.py weekly_summary.txt github_data.json jira_data.json
```

**Features:**
- Verifies PR/ticket counts match data
- Checks if mentioned risks exist
- Validates completeness
- Provides recommendations

**Demo Notes:**
- Show importance of verification
- Demonstrate checking numbers
- Point out prompt refinement suggestions

### `cost_tracking.py`
Track and analyze AI usage costs.

**Usage:**
```bash
# Weekly report
python cost_tracking.py --log ai_usage_log.json --period weekly

# Monthly report
python cost_tracking.py --log ai_usage_log.json --period monthly
```

**Features:**
- Analyzes usage log
- Breaks down costs by operation and model
- Calculates ROI estimates
- Generates cost reports

**Demo Notes:**
- Show cost breakdown by operation
- Demonstrate ROI calculation
- Point out cost optimization opportunities

### `weekly_summary_prompt.txt`
Prompt template for weekly summaries.

**Usage:**
- Reference during demo
- Use with Copilot Chat
- Customize for your context

### `component_health_prompt.txt`
Prompt template for component health analysis.

**Usage:**
- Use with LLM API or Copilot Chat
- Customize thresholds for your context
- Adapt scoring formula as needed

## Demo Flow

### Exercise 5.1: Data Extraction (15 min)
1. Run `pull_github_data.py --sample`
2. Run `pull_jira_data.py --sample`
3. Review JSON output structure
4. Show metrics calculated automatically

### Exercise 5.2: Generate Summary (20 min)
1. Show `weekly_summary_prompt.txt`
2. Run `generate_weekly_summary.py`
3. Show token usage and cost
4. Calculate ROI

### Exercise 5.3: Sanity Check (10 min)
1. Run `sanity_check.py`
2. Show verification process
3. Discuss prompt refinement

## Key Connections

### Connection to Lab 1:
- Lab 1: Extract → Prompt → Structure
- Part 5: Extract → Prompt → Structure
- **Same pattern:** Data extraction → LLM analysis → Structured output

### Connection to Part 2:
- Part 2 argument: "Most AI tools are LLM wrappers"
- Part 5: Building your own metrics tool
- **You can build this yourself**

### Connection to Part 3:
- Part 3: Verify AI output
- Part 5: Sanity check summary
- **Same principle:** Don't trust blindly

## Tips for Instructors

1. **Use sample data:** If no API access, use `--sample` flags
2. **Show cost tracking:** Emphasize ROI calculation
3. **Demonstrate verification:** Show sanity check process
4. **Connect to their context:** Use their actual metrics if possible
5. **Emphasize pattern:** Same Extract → Prompt → Structure pattern

## Customization for RDK Context

### GitHub Data:
- Update repo name to `rdkcentral/telemetry` (example)
- Add component labels if available
- Include BD ticket references

### Jira Data:
- Use BD-1290 format tickets
- Include component names (telemetry, hal, etc.)
- Add compliance/license labels

### Summary Format:
- Include component health metrics
- Reference BD tickets
- Format for RDK Slack channels

## Troubleshooting

**No GitHub API access?**
- Use `--sample` flag
- Focus on the pattern, not the data source

**No Jira access?**
- Use `--sample` flag
- Show CSV import process conceptually

**LLM API errors?**
- Use sample summary output
- Focus on cost tracking and verification

**Time pressure?**
- Focus on Exercise 5.2 (summary generation)
- Skip sanity check if needed
- Emphasize: "Same pattern as Lab 1"

