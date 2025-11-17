# Part 4: GitHub & AI in Practice

**Duration:** 45 minutes (12:15-13:00)  
**Format:** Live Demos + Hands-on Practice

## Learning Objectives

By the end of this section, participants will:
- Use GitHub Copilot and Copilot Chat effectively for infrastructure code
- Generate PR summaries using AI
- Parse and analyze logs with AI assistance
- Understand GitHub's AI integrations beyond Copilot
- Evaluate GitHub Teams vs. Enterprise for their context

## Key Topics

- Using GitHub Copilot and Copilot Chat effectively for:
  - Infrastructure code (YAML, shell, CI/CD scripts)
  - Change set summaries from PRs and associated tickets
  - Parsing and analyzing logs
- Exploring GitHub's AI integrations beyond Copilot:
  - AI-powered PR summarization
  - Security scanning (CodeQL)
  - Issue triage
- Teams plan vs. Enterprise considerations

## Demo 1: Copilot Chat for Infrastructure Code (15 minutes)

### Scenario: Create a GitHub Actions Workflow

**Task:** Create a CI workflow for a C/C++ project using CMake.

**Traditional approach:**
- Look up GitHub Actions syntax
- Write YAML manually
- Test iteratively

**Copilot Chat approach:**

**Prompt:**
```
Create a GitHub Actions workflow for a C/C++ project that:
1. Builds with CMake (using GCC and Clang)
2. Runs tests with CTest
3. Generates coverage reports with lcov
4. Uploads coverage to Codecov
5. Only runs on PRs and pushes to main branch
```

**Demo steps:**
1. Open `.github/workflows/ci.yml`
2. Use Copilot Chat to generate the workflow
3. Review the generated code
4. Discuss what's good, what needs adjustment

**Follow-up:** Modify the workflow
- "Add a step to run CodeQL analysis"
- "Add caching for CMake build artifacts"

### Discussion Points

**What Copilot Chat does well:**
- ✅ Generates boilerplate YAML quickly
- ✅ Understands context from repository
- ✅ Can suggest improvements

**What to watch for:**
- ⚠️ May suggest deprecated actions
- ⚠️ Security: check for secrets in workflows
- ⚠️ Always review generated workflows

### Exercise 4.1: Generate Shell Script (10 minutes)

**Task:** Use Copilot Chat to generate a build script.

**Scenario:**
You need a script that:
- Clones a C dependency
- Builds it with specific CMake flags
- Installs it to a local directory
- Sets up environment variables

**Try it:**
1. Create `scripts/build-dependency.sh`
2. Use Copilot Chat to generate the script
3. Review for:
   - Security (no hardcoded secrets)
   - Error handling
   - Portability (works on different systems)

**Share results:** (2-3 volunteers)

## Demo 2: PR Change Set Summaries (15 minutes)

### Scenario: Summarize a Large PR

**Context:** PR with 50+ changed files across C/C++ modules, Jira ticket linked.

**Traditional approach:**
- Manually read through all changes
- Write summary by hand
- Time-consuming for large PRs

**GitHub AI approach:**

**Option 1: GitHub Copilot PR Summary**
- GitHub can auto-generate PR summaries (if enabled)
- Uses AI to understand changes across files

**Option 2: Copilot Chat in PR**
```
@workspace Summarize this PR in 3-5 bullet points:
- What changed
- Why it changed (if mentioned in commits)
- Any risks or testing needed
- Link to related Jira ticket: PROJ-123
```

**Demo steps:**
1. Show a sample PR with many changes
2. Use Copilot Chat to generate summary
3. Compare with manual summary (if available)
4. Adjust summary based on requirements

### Exercise 4.2: Generate PR Summary for Your Context (10 minutes)

**Task:** Practice generating PR summaries that would be useful for your team.

**Considerations from callnotes:**
- Team uses Jira for tickets
- Need to extract meaningful information
- Summaries likely go to managers/stakeholders

