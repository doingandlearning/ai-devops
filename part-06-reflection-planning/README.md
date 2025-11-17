# Part 6: Reflection & Planning

**Duration:** 45 minutes (16:00-16:45)  
**Format:** Workshop + Discussion

## Learning Objectives

By the end of this section, participants will:
- Identify key takeaways and opportunities for their environment
- Create a roadmap for responsible AI adoption in DevSecOps
- Understand resources for experimenting with different LLMs
- Make informed decisions about local vs. hosted, general-purpose vs. code-specialized models
- Address governance and cost concerns

## Key Topics

- Key takeaways and identified opportunities for your environment
- Roadmap for responsible AI adoption in DevSecOps
- Resources and recommendations for experimenting with different LLMs (local vs. hosted, general-purpose vs. code-specialized)

## Workshop: Key Takeaways (15 minutes)

### Exercise 6.1: Individual Reflection (5 minutes)

**Task:** Each participant fills out a simple form.

**Form:**
```
1. **One thing I learned today that surprised me:**
   [Write your answer]

2. **One use case I want to try immediately:**
   [Write your answer]

3. **One concern I still have:**
   [Write your answer]

4. **One thing I'll avoid:**
   [Write your answer]
```

### Exercise 6.2: Share-Back (10 minutes)

**Format:** Round-robin sharing (2-3 minutes per person)

**Prompt for each participant:**
- Share your "surprising learning" and "immediate use case"
- Others can ask questions or offer suggestions

**Facilitator notes:**
- Document common themes (write on whiteboard/flipchart)
- Note concerns that multiple people share
- Identify opportunities mentioned by the group

**Common themes to look for:**
- Cost concerns
- Security/governance questions
- Specific tools they want to try
- Integration challenges

## Workshop: Adoption Planning (20 minutes)

### Exercise 6.3: Three-Tier Adoption Plan (10 minutes)

**Task:** Each participant creates a simple adoption plan.

**Format:**
```
**Adopt Now** (this week):
- [One thing they'll try immediately]
- [Tool/resource needed]
- [Success criteria]

**Pilot** (next month):
- [One thing to test/pilot]
- [What needs to be set up]
- [How to measure success]
- [Risk mitigation]

**Avoid/Defer**:
- [One thing they'll avoid or defer]
- [Reason why]
```

### Exercise 6.4: Group Pilot Candidates (10 minutes)

**Task:** As a group, identify 2-3 pilot projects to start together.

**Discussion prompts:**
1. **What use case would benefit the whole team?**
   - PR summaries? Log triage? Component health analysis?

2. **What's the lowest-risk pilot?**
   - Start with non-critical path
   - Clear success metrics
   - Easy to roll back

3. **What resources do we need?**
   - Tools (GitHub Copilot? Ollama? Other?)
   - Budget approval?
   - Policy approval?

**Deliverable:** List of 2-3 pilot candidates with:
- Use case description
- Success criteria
- Timeline
- Resources needed
- Owner/lead

**Example from review.md:**
- PR summaries (low risk, high value)
- Log triage (saves time, easy to measure)
- SBOM assist (complements existing tools)

## Discussion: Roadmap for Responsible AI Adoption

### Phase 1: Foundation (Weeks 1-4)

**Goals:**
- Set up basic tooling
- Establish governance policies
- Run first pilot

**Activities:**
1. **Tool selection:**
   - Evaluate GitHub Copilot (Teams vs. Enterprise)
   - Set up Ollama for local experiments (if needed)
   - Choose model tiers (local vs. hosted)

2. **Policy creation:**
   - Draft AI usage policy (one-pager)
   - Define "is it AI or not?" gatekeeper process
   - Establish logging requirements

3. **First pilot:**
   - Choose lowest-risk use case
   - Set success metrics
   - Start small (one team member, one use case)

