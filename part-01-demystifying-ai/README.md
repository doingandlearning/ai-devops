# Part 1: Demystifying AI for DevOps Professionals

**Duration:** 30 minutes (09:30-10:00)  
**Format:** Discussion + Demo (Small Group - 7 participants)

## Learning Objectives

By the end of this section, participants will:
- Understand what AI (specifically LLMs) is and isn't in a DevOps context
- Distinguish LLMs from traditional automation
- Identify realistic value areas vs. hype
- Recognize AI's relevance for managing RDK code hosting facility (CMF team context)
- Map their specific pain points to AI solutions

## Your Context: RDK Management (RDKM)

**You're the CMF Team** - managing the RDK code hosting facility for RDKM (Comcast, Charter, LGI) and the Community.

**Your responsibilities:**
- Managing RDK Software Stack codebase (github.com/rdkcentral)
- Code hosting and community management
- Compliance and licensing (Apache, NOTICE files)
- Security scanning (CodeQL, Coverity, Black Duck)
- Build failures, log analysis, copyright scanning

**Today's question:** "Can we use AI to help make the job?" Let's find out.

## Key Topics

- What AI is (and what it is not) in the context of DevOps
- How LLMs differ from traditional automation
- Realistic areas of value in software delivery vs. hype
- Relevance for C/C++ code hosting and CI/CD

## Exercise 1.0: Map Your Pain Points (10 minutes)
**Full Group Discussion** (Small group - everyone participates)

**Context:** You've identified three main pain points:
1. **Log file analysis** - Understanding build failures, CI errors
2. **Running AI as automated task with Jenkins** - Integrating AI into CI/CD
3. **Copyright scanning** - Black Duck attribution, identifying original sources

**Task:** As a group, discuss:
- Which of these takes most of your time?
- What's the biggest bottleneck in each?
- What would "good" look like for each?

**We'll address each of these today:**
- ✅ **Log file analysis** → Lab 1 (Part 2) - Build/Log Failure Triage
- ✅ **Jenkins automation** → New lab (Part 2) - AI Automation with Jenkins
- ✅ **Copyright scanning** → Part 3 - Black Duck Source Identification

**Takeaway:** AI isn't magic - it's a tool that can help with YOUR specific pain points.

---

## Demo: "Same Task, Three Ways"

**Objective:** Show when traditional automation wins, when LLMs win, and when to combine them.

### Scenario
Extract error patterns from a CI build log to identify the top 3 root causes.

**Real context:** This addresses your pain point #1 - log file analysis. Let's see three approaches.

### Approach 1: Traditional Automation (regex/jq)
```bash
# Show grep/awk/jq pipeline
grep -i "error\|fatal\|failed" build.log | \
  awk '{print $1, $2}' | \
  sort | uniq -c | sort -rn | head -3
```
**When this wins:** Deterministic patterns, fast execution, no external dependencies, auditability.

### Approach 2: Small Python Script
```python
# Structured parsing with error categorization
import re
errors = {}
for line in log:
    if match := re.search(r'(error|fatal):\s*(\w+)', line):
        errors[match.group(2)] = errors.get(match.group(2), 0) + 1
```
**When this wins:** Complex parsing needs, maintainable logic, can handle edge cases.

### Approach 3: LLM Prompt
```
Analyze this build log and identify the top 3 root causes of failures.
For each, provide:
1. The root cause
2. Confidence level (high/medium/low)
3. Suggested fix

Log:
[build log content]
```
**When this wins:** Unstructured logs, need for context understanding, explaining failures to humans, generating actionable summaries.

### Discussion Points (Full Group)
- What are the trade-offs in execution time?
- Which approach is most auditable?
- When would you need human-in-the-loop regardless?
- **For your RDK context:** Which approach would you use for github.com/rdkcentral build logs?

---

## Alan's Sceptic Corner (10 minutes)
**Dedicated time to address concerns directly**