**Try generating a summary that includes:**
1. **What changed:** Technical changes (files, modules)
2. **Why changed:** Business/context (link to Jira ticket)
3. **Impact:** Risks, testing needed, deployment considerations
4. **Format:** Suitable for Slack/Teams update

**Prompt template:**
```
Summarize this PR for a technical manager:

PR: [PR number/link]
Jira ticket: [ticket key]

Include:
- What changed (technical summary)
- Why (business context from Jira if available)
- Risks or testing required
- Deployment considerations

Format as a Slack message (concise, bullet points).
```

**Share results:** What would you add/remove from the template?

## Demo 3: Log Parsing and Analysis (10 minutes)

### Scenario: Analyze CI Build Failure

**Context:** Build failed in CI, large log file, need to identify root cause quickly.

**Traditional approach:**
```bash
grep -i error build.log | tail -20
# Still need to read and understand
```

**Copilot Chat approach:**

**Prompt:**
```
Analyze this CI build log and identify:
1. The primary error that caused the build to fail
2. Any secondary errors
3. Suggested fix (specific, actionable)
4. Files that need to be changed

Build log:
[PASTE LOG CONTENT]

Be concise and actionable.
```

**Demo steps:**
1. Show a real (or anonymized) build failure log
2. Use Copilot Chat to analyze
3. Compare with manual grep approach
4. Discuss: When is AI faster? When is grep better?

### Exercise 4.3: Log Analysis Practice (5 minutes)

**Task:** Practice analyzing different log types.

**Scenarios:**
1. **CMake configuration error:** Missing dependency
2. **Test failure:** Flaky test, need to understand why
3. **Deployment log:** Service failed to start

**Try analyzing one of these with Copilot Chat.**

## Demo 4: Slackbot Integration - Lab 1 Output in Action (10 minutes)

### Scenario: Automated Build Failure Notifications

**Context:** You've seen Lab 1's hybrid log analysis. Now see it in production - automated Slack notifications.

**What the Slackbot Does:**
1. **PR Summaries:** Receives GitHub PR webhooks → Summarizes with LLM → Posts to Slack
2. **Build Failures:** Receives build logs → Uses Lab 1 hybrid analysis → Posts formatted summary to Slack

**Connection to Lab 1:**
- Lab 1 showed you how to extract errors → LLM analysis → Structured JSON
- Slackbot uses the same hybrid approach (`build_analysis.py`)
- Output goes to Slack instead of console

**Demo Steps:**
1. Show Slackbot architecture (GitHub webhook → Flask app → Slack)
2. Trigger build failure endpoint with `build_test.http`
3. Show Slack message with formatted analysis
4. Show PR summary endpoint (GitHub webhook → Slack)

**Key Points:**
- **Same Pattern:** Extract → Prompt → Structure (Lab 1)
- **Automated:** Runs automatically on webhooks
- **Cost-Effective:** Uses hybrid approach (70-90% token savings)
- **Production-Ready:** Error handling, logging, signature verification

**Code Walkthrough:**
```python
# Show them build_analysis.py - same hybrid approach as Lab 1
# Show them routes.py - webhook handling
# Show them slack_client.py - message formatting
```

**Exercise 4.4: Test Slackbot Endpoints (5 minutes)**

**Task:** Test the Slackbot endpoints.

**Option A: Build Failure Notification**
```bash
# Use build_test.http or curl
curl -X POST http://localhost:8000/build/failure \
  -H "Content-Type: application/json" \
  -d '{
    "log": "error: unknown type name...",
    "repo": "rdk/telemetry",
    "branch": "main",
    "build_url": "https://jenkins.example.com/build/123"
  }'
```

**Option B: PR Summary (via GitHub Webhook)**
- Create a test PR
- Configure webhook to point to Slackbot
- Show Slack message

**Discussion:**
- How does this compare to manual Copilot Chat?
- When would you use automated vs. manual?
- What other webhooks could you add?

## GitHub AI Integrations Beyond Copilot