**Deliverables:**
- Approved AI usage policy
- Tool setup (Copilot or Ollama)
- First pilot results (what worked, what didn't)

### Phase 2: Expansion (Months 2-3)

**Goals:**
- Expand successful pilots to more team members
- Add more use cases
- Refine policies based on learnings

**Activities:**
1. **Expand pilots:**
   - If PR summaries work, expand to whole team
   - If log triage works, integrate into CI/CD
   - Measure impact (time saved, quality improvements)

2. **Refine governance:**
   - Update policies based on real-world experience
   - Adjust cost controls (if needed)
   - Refine review processes

3. **Knowledge sharing:**
   - Document successful patterns
   - Share lessons learned
   - Train additional team members

**Deliverables:**
- Expanded pilot results
- Updated policies
- Internal documentation/training materials

### Phase 3: Integration (Months 4-6)

**Goals:**
- Integrate AI into regular workflows
- Scale successful patterns
- Measure long-term impact

**Activities:**
1. **Workflow integration:**
   - Integrate AI into CI/CD pipelines (where appropriate)
   - Automate reporting (weekly summaries)
   - Build reusable scripts/templates

2. **Cost optimization:**
   - Track costs over time
   - Optimize model selection (use cheaper models where possible)
   - Justify costs with value metrics

3. **Continuous improvement:**
   - Collect feedback from team
   - Refine prompts and workflows
   - Share successes with broader organization

**Deliverables:**
- Integrated workflows
- Cost-benefit analysis
- Success stories/metrics

## Resources & Recommendations

### Local vs. Hosted Models

**When to use local (Ollama, GPT4All):**
- ✅ Sensitive data (can't send to external APIs)
- ✅ Cost control (no per-token charges)
- ✅ Offline/air-gapped environments
- ✅ High-volume usage (once set up, only infrastructure costs)
- ⚠️ Requires local GPU/resource
- ⚠️ Smaller models (may be less capable)

**When to use hosted APIs:**
- ✅ More capable models (GPT-4, Claude)
- ✅ No infrastructure setup
- ✅ Always up-to-date models
- ✅ Easy to scale
- ⚠️ Data privacy concerns
- ⚠️ Per-token costs add up
- ⚠️ Internet dependency

**Recommendation for Comcast/Sky:**
- **Start with hosted** for low-risk use cases (PR summaries, documentation)
- **Use local (Ollama)** for sensitive logs, internal analysis
- **Hybrid approach:** Hosted for general tasks, local for sensitive data

### General-Purpose vs. Code-Specialized Models

**General-purpose models (GPT-4, Claude, Llama):**
- ✅ Understand context across domains
- ✅ Good for summaries, explanations, documentation
- ✅ Flexible (can handle various tasks)
- ⚠️ May not be optimized for code

**Code-specialized models (Code Llama, StarCoder, WizardCoder):**
- ✅ Optimized for code generation
- ✅ Better at understanding code structure
- ✅ Often open-source (can self-host)
- ⚠️ May struggle with non-code tasks

**Recommendation:**
- **Use code-specialized** for: Code generation, test generation, code review
- **Use general-purpose** for: Log analysis, summaries, documentation, explanations

**Try both and compare:**
- Same task with both models
- Compare quality and cost
- Choose based on your needs

### Specific Tool Recommendations

**Getting started:**
1. **GitHub Copilot Chat** (if GitHub available)
   - Easiest to start
   - Integrated with workflow
   - Good for PR summaries, code explanations

2. **Ollama** (free, local)
   - Set up locally
   - Try: `llama3:instruct`, `codellama`
   - Good for: Sensitive data, cost control

3. **Anthropic Claude** (hosted API)
   - Strong for: Summaries, analysis, explanations
   - Good safety/guardrails

**For advanced use:**
- **Sourcegraph Cody** (if using Sourcegraph)
- **Tabnine** (if need privacy-focused commercial option)
- **Custom scripts** with OpenAI/Anthropic APIs

### Learning Resources

**Documentation:**
- GitHub Copilot documentation
- Ollama documentation
- Prompt engineering guides

**Communities:**
- GitHub Discussions (Copilot)
- Reddit (r/LocalLLaMA for self-hosting)
- Stack Overflow (tag: prompt-engineering)

**Practice:**
- Start with non-critical tasks
- Experiment with different prompts
- Compare outputs (AI vs. manual vs. automation)

## Governance: One-Pager Policy Template

### AI Usage Policy Draft

**Based on discussion and callnotes, here's a template:**

```
AI USAGE POLICY - DevSecOps Team

**Approved Tools:**
- GitHub Copilot (Teams/Enterprise) [specify plan]
- Ollama (local models) [specify models]
- [Other tools as approved]

**Use Cases - Approved:**
✅ PR summaries (with human review)
✅ Log analysis (non-sensitive logs)
✅ Documentation generation (with human review)
✅ Test case generation (with human review)
✅ Code explanations

**Use Cases - Prohibited:**
❌ Security decisions (always human review)
❌ License compliance decisions (always human review)
❌ Sensitive data analysis (use local models only)
❌ Auto-merge of AI-generated code (human review required)

**Gatekeeper Process ("Is it AI or not?"):**
1. Is this sensitive data? → Use local model or redact
2. Is this a security/license decision? → Human review required
3. Is this a code change? → Human review + tests + static analysis required
4. Document AI usage: Log prompt + output, link to PR/ticket

**Cost Controls:**
- Monthly budget: $[amount]
- Alert threshold: 80% of budget
- Model tiers: [specify which models for which use cases]

**Review & Logging:**
- All AI-generated code: Human review required
- Log all prompts/outputs: Attach to PRs, link to tickets
- Weekly cost report: Track spend per use case

**Responsible Party:**
- Policy owner: [name]
- Review frequency: [monthly/quarterly]
- Last updated: [date]
```

**Exercise 6.5:** As a group, customize this template for your team (10 minutes)

## Discussion Questions

### For Roadmap Planning

1. **Priorities:**
   - What's your biggest pain point that AI could address?
   - What would have the highest impact?

2. **Risk tolerance:**
   - What's your comfort level with AI-generated code?
   - What safeguards do you need before starting?

3. **Resources:**
   - What budget is available?
   - What tools do you already have access to?
   - What infrastructure is available (for local models)?

4. **Timeline:**
   - What's realistic for your team?
   - Are there deadlines or milestones to work towards?

### For Tool Selection

1. **GitHub Copilot:**
   - Teams vs. Enterprise: What's your decision?
   - How will you handle the "gatekeeper" requirement?

2. **Local vs. hosted:**
   - Do you have infrastructure for local models?
   - What data sensitivity requirements do you have?

3. **Model selection:**
   - Which use cases need the best models?
   - Which can use cheaper/smaller models?

## Wrap-Up & Next Steps (15 minutes)

### Exercise 6.6: Commitments (5 minutes)

**Each participant commits to:**
- **This week:** [One action]
- **This month:** [One pilot]
- **This quarter:** [One goal]

**Write it down:** Participants write commitments (for accountability)

### Exercise 6.7: Group Agreements (5 minutes)

**As a team, agree on:**
- **Pilot project:** What will you pilot together?
- **Timeline:** When will you start? When will you review?
- **Success metrics:** How will you know it's working?
- **Communication:** How will you share learnings?

### Resources Handout (5 minutes)

**Provide:**
- Links to documentation
- Prompt templates (from labs)
- Policy template (customized)
- Contact information for follow-up questions

**Final Q&A:**
- Open floor for questions
- Address any remaining concerns
- Provide contact information for follow-up

## Key Takeaways Summary

### What We Covered Today

1. **AI is a tool, not a replacement:**
   - Use AI to assist, not automate critical decisions
   - Always apply human review for security, licenses, code changes

2. **Start small, measure, iterate:**
   - Begin with low-risk pilots
   - Measure impact (time saved, quality)
   - Expand successful pilots gradually

3. **Governance is critical:**
   - Define policies (what's allowed, what's not)
   - Implement "gatekeeper" process
   - Log and audit AI usage

4. **Cost awareness:**
   - Track token usage and costs
   - Use cheaper models where possible
   - Justify costs with value metrics

5. **C/C++ considerations:**
   - AI can help, but be extra cautious (UB, memory safety)
   - Always use static analysis (CodeQL, Coverity)
   - Never trust AI suggestions blindly

### What to Do Next

**Immediate (this week):**
- Review today's materials
- Set up one tool (Copilot or Ollama)
- Try one use case (PR summary or log analysis)

**Short-term (this month):**
- Run first pilot
- Draft AI usage policy
- Start tracking costs

**Long-term (this quarter):**
- Integrate successful patterns into workflows
- Share learnings with broader team
- Refine policies based on experience

## Final Notes

**Remember:**
- AI is powerful but has limitations
- Human judgment is always required for critical decisions
- Start with small experiments, learn, and scale
- Governance and cost control are essential

**Contact:**
- [Your contact information]
- [Follow-up session if planned]
- [Resources/documentation links]

**Thank you for participating!**