**Alan, you're managing software for Comcast and you're sceptical about AI-generated code. Let's address your concerns directly:**

### 1. Failure Modes & Hallucinations
**Your concern:** "What happens when AI gets it wrong?"

**Discussion:**
- When have you seen automation fail? How does LLM failure differ?
- What happens when an LLM confidently states wrong information?
- How do you verify LLM output without trusting it blindly?

**For RDK context:**
- AI might suggest wrong license attribution → human review required
- AI might miss security issues → always use CodeQL/Coverity
- AI might suggest unsafe C/C++ code → always compile with `-Werror`, run sanitizers

### 2. Cost Concerns
**Your concern:** "At the edge of AI becoming more expensive"

**Discussion:**
- Traditional automation: predictable CPU/memory costs
- LLMs: per-token pricing, API rate limits
- How would you budget for AI in CI/CD? What happens when usage scales?
- **For RDK context:** Managing codebase for Comcast/Sky with community users - how do costs scale?

**We'll address this in Part 6:** Cost at scale - concrete numbers for your use cases.

### 3. Vendor Lock-in
**Your concern:** "What if we become dependent on a vendor?"

**Discussion:**
- Regex/jq: universal, portable
- Python scripts: portable with dependencies
- LLM APIs: vendor-specific, changing models, pricing uncertainty
- How do you build resilience against vendor changes?

**For RDK context:**
- Start with local models (Ollama) for sensitive data
- Use hosted APIs for non-sensitive tasks
- Keep prompts portable (not vendor-specific)

### 4. Code Being Generated by AI
**Your concern:** "Code being generated by AI - is it safe?"

**Discussion:**
- C/C++ build failures often have deterministic patterns (compiler errors, linter issues)
- When would an LLM add value vs. a simple parser?
- **For RDK context:** Think about build configuration errors, dependency conflicts, test failure analysis

**We'll address this in Lab 2:** C/C++ Unit Test Generation - safe patterns, acceptance checklist.

**Key point:** AI generates suggestions, humans review and decide. Always.

---

## Discussion Questions (Full Group)

**Open floor for questions and concerns:**

1. **For RDK context:**
   - How might AI help with managing github.com/rdkcentral?
   - What are your biggest concerns about using AI in your workflow?
   - What would make you comfortable trying AI for your pain points?

2. **Practical concerns:**
   - How do you verify AI output is correct?
   - What happens when AI costs scale up?
   - How do you prevent vendor lock-in?

3. **Getting started:**
   - What's the lowest-risk way to try AI?
   - What would success look like for your team?

## Exercises

### Exercise 1.1: Value Assessment (10 minutes)
**Full Group Discussion** (Small group - everyone participates)

Given scenarios relevant to your RDK context, classify as:
- ✅ **High AI value:** Where LLMs meaningfully improve outcomes
- ⚠️ **Moderate value:** Where AI helps but isn't essential
- ❌ **Low/no value:** Where traditional automation is better