### AI-Powered PR Summarization (Automatic)

**Feature:** GitHub can auto-generate PR summaries (if enabled in settings).

**How it works:**
- Analyzes code changes across files
- Understands commit messages
- Generates summary automatically

**When useful:**
- Large PRs (saves reviewer time)
- Cross-module changes
- Quick overview before detailed review

**Limitations:**
- May miss nuanced changes
- Doesn't understand business context (link to Jira manually)
- Should always be reviewed/edited by humans

### Security Scanning: CodeQL

**Context:** Team already uses CodeQL (noted in callnotes) for security and secrets.

**How AI enhances CodeQL:**

**1. Query Writing:**
- Use Copilot Chat to help write CodeQL queries
- "Write a CodeQL query to find unsafe strcpy usage"

**2. Result Explanation:**
- Use AI to explain CodeQL findings
- "Explain why this CodeQL alert is high severity"

**3. Fix Suggestions:**
- AI can suggest fixes for CodeQL findings
- **Important:** Always review fixes (AI may suggest insecure code)

**Demo:** 
- Show a CodeQL alert in GitHub
- Use Copilot Chat to explain the finding
- Generate a fix suggestion (with caveats)

### Issue Triage

**Feature:** GitHub can help categorize and prioritize issues.

**Use cases:**
- **Categorization:** Bug vs. feature vs. documentation
- **Priority suggestion:** Based on issue content
- **Duplicate detection:** Find similar issues

**Example prompt:**
```
Analyze this GitHub issue and:
1. Categorize (bug/feature/documentation/other)
2. Suggest priority (P0/P1/P2/P3)
3. Identify if this might be a duplicate (search for similar issues)
4. Suggest assignee based on code areas mentioned

Issue:
[ISSUE CONTENT]
```

**Limitations:**
- Priority suggestions are estimates (human decides)
- Duplicate detection needs verification
- Use as assistance, not automation

### "Ask Me Anything" (AMA) Patterns

**Context:** Team wants to use Copilot for "Ask Me Anything" (noted in callnotes).

**What works well:**
- ✅ "Explain this code"
- ✅ "How do I...?" (procedural questions)
- ✅ "What does this function do?"
- ✅ "Find similar patterns in this repo"

**What to be cautious with:**
- ⚠️ Security decisions (always verify)
- ⚠️ License questions (legal review needed)
- ⚠️ Architectural decisions (team consensus)

**Example prompts that help infra teams:**
```
"How do I add caching to this GitHub Actions workflow?"
"Explain this CMake configuration error"
"Find all places where we use strcpy in this codebase"
"What are the security implications of this code pattern?"
```

## Teams Plan vs. Enterprise Considerations

### From Callnotes
- Team is considering GitHub Copilot
- Question: Teams plan vs. Enterprise?
- **Context:** Comcast signed license to allow AI use, but need "gatekeeper"

### Differences

**Teams Plan:**
- ✅ Lower cost per user
- ✅ Basic Copilot features
- ✅ Suitable for smaller teams
- ⚠️ Limited admin controls
- ⚠️ Less fine-grained policy enforcement

**Enterprise Plan:**
- ✅ Advanced admin controls
- ✅ Policy enforcement (can restrict features)
- ✅ Audit logging
- ✅ Better for "gatekeeper" requirements
- ⚠️ Higher cost
- ⚠️ More complex setup

### For Comcast/Sky Context

**"Is it AI or not?" Gatekeeper Requirements:**

**Enterprise features that help:**
- **Allow-list:** Restrict which repos can use Copilot
- **Audit logs:** Track all Copilot usage
- **Policy enforcement:** Block Copilot for sensitive repos
- **Data controls:** Ensure code doesn't leave organization

**Questions to consider:**
1. Do you need to restrict Copilot to certain repos? → **Enterprise**
2. Do you need detailed audit logs? → **Enterprise**
3. Is basic Copilot enough for your team? → **Teams might work**

