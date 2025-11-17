# Part 2: AI Tools for DevOps – Landscape and C/C++ Use Cases

**Duration:** 1 hour (10:00-11:00)  
**Format:** Hands-on Lab + Tool Landscape Overview

## Learning Objectives

By the end of this section, participants will:
- **Address your pain point #1:** Log file analysis (Lab 1)
- Compare traditional automation vs. AI-assisted approaches
- Understand prompt engineering for actionable outputs
- Apply hybrid approach (deterministic + LLM) for production use
- Understand categories of AI tools available for DevOps
- Recognize when to use commercial vs. open-source tools
- **Output from Lab 1 will be used for Slack bots in Part 4** ⭐

## Key Topics

- Log parsing and build failure analysis (Lab 1)
- Categories of AI tools: code intelligence, monitoring, QA, pipelines
- Commercial vs. open-source tools overview
- When to use each type of tool
- **Note:** Unit test generation → Part 4 (GitHub & AI in Practice)
- **Note:** Security scanning → Part 3 (Security in AI-Enabled DevSecOps)
- **Note:** License scanning → Part 3 (Black Duck focus)
- **Note:** Jenkins automation → Part 4 (CI/CD integration) or optional/homework

## Lab 1: Build/Log Failure Triage (45 minutes)
**Addresses your pain point #1: Log file analysis**

### Objectives
- Compare traditional automation vs. AI-assisted log analysis
- Understand prompt engineering for actionable outputs
- Generate triage comments suitable for PRs
- **Apply to your RDK context:** Analyze github.com/rdkcentral build logs

### Materials Provided
- **Real RDK build log:** `build.log` (173 lines, realistic RDK telemetry component build)
- **Scripts from Part 1:**
  - `01_grep.sh` - Grep/awk approach
  - `02_python_analysis.py` - Python approach
  - `03_llm_api_call.py` - LLM approach (full log)
  - `04_hybrid_approach.py` - Hybrid approach (recommended) ⭐
- Sample baseline scripts (grep/awk/jq, Python)

### RDK Context
**You're analyzing build logs from github.com/rdkcentral** - the RDK Software Stack codebase you manage. This directly addresses your pain point: understanding build failures quickly.

### Exercise 2.1: Baseline Automation (15 minutes)

**Task:** Use the scripts from Part 1 to analyze the RDK build log.

**Option A: Use grep script**
```bash
cd part-01-demystifying-ai/resources
./01_grep.sh
```

**Option B: Use Python script**
```bash
cd part-01-demystifying-ai/resources
python3 02_python_analysis.py
```

**Option C: Write your own**
- Use `build.log` from resources
- Extract top 3 error patterns
- Compare with scripts from Part 1

**Deliverable:** 
- Output showing top 3 error patterns
- Note: execution time, accuracy, maintainability
- **For your RDK context:** How would you use this for github.com/rdkcentral builds?

### Exercise 2.2: AI-Assisted Analysis (20 minutes)

**Task:** Use LLM approaches to analyze the RDK build log.

**Option A: Full log approach** (from Part 1)
```bash
cd part-01-demystifying-ai/resources
python3 03_llm_api_call.py
```
- Uses entire build.log
- Good for complex analysis
- More expensive (~$0.04-0.10 per analysis)

**Option B: Hybrid approach** (recommended) ⭐
```bash
cd part-01-demystifying-ai/resources
python3 04_hybrid_approach.py
```
- Filters errors deterministically first
- Sends only relevant sections to LLM
- 70-90% cost savings (~$0.004-0.01 per analysis)
- **Best for production use**

**Prompt Template** (from `03_llm_approach.md`):
```
You are assisting the RDK CMF team. Analyse the following CI build log.

Return:
1) A JSON array of the top 3 failure causes with fields:
   cause, evidence (line numbers or snippets), confidence (high/medium/low), next_action.
2) A 3-bullet human summary.

Prefer evidence over speculation. If uncertain, mark confidence low.
```

**Tools to use:**
- **Online:** GitHub Copilot Chat, OpenAI (GPT-4o), Anthropic (Claude)
- **Offline:** Ollama with `codellama:7b` or `llama3:latest`

**Deliverable:** 
- LLM output with confidence levels
- Compare precision/recall vs. baseline script
- **For your RDK context:** Which approach would you use for github.com/rdkcentral builds?
- **Cost comparison:** Full log vs. hybrid approach

### Exercise 2.3: Prompt Hardening (10 minutes)

**Task:** Refine the prompt to improve accuracy and reduce hallucinations.

**Considerations:**
- Add constraints: "Only report errors that appear in the log"
- Request citations: "Quote the exact log line for each root cause"
- Add guardrails: "If confidence is Low, explain what information is missing"

**Deliverable:** Improved prompt that produces more reliable output.

### Debrief Discussion
- **Precision/Recall:** Did the LLM find real issues? Did it hallucinate?
- **Actionability:** Were the suggested fixes actually useful?
- **Token Discipline:** How much did this cost? How could you reduce token usage?
- **When to use each:** Automation vs. AI-assisted?
- **For your pain point #1 (log file analysis):**
  - How much time does this save vs. manual analysis?
  - Which approach (grep/Python/LLM/Hybrid) would you use in production?
  - What's the cost per analysis? Is it worth it?
- **Hybrid approach benefits:**
  - 70-90% cost savings vs. full log
  - Deterministic filtering (auditable)
  - LLM analysis (intelligent)
  - **Recommended for production use**

## Tool Landscape Overview (15 minutes)

**Note:** Deep dive on specific tools deferred to Part 4 (GitHub & AI in Practice) and Part 6 (Reflection & Planning)

### Categories of AI Tools

