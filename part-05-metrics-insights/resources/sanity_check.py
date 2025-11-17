#!/usr/bin/env python3
"""
Sanity Check for AI-Generated Summary
Example script for Part 5: Metrics & Reporting

Usage:
    python sanity_check.py weekly_summary.txt github_data.json jira_data.json
"""

import argparse
import json
import re
import sys
from typing import Dict, List, Tuple


def extract_numbers(text: str) -> List[int]:
    """Extract numbers from text."""
    return [int(m) for m in re.findall(r'\d+', text)]


def verify_pr_counts(summary: str, github_data: Dict) -> Tuple[bool, List[str]]:
    """Verify PR counts mentioned in summary match actual data."""
    issues = []
    
    github_metrics = github_data.get("metrics", {})
    actual_total = github_metrics.get("total_prs", 0)
    actual_merged = github_metrics.get("merged_count", 0)
    actual_open = github_metrics.get("open_count", 0)
    
    # Extract numbers from summary
    numbers = extract_numbers(summary)
    
    # Check if summary mentions PR counts
    if "PR" in summary.upper() or "pull request" in summary.lower():
        # Look for patterns like "X PRs", "X pull requests"
        pr_patterns = [
            r'(\d+)\s+PRs?',
            r'(\d+)\s+pull\s+requests?',
            r'PRs?:\s*(\d+)',
        ]
        
        found_counts = []
        for pattern in pr_patterns:
            matches = re.findall(pattern, summary, re.IGNORECASE)
            found_counts.extend([int(m) for m in matches])
        
        if found_counts:
            # Check if any match actual counts (within reasonable range)
            close_match = False
            for count in found_counts:
                if abs(count - actual_total) <= 2:  # Allow small variance
                    close_match = True
                    break
            
            if not close_match and found_counts:
                issues.append(f"PR count mismatch: Summary mentions {found_counts}, actual is {actual_total}")
    
    return len(issues) == 0, issues


def verify_ticket_counts(summary: str, jira_data: Dict) -> Tuple[bool, List[str]]:
    """Verify ticket counts mentioned in summary match actual data."""
    issues = []
    
    jira_metrics = jira_data.get("metrics", {})
    actual_total = jira_metrics.get("total_tickets", 0)
    actual_resolved = jira_metrics.get("resolved_count", 0)
    actual_open = jira_metrics.get("open_count", 0)
    
    # Check if summary mentions ticket counts
    if "ticket" in summary.lower() or "issue" in summary.lower():
        ticket_patterns = [
            r'(\d+)\s+tickets?',
            r'(\d+)\s+issues?',
            r'tickets?:\s*(\d+)',
        ]
        
        found_counts = []
        for pattern in ticket_patterns:
            matches = re.findall(pattern, summary, re.IGNORECASE)
            found_counts.extend([int(m) for m in matches])
        
        if found_counts:
            close_match = False
            for count in found_counts:
                if abs(count - actual_total) <= 2:
                    close_match = True
                    break
            
            if not close_match and found_counts:
                issues.append(f"Ticket count mismatch: Summary mentions {found_counts}, actual is {actual_total}")
    
    return len(issues) == 0, issues


def check_mentioned_risks(summary: str, github_data: Dict, jira_data: Dict) -> Tuple[bool, List[str]]:
    """Check if risks mentioned in summary actually exist in data."""
    issues = []
    
    # Risk keywords
    risk_keywords = ["security", "blocker", "urgent", "critical", "failure", "error"]
    
    mentioned_risks = []
    for keyword in risk_keywords:
        if keyword.lower() in summary.lower():
            mentioned_risks.append(keyword)
    
    # Check if risks exist in data
    found_risks = []
    
    # Check GitHub PRs
    for pr in github_data.get("prs", []):
        title_lower = pr.get("title", "").lower()
        labels_lower = [l.lower() for l in pr.get("labels", [])]
        
        for risk in mentioned_risks:
            if risk in title_lower or risk in " ".join(labels_lower):
                found_risks.append(f"PR #{pr['number']}: {risk}")
    
    # Check Jira tickets
    for ticket in jira_data.get("tickets", []):
        summary_lower = ticket.get("summary", "").lower()
        priority_lower = (ticket.get("priority") or "").lower()
        
        for risk in mentioned_risks:
            if risk in summary_lower or risk in priority_lower:
                found_risks.append(f"{ticket['key']}: {risk}")
    
    # If risks mentioned but not found, flag it
    if mentioned_risks and not found_risks:
        issues.append(f"Summary mentions risks ({', '.join(mentioned_risks)}) but none found in data")
    elif found_risks:
        print(f"   ✅ Found risks in data: {len(found_risks)}")
        for risk in found_risks[:3]:  # Show first 3
            print(f"      - {risk}")
    
    return len(issues) == 0, issues


