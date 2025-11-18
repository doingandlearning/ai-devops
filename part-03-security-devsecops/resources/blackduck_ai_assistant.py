#!/usr/bin/env python3
"""
Black Duck AI Assistant - Copyright Challenge Demo

This script demonstrates:
1. Extracting code to reduce token usage (hybrid approach)
2. Using BD report to decrease hallucinations (structured input)
3. Using LLM to enhance but get structured responses

Usage:
    python blackduck_ai_assistant.py --bd-report bd-report.txt --source wifi_hal.c --outdir compliance
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional

try:
    from openai import OpenAI
except ImportError:
    print("Error: openai package not installed. Run: pip install openai")
    sys.exit(1)


class BlackDuckAIAssistant:
    """Assists with Black Duck compliance by extracting code and generating structured responses."""
    
    def __init__(self, source_file: str, bd_report: str, outdir: str = "compliance"):
        self.source_file = Path(source_file)
        self.bd_report = Path(bd_report)
        self.outdir = Path(outdir)
        self.outdir.mkdir(exist_ok=True)
        
        # Load files
        self.source_lines = self._load_source_file()
        self.bd_content = self._load_bd_report()
        
        # Extract references
        self.code_sections = []
        self.references = self._parse_bd_references()
    
    def _load_source_file(self) -> List[str]:
        """Load source file lines."""
        if not self.source_file.exists():
            raise FileNotFoundError(f"Source file not found: {self.source_file}")
        
        with open(self.source_file, 'r', encoding='utf-8') as f:
            return f.readlines()
    
    def _load_bd_report(self) -> str:
        """Load Black Duck report."""
        if not self.bd_report.exists():
            raise FileNotFoundError(f"BD report not found: {self.bd_report}")
        
        with open(self.bd_report, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _parse_bd_references(self) -> List[Dict]:
        """Parse BD report to extract file:line references."""
        references = []
        
        # Extract file references: wifi_hal.c:72 (more flexible pattern)
        # Pattern matches: filename.ext:number or filename:number
        for match in re.finditer(r'([\w\-_]+\.\w+):(\d+)', self.bd_content):
            filename = match.group(1)
            line_num = int(match.group(2))
            # Only process if it matches our source file
            if filename == self.source_file.name or filename in self.source_file.name:
                references.append({
                    'file': self.source_file.name,
                    'line': line_num,
                    'type': 'exact',
                    'context': self._get_context(line_num)
                })
        
        # Also try simpler pattern: any text ending with :number
        for match in re.finditer(r'(\w+\.c):(\d+)', self.bd_content):
            filename = match.group(1)
            line_num = int(match.group(2))
            if filename == self.source_file.name or self.source_file.name.endswith(filename):
                references.append({
                    'file': self.source_file.name,
                    'line': line_num,
                    'type': 'exact',
                    'context': self._get_context(line_num)
                })
        
        # Extract "before line" references: before 18773
        for match in re.finditer(r'before\s+(\d+)', self.bd_content, re.IGNORECASE):
            line_num = int(match.group(1))
            # Only process if line number is valid
            if 0 < line_num <= len(self.source_lines):
                references.append({
                    'file': self.source_file.name,
                    'line': line_num,
                    'type': 'before',
                    'context': self._get_context(line_num, context_lines=10, before_lines=5)
                })
        
        # Extract function/code references mentioned in BD report
        function_refs = [
            'rxStatsInfo_callback',
            'callback_dump',
            'ieee80211',
        ]
        
        for func_name in function_refs:
            if func_name.lower() in self.bd_content.lower():
                line_num = self._find_function_line(func_name)
                if line_num:
                    references.append({
                        'file': self.source_file.name,
                        'line': line_num,
                        'type': 'function',
                        'function': func_name,
                        'context': self._get_context(line_num, context_lines=20, before_lines=5)
                    })
        
        # Extract copyright notice sections (lines 30-36 based on BD report)
        # Look for copyright-related comments in the source
        copyright_patterns = [
            r'Copyright.*?ISC',
            r'Copyright.*?BSD',
            r'Copyright.*?Apache',
        ]
        
        for i, line in enumerate(self.source_lines, 1):
            for pattern in copyright_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    # Check if this is already referenced
                    if not any(ref['line'] == i for ref in references):
                        references.append({
                            'file': self.source_file.name,
                            'line': i,
                            'type': 'copyright',
                            'context': self._get_context(i, context_lines=10, before_lines=5)
                        })
                    break
        
        # Remove duplicates (same line number)
        seen_lines = set()
        unique_refs = []
        for ref in references:
            if ref['line'] not in seen_lines:
                seen_lines.add(ref['line'])
                unique_refs.append(ref)
        
        return unique_refs
    
    def _find_function_line(self, func_name: str) -> Optional[int]:
        """Find line number of function definition."""
        for i, line in enumerate(self.source_lines, 1):
            if re.search(rf'\b{re.escape(func_name)}\s*\(', line):
                return i
        return None
    
    def _get_context(self, line_num: int, context_lines: int = 10, before_lines: int = 5) -> str:
        """Extract code context around a line number."""
        start = max(0, line_num - before_lines - 1)
        end = min(len(self.source_lines), line_num + context_lines)
        
        context = []
        for i in range(start, end):
            prefix = ">>> " if i == line_num - 1 else "    "
            context.append(f"{prefix}{i+1:5d}: {self.source_lines[i]}")
        
        return "".join(context)
    
    def extract_code_sections(self) -> Dict:
        """Extract referenced code sections and save as artifact."""
        artifact = {
            'source_file': str(self.source_file),
            'bd_report': str(self.bd_report),
            'sections': []
        }
        
        for ref in self.references:
            line_num = ref['line']
            start = max(0, line_num - 10)
            end = min(len(self.source_lines), line_num + 20)
            
            section = {
                'reference': ref,
                'start_line': start + 1,
                'end_line': end,
                'code': ''.join(self.source_lines[start:end]),
                'context': ref.get('context', '')
            }
            
            artifact['sections'].append(section)
            self.code_sections.append(section)
        
        # Save artifact (like a git diff would show)
        artifact_file = self.outdir / 'extracted_code.json'
        with open(artifact_file, 'w', encoding='utf-8') as f:
            json.dump(artifact, f, indent=2)
        
        print(f"✅ Extracted {len(self.code_sections)} code sections")
        print(f"📁 Saved artifact: {artifact_file}")
        
        return artifact
    
    def create_prompt(self) -> str:
        """Create structured prompt for LLM."""
        # Combine extracted code sections
        code_snippets = []
        for section in self.code_sections:
            code_snippets.append(f"=== {section['reference']['file']}:{section['start_line']}-{section['end_line']} ===\n{section['code']}")
        
        code_block = "\n\n".join(code_snippets)
        
        # Extract relevant BD notes (first 2000 chars to avoid token bloat)
        bd_summary = self.bd_content[:2000] + "..." if len(self.bd_content) > 2000 else self.bd_content
        
        prompt = f"""Role: RDKM compliance assistant.
