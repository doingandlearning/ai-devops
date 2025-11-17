# Lab 3: AI Automation with Jenkins

**Time:** 30 minutes (can complete as homework if time is tight)  
**Addresses your pain point #2: Running AI as automated task with Jenkins**

**Goal:** Run hybrid analysis automatically **only on failures**, post summary, cap cost.

## Setup

```bash
# From repo root
cd part-02-ai-tools-landscape/labs/lab-3-jenkins

# Ensure you have access to:
# - Jenkins instance (or local Jenkins)
# - Hybrid approach script: ../../../../resources/lab-1-solutions/04_hybrid_approach.py
# - Build log location (or use sample build.log)
```

## Pipeline Skeleton (Declarative)

Create a `Jenkinsfile` with the following structure:

```groovy
pipeline {
  agent any

  environment {
    // API key from Jenkins credentials
    OPENAI_API_KEY = credentials('openai-api-key')
    // OR use Ollama (local)
    // OLLAMA_URL = 'http://localhost:11434'
    
    // Kill switch for AI
    AI_ENABLED = "${params.AI_ENABLED ?: 'true'}"
    
    // Cost control
    MAX_TOKENS = "${params.MAX_TOKENS ?: '1000'}"
  }

  options { 
    skipDefaultCheckout(true)
    // Archive artifacts for audit
    archiveArtifacts artifacts: '**/.hybrid_out/**', fingerprint: true
  }

  stages {
    stage('Checkout') {
      steps { 
        checkout scm 
      }
    }

    stage('Build') {
      steps { 
        sh '''
          cmake -S . -B build
          cmake --build build -j
        '''
      }
    }

    stage('Test') {
      steps { 
        sh 'ctest --test-dir build || true'  // Allow failure for post{} to trigger
      }
    }
  }

  post {
    failure {
      script {
        // Only run AI on failures (cost control)
        if (env.AI_ENABLED != 'true') { 
          echo 'AI disabled - skipping analysis'
          return 
        }
        
        echo 'Build failed - running AI log analysis...'
        
        // Run hybrid approach
        sh '''
          cd ${WORKSPACE}
          python3 -m venv .venv || true
          source .venv/bin/activate || true
          pip install -q -r requirements.txt || true
          
          # Run hybrid analysis
          python3 resources/lab-1-solutions/04_hybrid_approach.py \
            --log build.log \
            --outdir .hybrid_out \
            > hybrid_run.txt 2>&1 || true
        '''
        
        // Parse results
        def result = [:]
        try {
          result = readJSON file: '.hybrid_out/hybrid_result.json'
        } catch (Exception e) {
          echo "Warning: Could not parse AI results: ${e.message}"
          // Fallback to deterministic script
          sh '''
            python3 resources/lab-1-solutions/01_grep.sh > fallback_analysis.txt || true
          '''
          return
        }
        
        // Extract summary
        def bullets = result.summary ? result.summary.join('\n') : 'No summary available'
        
        // Post to Slack (if configured)
        try {
          slackSend(
            channel: '#rdk-builds',
            color: 'danger',
            message: """Build failed: ${env.BUILD_URL}
            
AI Triage:
${bullets}

Full analysis: ${env.BUILD_URL}artifact/.hybrid_out/hybrid_result.json"""
          )
        } catch (Exception e) {
          echo "Slack not configured: ${e.message}"
        }
        
        // Archive artifacts for audit
        archiveArtifacts artifacts: '.hybrid_out/*.json, hybrid_run.txt', fingerprint: true
        
        // Set build description
        currentBuild.description = "AI Analysis: ${result.root_causes?.size() ?: 0} root causes identified"
      }
    }
    
    always {
      // Archive build log for reference
      archiveArtifacts artifacts: 'build.log', allowEmptyArchive: true
    }
  }

  parameters {
    booleanParam(
      name: 'AI_ENABLED', 
      defaultValue: true, 
      description: 'Enable AI triage on failure'
    )
    stringParam(
      name: 'MAX_TOKENS',
      defaultValue: '1000',
      description: 'Maximum tokens per AI analysis (cost control)'
    )
  }
}
```

## Cost Guardrails

### 1. Fail-Only Execution

- **Only run AI on failures** via `post { failure { ... } }`
- Never run AI on successful builds
- Reduces cost by 80-90% (assuming 10-20% failure rate)

### 2. Hybrid Approach Only

- Use `04_hybrid_approach.py` (not full log approach)
- 70-90% cost savings vs. full log analysis
- Deterministic filtering first, then LLM

### 3. Token Budget

- Set `MAX_TOKENS` parameter (default: 1000)
- Script should respect token limit
- Fail gracefully if limit exceeded

### 4. Kill Switch

- `AI_ENABLED=false` parameter or environment variable
- Allows disabling AI without code changes
- Useful for debugging or cost emergencies

### 5. Audit Trail

- Archive `hybrid_result.json`, `meta.json`, and sections
- Store in Jenkins artifacts
- Track costs per build

## Exercise 2.8: Integrate into Your Pipeline (20 minutes)

**Task:** Adapt the pipeline skeleton to your Jenkins setup.