#### Code Intelligence
- **GitHub Copilot:** Inline completions, chat (covered in Part 4)
- **Tabnine:** Multi-language, privacy-focused
- **Amazon CodeWhisperer:** AWS-integrated
- **Sourcegraph Cody:** Code search + AI

#### Monitoring & Observability
- **AI-powered log analysis:** Custom LLM prompts (Lab 1)
- **Anomaly detection:** Combining AI with traditional metrics
- **Incident response:** AI-assisted runbooks

#### QA & Testing
- **Test generation:** Unit, integration tests (covered in Part 4 with Copilot)
- **Test case prioritization:** Using AI to identify critical paths
- **Code review assistance:** Not replacement, but aid

#### Pipelines & CI/CD
- **YAML generation:** GitHub Actions, Docker Compose (Part 4)
- **Build script generation:** Shell, Makefiles
- **Deployment automation:** Infrastructure as Code assistance
- **Jenkins integration:** (Optional/homework - see `labs/lab-3-jenkins/`)

### Commercial vs. Open Source

**Commercial Tools:**
- **GitHub Copilot** - Integrated with GitHub workflow (Part 4)
- **Tabnine** - Privacy-focused, on-premises option
- **Amazon CodeWhisperer** - Free tier, AWS integration
- **Sourcegraph Cody** - Strong code search + AI

**Open Source / Self-Hosted:**
- **Ollama** - Free, runs locally, no data sent externally
- **GPT4All** - Completely offline
- **Code Llama** - Specialized for code, C/C++ support

### When to Use Each

**For RDKM/CMF context:**
- **Data sensitivity:** Use self-hosted tools (Ollama) for sensitive logs
- **Cost control:** Start with free/open-source, evaluate commercial later
- **Governance:** Need "is it AI or not?" gate → log all tool usage
- **C/C++ focus:** Verify tool support for C/C++ syntax and build systems
- **RDK context:** Managing github.com/rdkcentral - which tools work best?

### Discussion Questions

1. Which tools fit your "gatekeeper" requirement?
2. How would you handle the Teams vs. Enterprise Copilot decision?
3. What's your fallback if commercial tools become too expensive?
4. **For your pain points:** Which tools address log analysis, Jenkins automation, copyright scanning?
5. **Hybrid approach:** Would you use deterministic filtering + LLM for production?

**Deep dive:** We'll explore specific tools in Part 4 (GitHub & AI in Practice) and Part 6 (Reflection & Planning)

---

## What's Next?

**Lab 1 output will be used in Part 4** for building Slack bots:
- The log analysis JSON output from Lab 1
- Can be integrated into Slack bot for automated build failure notifications
- See Part 4: GitHub & AI in Practice for Slack bot implementation

**Other labs moved:**
- **Unit test generation** → Part 4 (GitHub & AI in Practice) - Copilot demos
- **Jenkins automation** → Part 4 (CI/CD integration) or optional/homework
- **Security scanning** → Part 3 (Security in AI-Enabled DevSecOps)
- **License scanning** → Part 3 (Black Duck focus)

## Key Details to Explore

### License Scanning: AI + Black Duck

**Note:** This is covered in detail in Part 3 (Security in AI-Enabled DevSecOps)

**Quick overview:**
- Use Black Duck for license scanning
- **Slowest part:** Identifying original version of copied code and its license
- **How AI helps:** When Black Duck has multiple matches or no match, AI can analyze code snippets and suggest original source
- **Time savings:** AI can reduce time spent on source identification by 70-80%
- **For RDK context:** RDK uses Apache licensing, NOTICE files required

**See Part 3 for:**
- Detailed workflow
- AI-Assisted Black Duck Source Identification lab
- Jira ticket BD-1290 format example
- NOTICE file generation with AI

### Security Scanning: AI + CodeQL/Coverity

**Note:** This is covered in detail in Part 3 (Security in AI-Enabled DevSecOps)

**Quick overview:**
- CodeQL (security, secrets) - already in use
- Coverity - already in use
- **Challenge:** Too many findings, need prioritization
- **How AI helps:** Prioritization, explanation, false positive reduction
- **Never replace:** Static analysis tools, human security review, policy decisions

**See Part 3 for:**
- Detailed workflow
- AI-assisted prioritization lab
- Security risks specific to C/C++ development
- Governance and gatekeeping

### Unit Test Generation: Safe Patterns

**Note:** This is covered in Part 4 (GitHub & AI in Practice) with Copilot demos

**Quick overview:**
- Generate unit tests with AI (Copilot, ChatGPT, etc.)
- **Always review generated tests** - check for undefined behavior, memory safety
- **Use static analysis** - sanitizers (ASAN, UBSAN), compiler warnings
- **Acceptance criteria:** Compile with `-Werror`, pass sanitizers, test public API only

**See Part 4 for:**
- Copilot test generation demos
- Safety review checklist
- RDK-specific examples

## Transition to Part 4

**What we covered:**
- ✅ **Lab 1:** Log file analysis (your pain point #1) - using RDK build logs
- ✅ **Tool Landscape Overview:** Categories, commercial vs. open source, when to use each

**Key takeaways:**
- Hybrid approach (deterministic + LLM) is recommended for production
- 70-90% cost savings vs. full log analysis
- Lab 1 output (JSON) will be used for Slack bots in Part 4 ⭐
- Always apply human review for AI-generated code

**What's next:**
- **Part 4: GitHub & AI in Practice** - We'll use Lab 1 output to build Slack bots
- **Part 3: Security in AI-Enabled DevSecOps** - Security scanning, Black Duck source identification (your pain point #3)
- **Optional:** Unit test generation and Jenkins automation available as homework or in Part 4

**Lab 1 Output → Slack Bots:**
The JSON output from Lab 1 (root causes, summary) can be directly integrated into a Slack bot for automated build failure notifications. We'll build this in Part 4.

