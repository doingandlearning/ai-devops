# Part 3 — Security, Licensing & Governance (Reframed)

**Duration:** 60 mins (14:00–15:00)
**Format:** Two mini-labs + short design huddle
**Theme:** if it doesn’t cite evidence, it doesn’t ship.

## Outcomes

* A 1-page **AI Security & Licensing Guardrails** tailored to RDKM/CMF.
* A working **“Is it AI?” PR gate** (label + check).
* An AI-drafted **NOTICE/LICENCE snippet** with evidence for BD-style tickets.

---

## Minute-by-minute

**00–15 — Security Risks Discussion (15 min)**

* **Opening:** "What security risks do YOU see with AI in your workflow?"
* **Whiteboard:** Capture their concerns in real-time
* **Guide discussion:** Don't lecture, let them share
* **Connect to context:** C/C++ code, RDK, Black Duck
* **Expected risks:** Unsafe code, prompt injection, copyright errors, vendor lock-in, cost at scale

**15–20 — Connect to Their Lived Experience (5 min)**

* **Remind them:** "This is your pain point #3 - copyright scanning"
* **Show BD-1290 ticket:** "This is what you deal with"
* **Frame the problem:** "Black Duck finds matches, but YOU have to identify the original source"
* **Ask:** "What's the slowest part? What takes most time?"
* **Transition:** "You've seen this pattern before - remember Lab 1? Same pattern here: Tools → Extract → Prompt → Report"

**20–35 — Hands-on Lab: Same Flow as Lab 1 (15 min)**

**Mini-Lab A: License/IP (Black Duck reality)**
Using the BD-1290 pattern you shared.

**Flow: Tools → Extract → Prompt → Report**

**Step 1: Tools You Already Have**
* Black Duck reports (BD-1290 ticket)
* Source files (wifi_hal.c)
* These are your existing tools

**Step 2: Extract Relevant Context**
* Run extraction script to get only referenced code sections
* Reduces token usage by 99% (same hybrid approach as Lab 1)
* Saves as `compliance/extracted_code.json`

**Step 3: Construct Intelligent Prompt**
* Use structured prompt template (below)
* Include BD report notes for context
* Request structured JSON output with evidence

**Step 4: Produce Readable Report**
* LLM generates compliance suggestions
* Structured JSON with evidence citations
* Confidence levels and review flags

**Task**

1. Run the extraction script:
```bash
cd resources
python3 blackduck_ai_assistant.py \
  --bd-report bd-report.txt \
  --source wifi_hal.c \
  --outdir compliance \
  --extract-only
```

2. Review extracted code sections (`compliance/extracted_code.json`)

3. Run full analysis with LLM:
```bash
python3 blackduck_ai_assistant.py \
  --bd-report bd-report.txt \
  --source wifi_hal.c \
  --outdir compliance \
  --model gpt-4o
```

4. Review structured output (`compliance/ai_notice.json`)

**Prompt Template:**

```
Role: RDKM compliance assistant.
Task: Draft NOTICE and LICENSE addenda for the snippet below.

Return JSON:
{
  "notice_additions": ["..."],
  "license_additions": ["..."],
  "evidence": [{"file":"{{ PATH }}","lines":[START,END],"why":"..."}],
  "confidence":"high|medium|low",
  "review_required": true
}

Rules:
- Only cite text present in the snippet or in the BD notes below.
- If source isn’t provable from provided text, set confidence=low and review_required=true.
- Use RDK standard phrasing ("The component is licensed to you under the Apache License, Version 2.0...").
- Don’t invent years/names; use placeholders if uncertain: {{ YEAR }}, {{ COPYRIGHT HOLDER }}.
```

2. Save as `compliance/ai_notice.json`.

**Deliverable**

* `ai_notice.json` containing `notice_additions`, `license_additions`, `evidence`.
* 1-liner: “Confidence = {{ high/med/low }} because {{ reason }}”.

**Why this fits:** 
* Same pattern as Lab 1: Extract first, analyze second
* Automates the slowest part (original source + correct snippet wording)
* Forces evidence + placeholders where uncertain
* Reduces token usage by 99% vs. sending full file

**Key Connection:** This is the same hybrid approach from Lab 1, applied to copyright attribution.

---

