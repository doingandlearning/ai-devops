# Practical AI for DevSecOps - Participant Materials

**Welcome!** This directory contains all the materials you'll need for today's course.

## Course Structure

- **Part 1:** Demystifying AI (30 min)
- **Part 2:** AI Tools Landscape & Lab 1 (1 hour)
- **Part 3:** Security, Licensing & Governance (1 hour)
- **Part 4:** GitHub & AI in Practice (45 min)
- **Part 5:** Metrics, Insights & Reporting (45 min)
- **Part 6:** Reflection & Planning (45 min)

## Quick Start

### 1. Set Up Environment

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Or use the setup script
chmod +x setup_venv.sh
./setup_venv.sh
```

### 2. Get LLM Access

You'll need access to an LLM for the labs. Choose one:

**Option A: OpenAI**
```bash
export OPENAI_API_KEY="your-key-here"
```

**Option B: Anthropic**
```bash
export ANTHROPIC_API_KEY="your-key-here"
```

**Option C: Ollama (Local)**
```bash
# Install Ollama from https://ollama.ai
ollama serve  # Run in another terminal
```

### 3. Navigate to Labs

- **Lab 1:** `part-02-ai-tools-landscape/labs/lab-1-log-triage/`
- **Lab 3:** `part-03-security-devsecops/resources/`
- **Lab 4:** `part-05-metrics-insights/resources/`

## Directory Structure

```
participant-materials/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── setup_venv.sh                      # Setup script
│
├── part-01-demystifying-ai/           # Part 1 materials
│   ├── README.md
│   └── resources/                     # Demo scripts & build.log
│
├── part-02-ai-tools-landscape/       # Part 2 materials
│   ├── README.md
│   └── labs/
│       └── lab-1-log-triage/          # Lab 1: Log Triage
│
├── part-03-security-devsecops/       # Part 3 materials
│   ├── README.md
│   ├── slides.md                      # Optional slides
│   └── resources/                     # Black Duck assistant
│
├── part-04-github-ai-practice/        # Part 4 materials
│   ├── README.md
│   ├── slides.md                      # Optional slides
│   └── resources/                     # GitHub examples
│
├── part-05-metrics-insights/          # Part 5 materials
│   ├── README.md
│   └── resources/                     # Metrics scripts
│
├── part-06-reflection-planning/      # Part 6 materials
│   └── README.md
│
└── resources/
    ├── lab-1-solutions/                # Lab 1 solution scripts (reference)
    └── slackbot/                        # Slackbot example (Lab 1 in production)
```

## Key Resources

### Lab Scripts

**Lab 1 - Log Triage:**
- `part-02-ai-tools-landscape/labs/lab-1-log-triage/` - Your lab directory
- `resources/lab-1-solutions/` - Solution scripts (reference only)

**Lab 3 - Black Duck:**
- `part-03-security-devsecops/resources/blackduck_ai_assistant.py`

**Lab 4 - Metrics:**
- `part-05-metrics-insights/resources/pull_github_data.py`
- `part-05-metrics-insights/resources/pull_jira_data.py`
- `part-05-metrics-insights/resources/generate_weekly_summary.py`

**Slackbot Example:**
- `resources/slackbot/` - Working Slackbot (Lab 1 output in production)

### Slides

- Part 1: See instructor's presentation
- Part 2: See instructor's presentation
- Part 3: `part-03-security-devsecops/slides.md` (optional)
- Part 4: `part-04-github-ai-practice/slides.md` (optional)

## What You'll Need

- **Laptop** with Python 3.8+
- **LLM access** (OpenAI, Anthropic, or Ollama)
- **GitHub account** (for Part 4 demos)
- **Text editor** or IDE

## Getting Help

- Check each part's `README.md` for detailed instructions
- Solution scripts are in `resources/lab-1-solutions/` (reference only)
- Ask questions during the course!

## Course Objectives

By the end of the day, you will:
- ✅ Understand where AI fits into DevSecOps workflows
- ✅ Have hands-on experience with log triage (Lab 1)
- ✅ Know how to use AI for copyright attribution (Part 3)
- ✅ Understand GitHub AI integrations (Part 4)
- ✅ Generate metrics and reports with AI (Lab 4)
- ✅ Have a practical roadmap for AI adoption (Part 6)

## Important Notes

- **Lab 1 output** will be used in Part 4 (Slackbot demo)
- **Hybrid approach** is recommended for production (70-90% cost savings)
- **Security guardrails** are non-negotiable (Part 3)
- **Cost discipline** matters - track everything (Part 5)

---

**Enjoy the course!** 🚀