**Scenarios (RDK-focused):**
1. Parsing GCC compiler error messages from RDK builds (github.com/rdkcentral)
2. Explaining a CMake configuration error to a community contributor
3. Generating a PR summary from 50+ changed files across RDK modules
4. Detecting buffer overflow patterns in C/C++ code review
5. Generating shell scripts for Jenkins CI/CD pipeline steps
6. Analyzing Black Duck scan results to identify original source (your pain point #3)
7. Analyzing Coverity scan results to prioritize findings
8. Answering GitHub support questions about RDK (Slack bot use case)

**Group discussion:** Share classifications and reasoning. Focus on where AI adds value beyond automation.

**Key question:** Which of these directly addresses your pain points?

### Exercise 1.2: Cost-Benefit Quick Analysis (5 minutes)
**Full Group Discussion**

**Using your actual pain points:**
1. **Log file analysis** (pain point #1)
   - Current time: How long does it take to analyze a build failure?
   - AI-assisted: Could AI reduce this time? By how much?
   - Cost: What would AI cost per analysis? Is it worth it?

2. **Jenkins automation** (pain point #2)
   - Current: Manual intervention required?
   - AI-assisted: Could AI automate some decisions?
   - Cost: What would automated AI cost per build?

3. **Copyright scanning** (pain point #3)
   - Current: How long to identify original source with Black Duck?
   - AI-assisted: Could AI speed up source identification?
   - Cost: What would AI cost per scan?

**Group discussion:** Which pain point would benefit most from AI? Why?

## Key Details to Explore

### What AI Actually Is (in this context)
- **LLMs are not:** General intelligence, deterministic programs, always correct
- **LLMs are:** Statistical pattern matchers trained on code/text, probabilistic, best at language understanding and generation
- **For DevOps:** Think of LLMs as sophisticated text processing tools that understand context

### LLMs vs. Traditional Automation
| Aspect | Traditional Automation | LLMs |
|--------|----------------------|------|
| Determinism | Deterministic output | Probabilistic output |
| Auditability | Full traceability | Black box decisions |
| Speed | Fast (local execution) | Variable (API latency) |
| Cost | Predictable infrastructure | Per-token pricing |
| Maintenance | Code updates needed | Model updates change behavior |
| Understanding | Pattern matching only | Contextual understanding |

### Realistic Value Areas
**High value:**
- Explaining complex errors to humans
- Generating summaries and documentation
- Converting between formats with context
- Writing boilerplate/templates
- Code review assistance (not replacement)

**Moderate value:**
- Log analysis with structured output
- Test case generation (with review)
- Security scan prioritization

**Low value:**
- Deterministic parsing (use regex/tools)
- Simple transformations (use scripts)
- Performance-critical paths

### Relevance for RDK Context (C/C++ & CI/CD)

**Build failures (github.com/rdkcentral):**
- Compiler errors: Often structured → automation wins
- Configuration issues: Need context → LLMs can help explain
- Dependency conflicts: Complex reasoning → LLMs can assist
- **Your pain point #1:** Log file analysis - AI can help explain complex failures

**Security (CodeQL, Coverity):**
- Pattern detection: Use CodeQL, Coverity (deterministic tools)
- Explaining vulnerabilities: LLMs can help communicate risks
- Fix suggestions: LLMs can propose, but human review critical

**Copyright scanning (Black Duck):**
- **Your pain point #3:** Identifying original source when Black Duck has multiple/no matches
- AI can analyze code snippets and suggest original source
- Human review always required for final attribution
- **We'll cover this in Part 3:** AI-Assisted Black Duck Source Identification

**Test generation:**
- Boilerplate: LLMs good at generating test structure
- Edge cases: LLMs can suggest, but UB detection needs tooling
- Review always required for C/C++ (UB, memory safety)

**Jenkins automation:**
- **Your pain point #2:** Running AI as automated task with Jenkins
- AI can analyze logs, prioritize alerts, generate summaries
- Cost considerations: Per-build AI costs vs. time savings
- **We'll cover this in Part 2:** AI Automation with Jenkins

## Transition to Part 2

After this discussion, we move to **hands-on exploration** of AI tools addressing YOUR pain points:

- **Lab 1: Build/Log Failure Triage** → Addresses your pain point #1 (log file analysis)
  - Using github.com/rdkcentral build logs
  - Comparison: automation vs. AI
  
- **Lab 2: C/C++ Unit Test Generation** → Safe patterns for RDK code
  - Using RDK code examples
  - Acceptance checklist for C/C++ safety

- **Lab 3: AI Automation with Jenkins** → Addresses your pain point #2 (Jenkins automation)
  - Integrating AI into Jenkins pipelines
  - Cost considerations for automated AI tasks

**Key takeaway:** AI is a tool in your toolbox, not a replacement for good engineering practices. We'll show you how to use it safely and effectively for YOUR specific pain points.