def check_completeness(summary: str, github_data: Dict, jira_data: Dict) -> Tuple[bool, List[str]]:
    """Check if summary covers important items."""
    issues = []
    
    # Required sections
    required_sections = ["summary", "metrics", "risks", "actions"]
    
    missing_sections = []
    summary_lower = summary.lower()
    
    for section in required_sections:
        if section not in summary_lower:
            missing_sections.append(section)
    
    if missing_sections:
        issues.append(f"Missing sections: {', '.join(missing_sections)}")
    
    # Check if high-priority items are mentioned
    high_priority_tickets = [
        t for t in jira_data.get("tickets", [])
        if t.get("priority", "").lower() in ["critical", "high"]
    ]
    
    if high_priority_tickets and "high" not in summary_lower() and "critical" not in summary_lower():
        issues.append(f"High-priority tickets exist ({len(high_priority_tickets)}) but not mentioned")
    
    return len(issues) == 0, issues


def main():
    parser = argparse.ArgumentParser(description="Sanity check AI-generated summary")
    parser.add_argument("summary_file", help="Summary text file")
    parser.add_argument("github_data", help="GitHub data JSON file")
    parser.add_argument("jira_data", help="Jira data JSON file")
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("Sanity Check: AI-Generated Summary")
    print("=" * 70)
    
    # Load files
    with open(args.summary_file, 'r') as f:
        summary = f.read()
    
    with open(args.github_data, 'r') as f:
        github_data = json.load(f)
    
    with open(args.jira_data, 'r') as f:
        jira_data = json.load(f)
    
    print(f"\n📋 Summary length: {len(summary)} characters")
    print(f"📊 GitHub data: {len(github_data.get('prs', []))} PRs")
    print(f"📋 Jira data: {len(jira_data.get('tickets', []))} tickets")
    
    # Run checks
    print(f"\n🔍 Running sanity checks...")
    
    all_issues = []
    
    # Check 1: PR counts
    print(f"\n1. Verifying PR counts...")
    pr_ok, pr_issues = verify_pr_counts(summary, github_data)
    if pr_ok:
        print(f"   ✅ PR counts verified")
    else:
        print(f"   ⚠️  Issues found:")
        for issue in pr_issues:
            print(f"      - {issue}")
        all_issues.extend(pr_issues)
    
    # Check 2: Ticket counts
    print(f"\n2. Verifying ticket counts...")
    ticket_ok, ticket_issues = verify_ticket_counts(summary, jira_data)
    if ticket_ok:
        print(f"   ✅ Ticket counts verified")
    else:
        print(f"   ⚠️  Issues found:")
        for issue in ticket_issues:
            print(f"      - {issue}")
        all_issues.extend(ticket_issues)
    
    # Check 3: Mentioned risks
    print(f"\n3. Checking mentioned risks...")
    risk_ok, risk_issues = check_mentioned_risks(summary, github_data, jira_data)
    if risk_ok:
        print(f"   ✅ Risks verified")
    else:
        print(f"   ⚠️  Issues found:")
        for issue in risk_issues:
            print(f"      - {issue}")
        all_issues.extend(risk_issues)
    
    # Check 4: Completeness
    print(f"\n4. Checking completeness...")
    complete_ok, complete_issues = check_completeness(summary, github_data, jira_data)
    if complete_ok:
        print(f"   ✅ Summary is complete")
    else:
        print(f"   ⚠️  Issues found:")
        for issue in complete_issues:
            print(f"      - {issue}")
        all_issues.extend(complete_issues)
    
    # Summary
    print(f"\n" + "=" * 70)
    if all_issues:
        print(f"⚠️  Sanity Check: {len(all_issues)} issue(s) found")
        print(f"\nRecommendations:")
        print(f"  1. Verify numbers against raw data")
        print(f"  2. Check if risks mentioned actually exist")
        print(f"  3. Ensure all required sections are present")
        print(f"  4. Refine prompt to request citations")
        sys.exit(1)
    else:
        print(f"✅ Sanity Check: All checks passed")
        print(f"\nSummary appears accurate. Ready for use.")
        sys.exit(0)


if __name__ == '__main__':
    main()

