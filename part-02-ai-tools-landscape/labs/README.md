# Part 2 Labs

This directory contains all hands-on labs for Part 2: AI Tools for DevOps.

## Lab Structure

- **`lab-1-log-triage/`** - Build/Log Failure Triage (45 min)
- **`lab-2-c-tests/`** - C/C++ Unit Test Generation (30 min)
- **`lab-3-jenkins/`** - AI Automation with Jenkins (30 min)

## Setup

### Prerequisites

```bash
# From repo root
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Resources

Solution scripts are in `../../../../resources/lab-1-solutions/`

## Lab 1: Build/Log Failure Triage

**Time:** 45 minutes  
**Addresses pain point #1: Log file analysis**

Compare deterministic automation vs. AI-assisted log analysis.

- Exercise 2.1: Baseline automation (grep/Python)
- Exercise 2.2: AI-assisted analysis (full log vs. hybrid)
- Exercise 2.3: Prompt hardening

See `lab-1-log-triage/README.md` for details.

## Lab 2: C/C++ Unit Test Generation

**Time:** 30 minutes  
**Safe patterns for RDK code**

Generate unit tests with AI, then reject unsafe ones.

- Exercise 2.4: Manual baseline
- Exercise 2.5: AI test generation
- Exercise 2.6: Safety review

See `lab-2-c-tests/README.md` for details.

## Lab 3: AI Automation with Jenkins

**Time:** 30 minutes  
**Addresses pain point #2: Running AI as automated task with Jenkins**

Integrate AI into Jenkins pipelines for automated build failure analysis.

- Exercise 2.8: Jenkins AI integration
- Exercise 2.9: Cost & ROI analysis

See `lab-3-jenkins/README.md` for details.

## Solutions

Solution scripts are in `../../../../resources/lab-1-solutions/`

**Note:** Try writing your own first, then compare with solutions.

## RDK Context

All labs are designed for **github.com/rdkcentral** - the RDK Software Stack codebase managed by the CMF team.

**Pain points addressed:**
- Lab 1: Log file analysis
- Lab 3: Jenkins AI automation
- Lab 2: Safe test generation for RDK components

