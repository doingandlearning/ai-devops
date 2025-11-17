# Part 4: GitHub & AI in Practice

---

## Copilot Chat for Infrastructure Code

### What You'll See

**Demo:**
- Generate GitHub Actions workflow
- Generate shell scripts
- Review generated code

**Key Point:**
> Copilot Chat = LLM wrapper

*You can use it OR build your own*

---

## PR Summaries

### What You'll See

**Two Approaches:**

1. **Manual:** Copilot Chat in PR
   - One-off analysis
   - Interactive

2. **Automated:** Slackbot webhook
   - Runs automatically
   - Same pattern as Lab 1

**Remember Lab 1? Same pattern here!**

---

## Log Analysis

### What You'll See

**Demo:**
- Copilot Chat analyzing build logs
- Compare with Lab 1 hybrid approach

**Key Point:**
> Both use LLMs. One is manual, one is automated.

*Choose based on your use case*

---

## Slackbot Integration

### Lab 1 Output → Production

```
GitHub Webhook → Flask App → LLM → Slack
```

**What it does:**
- Receives build logs
- Uses Lab 1 hybrid approach
- Posts formatted summary to Slack

**Same code, different output format!**

---

## GitHub AI = LLM Wrappers

### Key Takeaway

- ✅ Copilot = LLM wrapper
- ✅ You can build your own
- ✅ Same pattern: Extract → Prompt → Structure

**The difference:**
- Copilot: Manual, integrated
- Your solutions: Automated, tailored

*Choose based on your use case*

---

## GitHub AI Integrations

### What's Available

- **PR Summarization:** Auto-generated summaries
- **CodeQL + AI:** Query writing, result explanation
- **Issue Triage:** Categorization, prioritization
- **Copilot Chat:** Code generation, explanations

**All are LLM wrappers. You can build similar things.**

---

## Teams vs. Enterprise

### For Your Context

**Enterprise features:**
- ✅ Advanced admin controls
- ✅ Policy enforcement
- ✅ Audit logging
- ✅ Better for "gatekeeper" requirements

**Recommendation:**
Start with Teams, evaluate Enterprise for stricter controls

---

## Takeaway

> "GitHub AI integrates with your existing workflow - start with low-risk use cases."

**Remember:**
- Same pattern: Extract → Prompt → Structure
- GitHub provides structured data
- You can use Copilot OR build your own

