# Quick Start Guide

## For Participants

### 1. Get the Materials

**Option A: Git Clone**
```bash
git clone <repository-url>
cd ai-devops-participant-materials
```

**Option B: Download Zip**
- Download zip file from repository
- Extract to your preferred location
- Navigate to extracted directory

### 2. Set Up Environment

```bash
# Create and activate virtual environment
python3 -m venv .venv
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

Choose one:

**OpenAI:**
```bash
export OPENAI_API_KEY="your-key-here"
```

**Anthropic:**
```bash
export ANTHROPIC_API_KEY="your-key-here"
```

**Ollama (Local):**
```bash
# Install from https://ollama.ai
# Then run: ollama serve
```

### 4. You're Ready!

- Read `README.md` for course overview
- Navigate to `part-02-ai-tools-landscape/labs/lab-1-log-triage/` for Lab 1
- Follow along with the instructor

---

**That's it!** See you in the course! 🚀