### Steps

1. **Adapt paths:**
   - Update `cd` path to match your job structure
   - Ensure `build.log` location matches your build output
   - Update script paths to point to `resources/lab-1-solutions/`

2. **Configure credentials:**
   - Add `openai-api-key` credential in Jenkins
   - OR configure `OLLAMA_URL` for local models

3. **Test locally (optional):**
   ```bash
   # Test hybrid script manually
   python3 resources/lab-1-solutions/04_hybrid_approach.py \
     --log build.log \
     --outdir .hybrid_out
   
   # Verify output
   cat .hybrid_out/hybrid_result.json
   ```

4. **Slack integration (if available):**
   - Configure Slack plugin in Jenkins
   - Update channel name (`#rdk-builds`)
   - Test with a manual build failure

5. **Fallback handling:**
   - If AI fails, use deterministic script (`01_grep.sh`)
   - Post link to raw log if no analysis available
   - Never block build pipeline on AI failure

### Deliverable

- Working `Jenkinsfile` with AI integration
- Test run showing AI analysis on failure
- Cost estimate per build failure

## Exercise 2.9: Cost & ROI Analysis (10 minutes)

**Task:** Calculate costs and ROI for automated AI in Jenkins.

### Fill in Your Numbers

| Metric | Value | Notes |
|--------|-------|-------|
| Avg builds/day | {{ PLACEHOLDER }} | |
| Avg failures/day | {{ PLACEHOLDER }} | (typically 10-20% failure rate) |
| Hybrid prompt chars (avg) | {{ PLACEHOLDER }} | (from hybrid output) |
| Estimated tokens saved vs full log | {{ PLACEHOLDER }} | (typically 70-90%) |
| Cost per failure (hybrid) | {{ PLACEHOLDER }} | (~$0.004-0.01 with GPT-4o) |
| Minutes saved per failure | {{ PLACEHOLDER }} | (typically 10-15 min) |
| Engineer cost/hour | {{ PLACEHOLDER }} | (your team's rate) |

### Calculate ROI

**Daily costs:**
- AI cost: `failures/day × cost_per_failure = {{ PLACEHOLDER }}`
- Example: `2 failures × $0.01 = $0.02/day`

**Daily savings:**
- Time saved: `failures/day × minutes_saved × (engineer_cost/60) = {{ PLACEHOLDER }}`
- Example: `2 failures × 15 min × ($50/hour / 60) = $25/day`

**ROI:**
- Daily ROI: `savings - costs = {{ PLACEHOLDER }}`
- Example: `$25 - $0.02 = $24.98/day`
- **ROI multiplier:** `savings / costs = {{ PLACEHOLDER }}x`
- Example: `$25 / $0.02 = 1,250x return`

**Monthly/Annual:**
- Monthly cost: `daily_cost × 30 = {{ PLACEHOLDER }}`
- Monthly savings: `daily_savings × 30 = {{ PLACEHOLDER }}`
- Annual cost: `monthly_cost × 12 = {{ PLACEHOLDER }}`
- Annual savings: `monthly_savings × 12 = {{ PLACEHOLDER }}`

### Scale Analysis

**What happens at scale?**

| Scenario | Builds/day | Failures/day | Daily Cost | Daily Savings | ROI |
|----------|-----------|--------------|------------|--------------|-----|
| Current | {{}} | {{}} | {{}} | {{}} | {{}} |
| 10x scale | {{}} | {{}} | {{}} | {{}} | {{}} |
| 100x scale | {{}} | {{}} | {{}} | {{}} | {{}} |

**Cost control at scale:**
- Set daily/monthly token budget
- Disable AI if budget exceeded
- Use cheaper models (GPT-3.5-turbo, Ollama) for routine analysis
- Reserve expensive models (GPT-4o) for critical failures

### Decision

**Ship now / Run as pilot / Not worth it** — {{ PLACEHOLDER }}

**Justification:** {{ PLACEHOLDER - 1-2 sentences }}

## Deliverables

Submit:

1. **`Jenkinsfile`** with AI integration
2. **Cost & ROI analysis** (filled table)
3. **Decision** (ship/pilot/not worth it) with justification
4. **Screenshot** of Jenkins build with AI analysis (if available)

## Debrief Questions

Be ready to discuss:

1. **Cost at scale:** What happens if 100 builds/day? 1000 builds/day?
2. **When to use:** Always? Only on failures? Only on certain error types?
3. **Fallback:** What if AI API is down? Use deterministic scripts
4. **For your pain point #2:** How would you implement this in your Jenkins setup?
5. **Governance:** How do you track AI usage? Log all AI calls?

## RDK Context

**For your RDK context:** Integrate this into your Jenkins setup for github.com/rdkcentral builds.

**RDK-specific considerations:**
- Build logs from RDK components (telemetry, etc.)
- Post to RDK Slack channels (`#rdk-builds`)
- Archive artifacts for compliance/audit
- Track costs for RDK management reporting

**Integration points:**
- Existing Jenkins pipelines
- RDK build infrastructure
- Slack notifications
- Cost tracking systems

