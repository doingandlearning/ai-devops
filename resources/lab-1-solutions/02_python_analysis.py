#!/usr/bin/env python3
"""
Extract top error patterns from build log with line numbers.
Python version - more structured than grep/awk approach.
"""

import re
from collections import Counter

def analyze_build_log(log_file='build.log'):
    """Analyze build log and extract error patterns."""
    
    errors = []
    error_types = Counter()
    
    # Error patterns to match
    error_patterns = [
        (r'error:\s*(.+)', 'Compilation error'),
        (r'fatal:\s*(.+)', 'Fatal error'),
        (r'cannot find\s+(.+)', 'Linker error - missing library'),
        (r'undefined reference to\s+(.+)', 'Linker error - undefined reference'),
    ]
    
    try:
        with open(log_file, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                
                # Skip non-error lines
                if 'ERROR:' in line or 'make[' in line:
                    continue
                
                # Check for error patterns
                for pattern, error_type in error_patterns:
                    match = re.search(pattern, line, re.IGNORECASE)
                    if match:
                        error_msg = match.group(1).strip()
                        errors.append({
                            'line': line_num,
                            'type': error_type,
                            'message': error_msg,
                            'full_line': line
                        })
                        error_types[error_type] += 1
                        break
    
    except FileNotFoundError:
        print(f"Error: {log_file} not found")
        return
    
    # Print error lines with line numbers
    print("=== Error Lines with Line Numbers ===")
    print()
    
    for error in errors[:10]:  # Show first 10
        print(f"Line {error['line']}: {error['full_line']}")
    
    print()
    print("=== Error Count Summary ===")
    print()
    
    # Print error type counts
    for error_type, count in error_types.most_common():
        print(f"{error_type}: {count}")
    
    print()
    print(f"Total error lines: {len(errors)}")
    
    # Show top 3 error patterns (by message content)
    if errors:
        print()
        print("=== Top 3 Error Patterns (by message) ===")
        print()
        
        # Extract first word/phrase from error messages
        message_patterns = Counter()
        for error in errors:
            # Extract first meaningful word from error message
            msg = error['message']
            # Get first word or first few words
            first_part = msg.split()[0] if msg.split() else msg[:30]
            message_patterns[first_part] += 1
        
        for pattern, count in message_patterns.most_common(3):
            print(f"{count}x: {pattern}")

if __name__ == '__main__':
    analyze_build_log()

