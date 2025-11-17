# Course Overview: Practical AI for DevSecOps

**Duration:** One day  
**Format:** Hands-on labs, demos, and discussions

---

## What You'll Learn

Today you'll explore how AI can help with YOUR specific DevSecOps challenges:

1. **Log file analysis** - Triage build failures faster
2. **Copyright scanning** - Speed up Black Duck source identification
3. **Metrics & reporting** - Generate business briefs automatically
4. **GitHub integration** - Use AI in your existing workflows

---

## Course Flow

### **Part 1: Demystifying AI (30 min)**
- What AI is (and isn't) in DevOps
- Mental models: "Ruler vs. Intern"
- Value triage: Where does AI help?
- Risk → Mitigation mapping

### **Part 2: AI Tools Landscape (1 hour)**
- **Lab 1: Log Triage** ⭐
  - Compare 4 approaches (grep → Python → LLM → Hybrid)
  - Hands-on with real RDK build logs
  - Learn the hybrid approach (70-90% cost savings)

### **Part 3: Security & Governance (1 hour)**
- **Mini-Lab A: Black Duck Source Identification** ⭐
  - AI-assisted copyright attribution
  - Uses BD-1290 pattern (your real workflow)
  - 70-80% time savings
- **Mini-Lab B: PR Gate for AI Code**
- Security guardrails: "Evidence or it doesn't ship"

### **Part 4: GitHub & AI in Practice (45 min)**
- Copilot Chat demos
- PR summaries
- Log analysis
- **Slackbot integration** (Lab 1 output in action!)
- **Slackbot code available** in `resources/slackbot/`

### **Part 5: Metrics & Reporting (45 min)**
- **Lab 4: Generate Weekly Briefs** ⭐
  - Extract GitHub/Jira data
  - Generate business briefs with AI
  - Track costs and ROI

### **Part 6: Reflection & Planning (45 min)**
- Create your adoption roadmap
- Three-tier plan: Adopt Now / Pilot / Avoid
- Governance policy template
- Next steps

---

## Key Concepts

### **Hybrid Approach** ⭐
- Deterministic filtering + LLM analysis
- 70-90% cost savings vs. full log analysis
- Recommended for production

### **Pattern: Extract → Prompt → Structure**
- Same pattern across all labs
- Extract relevant data first
- Construct intelligent prompts
- Get structured outputs

### **Security Guardrails**
- AI generates suggestions
- Humans review and decide
- Always require evidence
- Never trust blindly

---

## What You'll Take Away

### **Immediate (This Week):**
- Lab 1 scripts (log triage)
- Black Duck assistant script
- Understanding of hybrid approach
- Cost tracking scripts

### **Short-Term (This Month):**
- Metrics/reporting workflow
- Governance policy template
- Adoption roadmap
- Slackbot example (can adapt)

### **Long-Term (This Quarter):**
- Pattern: Extract → Prompt → Structure
- Cost discipline mindset
- Security guardrails
- Practical AI adoption strategy

---

## Prerequisites

- **Python 3.8+** installed
- **LLM access** (OpenAI, Anthropic, or Ollama)
- **Text editor** or IDE
- **GitHub account** (for Part 4)

---

## Setup Instructions

See `README.md` for detailed setup instructions.

**Quick start:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Course Materials

All materials are in this directory:
- Lab scripts and solutions
- Example data files
- Prompt templates
- Policy templates

---

**Let's get started!** 🚀