**Recommendation:** Start with Teams (if cost-sensitive), evaluate Enterprise if you need stricter controls.

## Hands-On Practice Session (10 minutes)

### Exercise 4.5: Infrastructure Code Generation

**Choose one:**

**Option A: GitHub Actions Workflow**
- Generate a workflow for your specific use case
- Add steps for: build, test, security scan, deploy

**Option B: Dockerfile/Container Setup**
- Generate Dockerfile for C/C++ build environment
- Include: dependencies, build tools, test frameworks

**Option C: CI Script**
- Generate shell script for local CI
- Include: build, test, coverage, linting

**Requirements:**
1. Use Copilot Chat to generate initial code
2. Review for security (no secrets, proper error handling)
3. Test that it works (or identify what needs fixing)
4. Document what AI got right/wrong

### Exercise 4.6: PR Summary for Stakeholders

**Task:** Generate a PR summary suitable for non-technical stakeholders.

**Context:** Large PR with many changes, needs to be explained to managers.

**Requirements:**
1. Use Copilot Chat to generate summary
2. Adjust language for non-technical audience
3. Include business impact (link to Jira ticket)
4. Format for Slack/email

**Try it:** Use a real PR or create a sample scenario.

## Discussion Questions

1. **Workflow Integration:**
   - How would you integrate Copilot Chat into your daily workflow?
   - What tasks would you delegate to AI? What would you keep manual?

2. **Security Concerns:**
   - Are you comfortable using Copilot for infrastructure code?
   - What safeguards would you want in place?

3. **Teams vs. Enterprise:**
   - What factors matter most for your team? (Cost, controls, audit?)
   - How would you make the decision?

4. **Beyond Copilot:**
   - What other GitHub AI features would be most valuable?
   - CodeQL + AI? Issue triage? What else?

## Key Details to Explore

### Effective Prompting for Infrastructure Code

**Good prompts:**
- Specific requirements (languages, tools, versions)
- Include context (existing code, constraints)
- Request explanations ("Explain why you chose this approach")

**Example:**
```
BAD: "Create a CI workflow"
GOOD: "Create a GitHub Actions workflow for a C/C++ project using CMake. Use GCC and Clang compilers, run tests with CTest, generate coverage with lcov. Only run on PRs and main branch. Cache CMake build artifacts."
```

### Copilot Chat Best Practices

**1. Use @workspace for repository context:**
```
@workspace How does this function work?
```
(Copilot uses code in your workspace for context)

**2. Iterate and refine:**
- Generate initial code
- Ask follow-up questions
- Refine based on needs

**3. Always review:**
- Don't blindly accept suggestions
- Check for security issues
- Verify it matches your requirements

**4. Learn from suggestions:**
- Understand why AI suggested certain approaches
- Use as learning tool, not just code generator

### Log Analysis Patterns

**When to use AI vs. grep:**
- **Use grep/regex:** Simple patterns, fast filtering
- **Use AI:** Complex errors, need explanation, unstructured logs

**Example workflow:**
1. **Grep first:** Filter to relevant sections
   ```bash
   grep -A 10 "error" build.log > errors.txt
   ```
2. **AI second:** Analyze filtered output
   ```
   Analyze these error sections and identify root cause...
   [PASTE errors.txt]
   ```

### Integration with Existing Tools

**From callnotes, team uses:**
- **Jira:** For tickets
- **Slack:** For team communication
- **CodeQL:** For security scanning
- **Coverity/Black Duck:** For security/license scanning

**How AI can connect these:**
1. **PR → Jira:** AI can extract Jira ticket references from PRs
2. **CodeQL → Slack:** AI can generate Slack alerts from CodeQL findings
3. **Jira → Summary:** AI can summarize Jira tickets for reports

**Discussion:** What integrations would be most valuable for your team?

## Transition to Part 5

Next: **Metrics, Insights & Reporting**
- Using AI to generate actionable insights from GitHub/Jira data
- Creating concise summaries for decision-makers
- DORA metrics and productivity analysis

