#!/usr/bin/env python3
"""
Generate Weekly Engineering Summary with AI
Example script for Part 5: Metrics & Reporting

Usage:
    python generate_weekly_summary.py github_data.json jira_data.json --output weekly_summary.txt
"""

import argparse
import json
import os
import sys
from datetime import datetime
from typing import Dict, List

try:
    from openai import OpenAI
except ImportError:
    print("Error: openai package not installed. Run: pip install openai")
    sys.exit(1)


def load_data(github_file: str, jira_file: str) -> tuple:
    """Load GitHub and Jira data from JSON files."""
    with open(github_file, 'r') as f:
        github_data = json.load(f)
    
    with open(jira_file, 'r') as f:
        jira_data = json.load(f)
    
    return github_data, jira_data


def create_prompt(github_data: Dict, jira_data: Dict) -> str:
    """Create prompt for weekly summary."""
    # Extract key metrics
    github_metrics = github_data.get("metrics", {})
    jira_metrics = jira_data.get("metrics", {})
    
    # Format PR data (last 10)
    prs = github_data.get("prs", [])[:10]
    pr_summary = "\n".join([
        f"- PR #{p['number']}: {p['title']} ({p['state']}, {p['files_changed']} files changed)"
        for p in prs
    ])
    
    # Format ticket data (last 10)
    tickets = jira_data.get("tickets", [])[:10]
    ticket_summary = "\n".join([
        f"- {t['key']}: {t['summary']} ({t['status']}, Priority: {t.get('priority', 'N/A')})"
        for t in tickets
    ])
    
    prompt = f"""You are analyzing engineering metrics for a weekly report to managers.

GitHub PR Data (last 10 PRs):
{pr_summary}

GitHub Metrics:
- Total PRs: {github_metrics.get('total_prs', 0)}
- Merged: {github_metrics.get('merged_count', 0)}
- Open: {github_metrics.get('open_count', 0)}
- Merge rate: {github_metrics.get('merge_rate', 0):.1%}
- Avg lead time: {github_metrics.get('avg_lead_time_days', 'N/A')} days
- Avg files changed: {github_metrics.get('avg_files_changed', 0):.1f}

Jira Ticket Data (last 10 tickets):
{ticket_summary}

Jira Metrics:
- Total tickets: {jira_metrics.get('total_tickets', 0)}
- Resolved: {jira_metrics.get('resolved_count', 0)}
- Open: {jira_metrics.get('open_count', 0)}
- Resolution rate: {jira_metrics.get('resolution_rate', 0):.1%}
- Avg resolution time: {jira_metrics.get('avg_resolution_time_days', 'N/A')} days

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
"""
    
    return prompt


def generate_summary(prompt: str, api_key: str = None, model: str = "gpt-4o") -> tuple:
    """Generate summary using LLM."""
    if not api_key:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
    
    client = OpenAI(api_key=api_key)
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an engineering metrics analyst. Generate concise, data-driven summaries."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3  # Lower temperature for consistent output
        )
        
        summary = response.choices[0].message.content
        tokens_used = response.usage.total_tokens
        
        # Calculate cost (approximate - adjust based on model)
        # GPT-4o: ~$0.005 per 1K input tokens, ~$0.015 per 1K output tokens
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens
        
        if "gpt-4o" in model.lower():
            cost = (input_tokens * 0.005 + output_tokens * 0.015) / 1000
        elif "gpt-4" in model.lower():
            cost = (input_tokens * 0.03 + output_tokens * 0.06) / 1000
        else:
            cost = tokens_used * 0.002 / 1000  # Default estimate
        
        return summary, tokens_used, cost, {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": tokens_used
        }
        
    except Exception as e:
        print(f"Error calling LLM: {e}", file=sys.stderr)
        raise


def track_usage(operation: str, tokens: int, cost: float, model: str, output_file: str = "ai_usage_log.json"):
    """Track AI usage for cost analysis."""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "operation": operation,
        "tokens": tokens,
        "cost": cost,
        "model": model
    }
    
    # Load existing log
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            log = json.load(f)
    else:
        log = []
    
    log.append(log_entry)
    
    # Save updated log
    with open(output_file, 'w') as f:
        json.dump(log, f, indent=2)
    
    return log_entry


def main():
    parser = argparse.ArgumentParser(description="Generate weekly engineering summary")
    parser.add_argument("github_data", help="GitHub data JSON file")
    parser.add_argument("jira_data", help="Jira data JSON file")
    parser.add_argument("--output", default="weekly_summary.txt", help="Output file")
    parser.add_argument("--api-key", help="OpenAI API key (or set OPENAI_API_KEY env var)")
    parser.add_argument("--model", default="gpt-4o", help="LLM model to use")
    parser.add_argument("--track-usage", action="store_true", help="Track usage in log file")
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("Weekly Engineering Summary Generator")
    print("=" * 70)
    
    # Load data
    print(f"\n📊 Loading data...")
    github_data, jira_data = load_data(args.github_data, args.jira_data)
    print(f"   GitHub: {len(github_data.get('prs', []))} PRs")
    print(f"   Jira: {len(jira_data.get('tickets', []))} tickets")
    
    # Create prompt
    print(f"\n📝 Creating prompt...")
    prompt = create_prompt(github_data, jira_data)
    prompt_size = len(prompt)
    print(f"   Prompt size: {prompt_size:,} characters")
    
    # Generate summary
    print(f"\n🤖 Generating summary with {args.model}...")
    try:
        summary, tokens, cost, usage_details = generate_summary(
            prompt, args.api_key, args.model
        )
        
        print(f"   ✅ Summary generated")
        print(f"   📊 Tokens used: {tokens:,}")
        print(f"      Input: {usage_details['input_tokens']:,}")
        print(f"      Output: {usage_details['output_tokens']:,}")
        print(f"   💰 Estimated cost: ${cost:.4f}")
        
        # Track usage
        if args.track_usage:
            track_usage("weekly_summary", tokens, cost, args.model)
            print(f"   📝 Usage logged to ai_usage_log.json")
        
    except Exception as e:
        print(f"   ❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Save summary
    with open(args.output, 'w') as f:
        f.write(summary)
        f.write(f"\n\n---\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n")
        f.write(f"Tokens used: {tokens:,}\n")
        f.write(f"Estimated cost: ${cost:.4f}\n")
    
    print(f"\n✅ Summary saved to {args.output}")
    print(f"\n📋 Summary Preview:")
    print("-" * 70)
    print(summary[:500] + "..." if len(summary) > 500 else summary)
    print("-" * 70)
    
    # ROI calculation
    print(f"\n💰 ROI Analysis:")
    print(f"   Cost per summary: ${cost:.4f}")
    print(f"   Estimated time saved: 2 hours (manual summary)")
    print(f"   Engineer cost/hour: $100 (example)")
    print(f"   Time value saved: $200")
    print(f"   ROI: ${200 - cost:.2f} per summary ✅")


if __name__ == '__main__':
    main()

