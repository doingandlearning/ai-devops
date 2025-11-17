#!/usr/bin/env python3
"""
Pull Jira Ticket Data
Example script for Part 5: Metrics & Reporting

Usage:
    python pull_jira_data.py --csv jira_export.csv --output jira_data.json
    # Or use sample data:
    python pull_jira_data.py --sample
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from typing import Dict, List

try:
    import pandas as pd
except ImportError:
    print("Error: pandas package not installed. Run: pip install pandas")
    sys.exit(1)


def read_jira_csv(csv_file: str) -> List[Dict]:
    """Read Jira export CSV file."""
    try:
        df = pd.read_csv(csv_file)
        return df.to_dict("records")
    except Exception as e:
        print(f"Error reading CSV: {e}", file=sys.stderr)
        return []


def extract_jira_summary(jira_data: List[Dict]) -> List[Dict]:
    """Extract key fields from Jira data."""
    summary = []
    
    for ticket in jira_data:
        # Handle different CSV column name variations
        key = ticket.get("Issue key") or ticket.get("Key") or ticket.get("issue_key")
        summary_text = ticket.get("Summary") or ticket.get("summary")
        status = ticket.get("Status") or ticket.get("status")
        created = ticket.get("Created") or ticket.get("created") or ticket.get("Created Date")
        resolved = ticket.get("Resolved") or ticket.get("resolved") or ticket.get("Resolved Date")
        priority = ticket.get("Priority") or ticket.get("priority")
        assignee = ticket.get("Assignee") or ticket.get("assignee")
        component = ticket.get("Component") or ticket.get("component") or ticket.get("Component/s")
        
        # Calculate resolution time if resolved
        resolution_time_days = None
        if resolved and created:
            try:
                created_dt = pd.to_datetime(created)
                resolved_dt = pd.to_datetime(resolved)
                resolution_time_days = (resolved_dt - created_dt).days
            except:
                pass
        
        ticket_summary = {
            "key": key,
            "summary": summary_text,
            "status": status,
            "created": str(created) if created else None,
            "resolved": str(resolved) if resolved else None,
            "resolution_time_days": resolution_time_days,
            "priority": priority,
            "assignee": assignee,
            "component": component
        }
        
        summary.append(ticket_summary)
    
    return summary


def get_sample_jira_data() -> List[Dict]:
    """Return sample Jira data for demo purposes."""
    return [
        {
            "Issue key": "BD-1290",
            "Summary": "Compliance Issues in rdkb/devices/test/hal",
            "Status": "Resolved",
            "Created": (datetime.now() - timedelta(days=20)).isoformat(),
            "Resolved": (datetime.now() - timedelta(days=15)).isoformat(),
            "Priority": "Major",
            "Assignee": "Sundar Subramanian",
            "Component/s": "Compliance"
        },
        {
            "Issue key": "RDK-456",
            "Summary": "Memory leak in telemetry collector",
            "Status": "In Progress",
            "Created": (datetime.now() - timedelta(days=10)).isoformat(),
            "Resolved": None,
            "Priority": "Critical",
            "Assignee": "Developer1",
            "Component/s": "Telemetry"
        },
        {
            "Issue key": "RDK-457",
            "Summary": "Build failures on main branch",
            "Status": "Open",
            "Created": (datetime.now() - timedelta(days=5)).isoformat(),
            "Resolved": None,
            "Priority": "High",
            "Assignee": "Developer2",
            "Component/s": "Build System"
        },
        {
            "Issue key": "RDK-458",
            "Summary": "Add caching to build system",
            "Status": "Resolved",
            "Created": (datetime.now() - timedelta(days=8)).isoformat(),
            "Resolved": (datetime.now() - timedelta(days=6)).isoformat(),
            "Priority": "Medium",
            "Assignee": "Developer2",
            "Component/s": "Build System"
        }
    ]


def calculate_metrics(jira_summary: List[Dict]) -> Dict:
    """Calculate basic metrics from Jira data."""
    resolved = [t for t in jira_summary if t["status"] == "Resolved"]
    open_tickets = [t for t in jira_summary if t["status"] in ["Open", "In Progress"]]
    
    # Group by priority
    by_priority = {}
    for ticket in jira_summary:
        priority = ticket.get("priority") or "Unassigned"
        by_priority[priority] = by_priority.get(priority, 0) + 1
    
    # Group by component
    by_component = {}
    for ticket in jira_summary:
        component = ticket.get("component") or "Unassigned"
        by_component[component] = by_component.get(component, 0) + 1
    
    # Calculate average resolution time
    resolution_times = [t["resolution_time_days"] for t in resolved if t["resolution_time_days"]]
    avg_resolution_time = sum(resolution_times) / len(resolution_times) if resolution_times else None
    
    metrics = {
        "total_tickets": len(jira_summary),
        "resolved_count": len(resolved),
        "open_count": len(open_tickets),
        "resolution_rate": len(resolved) / len(jira_summary) if jira_summary else 0,
        "avg_resolution_time_days": avg_resolution_time,
        "by_priority": by_priority,
        "by_component": by_component
    }
    
    return metrics


def main():
    parser = argparse.ArgumentParser(description="Pull Jira ticket data")
    parser.add_argument("--csv", help="Jira export CSV file")
    parser.add_argument("--output", default="jira_data.json", help="Output file")
    parser.add_argument("--sample", action="store_true", help="Use sample data")
    
    args = parser.parse_args()
    
    if args.sample:
        print("Using sample Jira data...")
        jira_data = get_sample_jira_data()
    elif args.csv:
        print(f"Reading Jira data from {args.csv}...")
        jira_data = read_jira_csv(args.csv)
        if not jira_data:
            print("Error: No data found in CSV", file=sys.stderr)
            sys.exit(1)
    else:
        print("Error: Either --csv or --sample required", file=sys.stderr)
        sys.exit(1)
    
    # Extract summary
    jira_summary = extract_jira_summary(jira_data)
    
    # Calculate metrics
    metrics = calculate_metrics(jira_summary)
    
    # Combine data
    output_data = {
        "metadata": {
            "source": args.csv or "sample",
            "generated_at": datetime.now().isoformat(),
            "total_tickets": len(jira_summary)
        },
        "metrics": metrics,
        "tickets": jira_summary
    }
    
    # Save to file
    with open(args.output, 'w') as f:
        json.dump(output_data, f, indent=2, default=str)
    
    print(f"\n✅ Saved {len(jira_summary)} tickets to {args.output}")
    print(f"\n📊 Metrics:")
    print(f"   Total tickets: {metrics['total_tickets']}")
    print(f"   Resolved: {metrics['resolved_count']}")
    print(f"   Open: {metrics['open_count']}")
    print(f"   Resolution rate: {metrics['resolution_rate']:.1%}")
    if metrics['avg_resolution_time_days']:
        print(f"   Avg resolution time: {metrics['avg_resolution_time_days']:.1f} days")
    print(f"\n   By Priority:")
    for priority, count in metrics['by_priority'].items():
        print(f"     {priority}: {count}")
    print(f"\n   By Component:")
    for component, count in metrics['by_component'].items():
        print(f"     {component}: {count}")


if __name__ == '__main__':
    main()

