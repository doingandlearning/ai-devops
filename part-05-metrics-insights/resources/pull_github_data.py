#!/usr/bin/env python3
"""
Pull GitHub PR and Issue Data
Example script for Part 5: Metrics & Reporting

Usage:
    python pull_github_data.py --repo org/repo --token YOUR_TOKEN --output github_data.json
    # Or use sample data if no token:
    python pull_github_data.py --sample
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional

try:
    import requests
except ImportError:
    print("Error: requests package not installed. Run: pip install requests")
    sys.exit(1)

# Set up logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


def get_pr_data(repo: str, token: Optional[str] = None, days: int = 30, max_pages: int = 10, filter_by: str = "updated") -> List[Dict]:
    """Pull PR data from GitHub API.
    
    Args:
        repo: Repository in format org/repo
        token: GitHub API token
        days: Number of days of history to fetch
        max_pages: Maximum number of pages to fetch (default 10 = 1000 PRs max)
        filter_by: Filter by "updated" (updated_at) or "created" (created_at). Default: "updated"
    """
    if not token:
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            print("Warning: No GitHub token provided. Using sample data.")
            return get_sample_pr_data()
    
    url = f"https://api.github.com/repos/{repo}/pulls"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Calculate cutoff date
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
    
    # Determine sort field based on filter
    if filter_by == "created":
        sort_field = "created"
        date_field = "created_at"
    else:
        sort_field = "updated"
        date_field = "updated_at"
    
    params = {
        "state": "all",
        "sort": sort_field,
        "direction": "desc",
        "per_page": 100
    }
    
    all_prs = []
    page = 1
    found_old_pr = False
    
    filter_type = "created" if filter_by == "created" else "updated"
    print(f"Fetching PRs {filter_type} since {cutoff_date.date()}...", end="", flush=True)
    
    while page <= max_pages:
        params["page"] = page
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            prs = response.json()
            
            if not prs:
                break
            
            # Filter by date
            filtered_prs = []
            page_has_recent_prs = False
            for pr in prs:
                # Use the appropriate date field based on filter_by
                pr_date = datetime.fromisoformat(pr[date_field].replace("Z", "+00:00"))
                if pr_date >= cutoff_date:
                    filtered_prs.append(pr)
                    page_has_recent_prs = True
                else:
                    # PRs are sorted by the date field descending, so if we find one older,
                    # all subsequent PRs in this page will be older too
                    # But we still need to check if this page had any recent PRs
                    break
            
            all_prs.extend(filtered_prs)
            print(f".", end="", flush=True)  # Progress indicator
            
            # Stop if:
            # 1. This page had no recent PRs (all PRs were older than cutoff) AND
            #    we've already found some PRs (meaning we've covered the recent period)
            # 2. OR this was the last page
            if (not page_has_recent_prs and len(all_prs) > 0) or len(prs) < 100:
                if not page_has_recent_prs:
                    found_old_pr = True
                break
            
            page += 1
            
        except requests.exceptions.RequestException as e:
            print(f"\nError fetching PRs: {e}", file=sys.stderr)
            return get_sample_pr_data()
    
    print(f" Done! Fetched {len(all_prs)} PRs from {page} page(s).")
    
    if page >= max_pages and not found_old_pr:
        print(f"⚠️  Warning: Reached max pages limit ({max_pages}). Some recent PRs may be missing.")
    
    return all_prs


def extract_pr_summary(prs: List[Dict]) -> List[Dict]:
    """Extract key fields from PR data."""
    summary = []
    
    for pr in prs:
        created = datetime.fromisoformat(pr["created_at"].replace("Z", "+00:00"))
        merged = None
        if pr.get("merged_at"):
            merged = datetime.fromisoformat(pr["merged_at"].replace("Z", "+00:00"))
        
        # Calculate lead time (hours)
        lead_time = None
        if merged:
            lead_time = (merged - created).total_seconds() / 3600
        
        pr_summary = {
            "number": pr["number"],
            "title": pr["title"],
            "state": pr["state"],
            "created": pr["created_at"],
            "merged": pr.get("merged_at"),
            "lead_time_hours": lead_time,
            "labels": [l["name"] for l in pr.get("labels", [])],
            "files_changed": pr.get("changed_files", 0),
            "additions": pr.get("additions", 0),
            "deletions": pr.get("deletions", 0),
            "author": pr.get("user", {}).get("login", "unknown"),
            "url": pr.get("html_url", "")
        }
        
        summary.append(pr_summary)
    
    return summary


def get_sample_pr_data() -> List[Dict]:
    """Return sample PR data for demo purposes."""
    now = datetime.now(timezone.utc)
    return [
        {
            "number": 123,
            "title": "Fix memory leak in telemetry collector",
            "state": "merged",
            "created_at": (now - timedelta(days=5)).isoformat(),
            "merged_at": (now - timedelta(days=3)).isoformat(),
            "labels": [{"name": "bug"}, {"name": "telemetry"}],
            "changed_files": 3,
            "additions": 45,
            "deletions": 12,
            "user": {"login": "developer1"},
            "html_url": "https://github.com/example/repo/pull/123"
        },
        {
            "number": 124,
            "title": "Add caching to build system",
            "state": "open",
            "created_at": (now - timedelta(days=2)).isoformat(),
            "merged_at": None,
            "labels": [{"name": "enhancement"}, {"name": "build"}],
            "changed_files": 8,
            "additions": 120,
            "deletions": 30,
            "user": {"login": "developer2"},
            "html_url": "https://github.com/example/repo/pull/124"
        },
        {
            "number": 125,
            "title": "Update Black Duck compliance notices",
            "state": "merged",
            "created_at": (now - timedelta(days=7)).isoformat(),
            "merged_at": (now - timedelta(days=6)).isoformat(),
            "labels": [{"name": "compliance"}, {"name": "black-duck"}],
            "changed_files": 5,
            "additions": 25,
            "deletions": 5,
            "user": {"login": "developer3"},
            "html_url": "https://github.com/example/repo/pull/125"
        }
    ]


def calculate_metrics(pr_summary: List[Dict]) -> Dict:
    """Calculate basic metrics from PR data."""
    merged = [p for p in pr_summary if p["state"] == "merged"]
    open_prs = [p for p in pr_summary if p["state"] == "open"]
    
    metrics = {
        "total_prs": len(pr_summary),
        "merged_count": len(merged),
        "open_count": len(open_prs),
        "merge_rate": len(merged) / len(pr_summary) if pr_summary else 0,
        "avg_files_changed": sum(p["files_changed"] for p in pr_summary) / len(pr_summary) if pr_summary else 0,
        "avg_additions": sum(p["additions"] for p in pr_summary) / len(pr_summary) if pr_summary else 0,
        "avg_deletions": sum(p["deletions"] for p in pr_summary) / len(pr_summary) if pr_summary else 0,
    }
    
    # Calculate average lead time
    lead_times = [p["lead_time_hours"] for p in merged if p["lead_time_hours"]]
    if lead_times:
        metrics["avg_lead_time_hours"] = sum(lead_times) / len(lead_times)
        metrics["avg_lead_time_days"] = metrics["avg_lead_time_hours"] / 24
    else:
        metrics["avg_lead_time_hours"] = None
        metrics["avg_lead_time_days"] = None
    
    return metrics


def main():
    parser = argparse.ArgumentParser(description="Pull GitHub PR data")
    parser.add_argument("--repo", help="Repository (org/repo)")
    parser.add_argument("--token", help="GitHub token (or set GITHUB_TOKEN env var)")
    parser.add_argument("--output", default="github_data.json", help="Output file")
    parser.add_argument("--days", type=int, default=30, help="Days of history")
    parser.add_argument("--max-pages", type=int, default=10, help="Maximum pages to fetch (default: 10 = 1000 PRs max)")
    parser.add_argument("--filter-by", choices=["updated", "created"], default="updated", 
                       help="Filter by 'updated' (updated_at) or 'created' (created_at). Default: updated")
    parser.add_argument("--sample", action="store_true", help="Use sample data")
    
    args = parser.parse_args()
    
    if args.sample:
        print("Using sample PR data...")
        prs = get_sample_pr_data()
    elif args.repo:
        print(f"Pulling PR data from {args.repo}...")
        prs = get_pr_data(args.repo, args.token, args.days, args.max_pages, args.filter_by)
    else:
        print("Error: Either --repo or --sample required", file=sys.stderr)
        sys.exit(1)
    
    # Extract summary
    pr_summary = extract_pr_summary(prs)
    
    # Calculate metrics
    metrics = calculate_metrics(pr_summary)
    
    # Combine data
    output_data = {
        "metadata": {
            "repo": args.repo or "sample",
            "period_days": args.days,
            "generated_at": datetime.now().isoformat(),
            "total_prs": len(pr_summary)
        },
        "metrics": metrics,
        "prs": pr_summary
    }
    
    # Save to file
    with open(args.output, 'w') as f:
        json.dump(output_data, f, indent=2, default=str)
    
    print(f"\n✅ Saved {len(pr_summary)} PRs to {args.output}")
    print(f"\n📊 Metrics:")
    print(f"   Total PRs: {metrics['total_prs']}")
    print(f"   Merged: {metrics['merged_count']}")
    print(f"   Open: {metrics['open_count']}")
    print(f"   Merge rate: {metrics['merge_rate']:.1%}")
    if metrics['avg_lead_time_days']:
        print(f"   Avg lead time: {metrics['avg_lead_time_days']:.1f} days")
    print(f"   Avg files changed: {metrics['avg_files_changed']:.1f}")


if __name__ == '__main__':
    main()

