#!/usr/bin/env python3
"""
AI Usage Cost Tracking
Example script for Part 5: Metrics & Reporting

Usage:
    python cost_tracking.py --log ai_usage_log.json --period weekly
    python cost_tracking.py --log ai_usage_log.json --period monthly
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List


def load_usage_log(log_file: str) -> List[Dict]:
    """Load AI usage log."""
    if not os.path.exists(log_file):
        return []
    
    with open(log_file, 'r') as f:
        return json.load(f)


def filter_by_period(log: List[Dict], period: str) -> List[Dict]:
    """Filter log entries by time period."""
    now = datetime.now()
    
    if period == "daily":
        cutoff = now - timedelta(days=1)
    elif period == "weekly":
        cutoff = now - timedelta(days=7)
    elif period == "monthly":
        cutoff = now - timedelta(days=30)
    else:
        return log
    
    filtered = []
    for entry in log:
        entry_time = datetime.fromisoformat(entry["timestamp"])
        if entry_time >= cutoff:
            filtered.append(entry)
    
    return filtered


def calculate_costs(log: List[Dict]) -> Dict:
    """Calculate cost breakdown."""
    total_cost = sum(entry["cost"] for entry in log)
    total_tokens = sum(entry["tokens"] for entry in log)
    
    # By operation
    by_operation = {}
    for entry in log:
        op = entry["operation"]
        if op not in by_operation:
            by_operation[op] = {"count": 0, "cost": 0, "tokens": 0}
        by_operation[op]["count"] += 1
        by_operation[op]["cost"] += entry["cost"]
        by_operation[op]["tokens"] += entry["tokens"]
    
    # By model
    by_model = {}
    for entry in log:
        model = entry["model"]
        if model not in by_model:
            by_model[model] = {"count": 0, "cost": 0, "tokens": 0}
        by_model[model]["count"] += 1
        by_model[model]["cost"] += entry["cost"]
        by_model[model]["tokens"] += entry["tokens"]
    
    return {
        "total_cost": total_cost,
        "total_tokens": total_tokens,
        "total_operations": len(log),
        "avg_cost_per_operation": total_cost / len(log) if log else 0,
        "by_operation": by_operation,
        "by_model": by_model
    }


def generate_cost_report(costs: Dict, period: str) -> str:
    """Generate human-readable cost report."""
    report = []
    report.append("=" * 70)
    report.append(f"AI Usage Cost Report ({period.capitalize()})")
    report.append("=" * 70)
    report.append("")
    
    report.append(f"📊 Summary:")
    report.append(f"   Total operations: {costs['total_operations']}")
    report.append(f"   Total tokens: {costs['total_tokens']:,}")
    report.append(f"   Total cost: ${costs['total_cost']:.4f}")
    report.append(f"   Avg cost per operation: ${costs['avg_cost_per_operation']:.4f}")
    report.append("")
    
    report.append(f"💰 Cost by Operation:")
    for op, stats in sorted(costs['by_operation'].items(), key=lambda x: x[1]['cost'], reverse=True):
        pct = (stats['cost'] / costs['total_cost'] * 100) if costs['total_cost'] > 0 else 0
        report.append(f"   {op}:")
        report.append(f"     Operations: {stats['count']}")
        report.append(f"     Tokens: {stats['tokens']:,}")
        report.append(f"     Cost: ${stats['cost']:.4f} ({pct:.1f}%)")
    report.append("")
    
    report.append(f"🤖 Cost by Model:")
    for model, stats in sorted(costs['by_model'].items(), key=lambda x: x[1]['cost'], reverse=True):
        pct = (stats['cost'] / costs['total_cost'] * 100) if costs['total_cost'] > 0 else 0
        report.append(f"   {model}:")
        report.append(f"     Operations: {stats['count']}")
        report.append(f"     Tokens: {stats['tokens']:,}")
        report.append(f"     Cost: ${stats['cost']:.4f} ({pct:.1f}%)")
    report.append("")
    
    # ROI estimate
    report.append(f"💡 ROI Estimate:")
    report.append(f"   Assuming each operation saves 30 minutes:")
    report.append(f"   Time saved: {costs['total_operations'] * 0.5} hours")
    report.append(f"   Engineer cost/hour: $100 (example)")
    report.append(f"   Time value: ${costs['total_operations'] * 0.5 * 100:.2f}")
    report.append(f"   AI cost: ${costs['total_cost']:.2f}")
    report.append(f"   Net savings: ${costs['total_operations'] * 0.5 * 100 - costs['total_cost']:.2f}")
    report.append("")
    
    return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(description="Track AI usage costs")
    parser.add_argument("--log", default="ai_usage_log.json", help="Usage log file")
    parser.add_argument("--period", choices=["daily", "weekly", "monthly", "all"], 
                       default="weekly", help="Time period")
    parser.add_argument("--output", help="Output file (default: stdout)")
    
    args = parser.parse_args()
    
    # Load log
    log = load_usage_log(args.log)
    
    if not log:
        print(f"No usage log found at {args.log}")
        print("Run generate_weekly_summary.py with --track-usage to create log")
        sys.exit(1)
    
    # Filter by period
    if args.period != "all":
        log = filter_by_period(log, args.period)
    
    if not log:
        print(f"No entries found for {args.period} period")
        sys.exit(0)
    
    # Calculate costs
    costs = calculate_costs(log)
    
    # Generate report
    report = generate_cost_report(costs, args.period)
    
    # Output
    if args.output:
        with open(args.output, 'w') as f:
            f.write(report)
        print(f"✅ Cost report saved to {args.output}")
    else:
        print(report)


if __name__ == '__main__':
    main()

