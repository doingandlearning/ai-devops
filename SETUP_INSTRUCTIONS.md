# Setup Instructions

## Quick Start

### 1. Clone This Repository

```bash
git clone <repository-url>
cd ai-devops-participant-materials
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Or use the setup script:**
```bash
chmod +x setup_venv.sh
./setup_venv.sh
```

### 3. Configure LLM Access

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
# Then run in another terminal:
ollama serve
```

### 4. Verify Setup

```bash
# Test Python environment
python --version  # Should be 3.8+

# Test imports
python -c "import requests; print('✅ requests installed')"
python -c "import openai; print('✅ openai installed')"  # If using OpenAI
```

## Directory Structure

```
.
├── README.md                    # Main guide
├── COURSE_OVERVIEW.md          # Course overview
├── requirements.txt            # Python dependencies
├── setup_venv.sh               # Setup script
│
├── part-01-demystifying-ai/    # Part 1 materials
├── part-02-ai-tools-landscape/ # Part 2 + Lab 1
├── part-03-security-devsecops/ # Part 3 + slides
├── part-04-github-ai-practice/ # Part 4 + slides
├── part-05-metrics-insights/   # Part 5 + Lab 4
├── part-06-reflection-planning/ # Part 6
└── resources/
    ├── lab-1-solutions/        # Lab 1 solutions (reference)
    └── slackbot/               # Slackbot example
```

## Next Steps

1. Read `README.md` for course overview
2. Read `COURSE_OVERVIEW.md` for detailed course flow
3. Navigate to `part-02-ai-tools-landscape/labs/lab-1-log-triage/` for Lab 1
4. Follow along with the instructor during the course

## Troubleshooting

**Python not found?**
- Install Python 3.8+ from python.org
- Or use `brew install python3` on macOS

**pip install fails?**
- Try: `pip install --upgrade pip`
- Or: `python3 -m pip install -r requirements.txt`

**LLM API errors?**
- Verify your API key is set: `echo $OPENAI_API_KEY`
- Check API key is valid
- For Ollama: Make sure `ollama serve` is running

**Permission denied on scripts?**
```bash
chmod +x setup_venv.sh
chmod +x part-01-demystifying-ai/resources/*.sh
chmod +x resources/lab-1-solutions/*.sh
```

## Support

- Check each part's `README.md` for detailed instructions
- Solution scripts are in `resources/lab-1-solutions/` (reference only)
- Ask questions during the course!

---

**Ready to start!** 🚀

