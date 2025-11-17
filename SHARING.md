# Sharing This Repository

## For Instructors

This repository contains all participant materials for the "Practical AI for DevSecOps" course.

### Sharing Options

**Option 1: GitHub (Recommended)**
```bash
# Create a new repository on GitHub
# Then push:
git remote add origin https://github.com/your-org/ai-devops-participant-materials.git
git branch -M main
git push -u origin main
```

**Option 2: GitLab**
```bash
# Create a new repository on GitLab
git remote add origin https://gitlab.com/your-org/ai-devops-participant-materials.git
git branch -M main
git push -u origin main
```

**Option 3: Zip File**
```bash
# Create a zip (excluding .git)
zip -r ai-devops-participant-materials.zip . -x "*.git*" ".venv/*" "__pycache__/*"
```

**Option 4: Private Git Server**
```bash
# Set up on your internal Git server
git remote add origin <your-git-server-url>
git push -u origin main
```

### Before Sharing

1. ✅ Review `.gitignore` - ensure sensitive data is excluded
2. ✅ Remove any API keys or secrets
3. ✅ Test that setup works: `./setup_venv.sh`
4. ✅ Verify all files are included: `git status`

### What's Included

- ✅ All course materials (Parts 1-6)
- ✅ Lab scripts and solutions
- ✅ Example data files
- ✅ Setup scripts
- ✅ Documentation

### What's Excluded

- ❌ Instructor guides (internal only)
- ❌ Course reviews (internal only)
- ❌ API keys or secrets
- ❌ Personal notes
- ❌ Git history from main repo

## For Participants

### Getting Started

1. **Clone or download** this repository
2. **Follow** `SETUP_INSTRUCTIONS.md`
3. **Read** `README.md` for course overview
4. **Join** the course session!

### Requirements

- Python 3.8+
- LLM API access (OpenAI, Anthropic, or Ollama)
- Text editor or IDE
- GitHub account (for Part 4)

---

**Questions?** Contact your instructor.