**35–50 — Mini-Lab B: "Is it AI?" PR gate + evidence check (15 min)**

**Task 1 — PR Gate (GitHub)**
Add a visible AI usage switch.

```yaml
# .github/workflows/ai-gate.yml
name: AI Gate
on:
  pull_request:
    types: [opened, synchronize, labeled]
jobs:
  ai_gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions-ecosystem/action-get-labeled@v1
        id: labels
      - name: Require Security Approver if AI-assisted
        if: contains(steps.labels.outputs.labels, 'ai-assisted')
        run: |
          echo "AI-assisted PR: security approver required"
          echo "::error::Missing code owners approval from @{{ SECURITY_TEAM }}"
          exit 1
```

Add auto-label if author ticks a checkbox in PR template:

```md
<!-- .github/pull_request_template.md -->
- [ ] This change used AI assistance (Copilot/LLM/Slack bot)
```

**Task 2 — Evidence check (log triage output)**
Fail CI if AI triage lacks line-cited evidence.

```yaml
# .github/workflows/ai-evidence-check.yml
name: AI Evidence Check
on: workflow_run  # or tie to your CI job
jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate ai triage JSON
        run: |
          test -f .hybrid_out/hybrid_result.json
          python - <<'PY'
import json,sys
j=json.load(open('.hybrid_out/hybrid_result.json'))
ok = all(rc.get('evidence') and all('line' in e and 'snippet' in e for e in rc['evidence']) for rc in j.get('root_causes',[]))
sys.exit(0 if ok else 1)
PY
```

**Deliverables**

* `.github/pull_request_template.md`
* `.github/workflows/ai-gate.yml`
* `.github/workflows/ai-evidence-check.yml`

**Why this fits:** matches Comcast “is it AI?” gatekeeper, keeps audits, stops unevidenced outputs.

---

**50–57 — Threat Model Huddle (7 min)**
Fill quickly; assign owners.

| Where                  | How it appears          | Mitigation                                         | Owner       |            |
| ---------------------- | ----------------------- | -------------------------------------------------- | ----------- | ---------- |
| Build logs             | Crafted errors/comments | Strip ANSI/comments; limit context; denylist `curl | bash`, URLs | {{ NAME }} |
| PR titles/descriptions | Social prompts          | Exclude PR text from prompts; deterministic gates  | {{ NAME }}  |            |
| Slack bot              | Over-broad commands     | Whitelist; read-only by default; no code exec      | {{ NAME }}  |            |
| Dependencies           | Typosquats              | SBOM allow-list; signatures; pinning               | {{ NAME }}  |            |

---

**57–60 — Wrap (3 min)**

* **Key Takeaways:**
  * Same pattern: Tools → Extract → Prompt → Report (Lab 1 and Part 3)
  * Evidence required: All AI output must cite sources
  * Human review: Always required - AI assists, doesn't replace
  * Governance: "Is it AI?" gatekeeper process in place
* **Transition:** "Next, we'll see this pattern in action with GitHub PRs and Slack bots."

---

## What you’ll collect (reuse later)

* `compliance/ai_notice.json` (from Mini-Lab A)
* `.github/pull_request_template.md` + workflows (from Mini-Lab B)
* `threat_model.md` (board export)

---

## Guardrails (paste into a 1-pager)

**Technical**

* All AI-generated code: `-Werror -Wall -Wextra`, ASan/UBSan clean, CodeQL/Coverity clean.
* AI triage: must include `evidence[].line` + `snippet`; no execution of AI output.

**Process**

* PR checkbox + `ai-assisted` label → Security Approver required.
* Store `{prompt, model, timestamp, reviewer}` in artefacts (`.hybrid_out/meta.json`) and link in PR/Jira.

**Data/Model**

* Hosted models only for public/sanitised artefacts.
* Self-hosted (Ollama) for internal logs/customer data.

**Cost**

* Fail-only invocation; token cap per job; `AI_ENABLED={{ true|false }}` kill switch.

---

## Why this outline fits your context

* Hits **RDKM/CMF** pain directly (Black Duck attribution; log triage in CI; governance).
* Respects **senior, AI-new** audience: minimal moving parts, high leverage artefacts.
* Addresses **Alan’s** scepticism (cost, safety, lock-in) via hybrid+fail-only, explicit gates, and self-hosted where needed.