Task: Draft NOTICE and LICENSE addenda for the snippet below.

Return JSON:
{{
  "notice_additions": ["..."],
  "license_additions": ["..."],
  "evidence": [{{"file":"{{ PATH }}","lines":[START,END],"why":"..."}}],
  "confidence":"high|medium|low",
  "review_required": true
}}

Rules:
- Only cite text present in the snippet or in the BD notes below.
- If source isn't provable from provided text, set confidence=low and review_required=true.
- Use RDK standard phrasing ("The component is licensed to you under the Apache License, Version 2.0...").
- Don't invent years/names; use placeholders if uncertain: {{ YEAR }}, {{ COPYRIGHT HOLDER }}.

<code_block>
{code_block}
</code_block>

<black_duck_summary>
{bd_summary}
</black_duck_summary>
"""
        return prompt
    
    def call_llm(self, api_key: Optional[str] = None, model: str = "gpt-4o") -> Dict:
        """Call LLM with structured prompt."""
        if not api_key:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable not set")
        
        client = OpenAI(api_key=api_key)
        
        prompt = self.create_prompt()
        
        # Calculate token savings
        full_file_size = len(''.join(self.source_lines))
        extracted_size = sum(len(s['code']) for s in self.code_sections)
        savings_pct = ((full_file_size - extracted_size) / full_file_size * 100) if full_file_size > 0 else 0
        
        print(f"\n📊 Token Usage Analysis:")
        print(f"   Full file: {full_file_size:,} characters")
        print(f"   Extracted: {extracted_size:,} characters")
        print(f"   Savings: {savings_pct:.1f}%")
        print(f"\n🤖 Calling LLM ({model})...")
        
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a compliance assistant. Always return valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3  # Lower temperature for more deterministic output
            )
            
            result_text = response.choices[0].message.content
            
            # Parse JSON response
            try:
                result = json.loads(result_text)
            except json.JSONDecodeError:
                # Try to extract JSON from markdown code blocks
                json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', result_text, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group(1))
                else:
                    raise ValueError("Could not parse JSON from LLM response")
            
            return result
            
        except Exception as e:
            print(f"❌ Error calling LLM: {e}")
            raise
    
    def save_results(self, llm_result: Dict):
        """Save LLM results as structured JSON."""
        output_file = self.outdir / 'ai_notice.json'
        
        # Add metadata
        result_with_meta = {
            'metadata': {
                'source_file': str(self.source_file),
                'bd_report': str(self.bd_report),
                'extracted_sections': len(self.code_sections),
                'confidence': llm_result.get('confidence', 'unknown'),
                'review_required': llm_result.get('review_required', True)
            },
            'notice_additions': llm_result.get('notice_additions', []),
            'license_additions': llm_result.get('license_additions', []),
            'evidence': llm_result.get('evidence', []),
            'confidence': llm_result.get('confidence', 'low'),
            'review_required': llm_result.get('review_required', True)
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result_with_meta, f, indent=2)
        
        print(f"\n✅ Saved results: {output_file}")
        print(f"\n📋 Summary:")
        print(f"   Confidence: {result_with_meta['confidence']}")
        print(f"   Review required: {result_with_meta['review_required']}")
        print(f"   Notice additions: {len(result_with_meta['notice_additions'])}")
        print(f"   License additions: {len(result_with_meta['license_additions'])}")
        print(f"   Evidence items: {len(result_with_meta['evidence'])}")
        
        return output_file


def main():
    parser = argparse.ArgumentParser(
        description="Black Duck AI Assistant - Extract code and generate compliance notices"
    )
    parser.add_argument(
        '--bd-report',
        required=True,
        help='Path to Black Duck report (e.g., bd-report.txt)'
    )
    parser.add_argument(
        '--source',
        required=True,
        help='Path to source file (e.g., wifi_hal.c)'
    )
    parser.add_argument(
        '--outdir',
        default='compliance',
        help='Output directory for artifacts (default: compliance)'
    )
    parser.add_argument(
        '--api-key',
        help='OpenAI API key (or set OPENAI_API_KEY env var)'
    )
    parser.add_argument(
        '--model',
        default='gpt-4o',
        help='LLM model to use (default: gpt-4o)'
    )
    parser.add_argument(
        '--extract-only',
        action='store_true',
        help='Only extract code sections, do not call LLM'
    )
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("Black Duck AI Assistant - Copyright Challenge Demo")
    print("=" * 70)
    print(f"\n📄 Source file: {args.source}")
    print(f"📋 BD report: {args.bd_report}")
    print(f"📁 Output dir: {args.outdir}")
    
    try:
        # Initialize assistant
        assistant = BlackDuckAIAssistant(
            source_file=args.source,
            bd_report=args.bd_report,
            outdir=args.outdir
        )
        
        # Step 1: Extract code sections (reduces token usage)
        print("\n" + "=" * 70)
        print("Step 1: Extracting referenced code sections")
        print("=" * 70)
        artifact = assistant.extract_code_sections()
        
        if args.extract_only:
            print("\n✅ Extraction complete. Use --extract-only=false to call LLM.")
            return
        
        # Step 2: Call LLM with structured prompt
        print("\n" + "=" * 70)
        print("Step 2: Calling LLM with structured prompt")
        print("=" * 70)
        llm_result = assistant.call_llm(api_key=args.api_key, model=args.model)
        
        # Step 3: Save structured results
        print("\n" + "=" * 70)
        print("Step 3: Saving structured results")
        print("=" * 70)
        output_file = assistant.save_results(llm_result)
        
        print("\n" + "=" * 70)
        print("✅ Demo Complete!")
        print("=" * 70)
        print(f"\n📁 Artifacts saved in: {args.outdir}/")
        print(f"   - extracted_code.json (code sections)")
        print(f"   - ai_notice.json (LLM results)")
        print(f"\n💡 Key Takeaways:")
        print(f"   1. Extracted code reduces token usage by ~{((len(''.join(assistant.source_lines)) - sum(len(s['code']) for s in assistant.code_sections)) / len(''.join(assistant.source_lines)) * 100):.1f}%")
        print(f"   2. BD report provides structured context to reduce hallucinations")
        print(f"   3. Structured JSON output ensures consistent, reviewable results")
        
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

