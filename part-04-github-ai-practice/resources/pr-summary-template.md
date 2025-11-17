# PR Summary Template
# Generated with Copilot Chat - Example for Part 4 Demo
#
# Use this template with Copilot Chat to generate PR summaries
# Format: Suitable for Slack/Teams/Email

## Prompt Template for Copilot Chat

```
@workspace Summarize this PR for a technical manager:

PR: [PR number/link]
Jira ticket: [ticket key]

Include:
- What changed (technical summary)
- Why (business context from Jira if available)
- Risks or testing required
- Deployment considerations

Format as a Slack message (concise, bullet points).
```

## Example Output Format

```
🔀 PR Summary: [PR Title] (#[PR Number])

📋 What Changed:
• [Technical change 1]
• [Technical change 2]
• [Technical change 3]

💼 Why Changed:
• [Business context from Jira ticket]
• [Related issue/requirement]

⚠️ Risks & Testing:
• [Risk 1] - [Mitigation]
• [Risk 2] - [Testing needed]
• [Risk 3] - [Review required]

🚀 Deployment:
• [Deployment step 1]
• [Deployment step 2]
• [Rollback plan if needed]

🔗 Links:
• PR: [PR link]
• Jira: [Jira ticket link]
• Related PRs: [Links if any]
```

## Example: Real PR Summary

```
🔀 PR Summary: Fix memory leak in telemetry collector (#123)

📋 What Changed:
• Fixed memory leak in telemetry_config_load() function
• Added proper cleanup in error paths
• Updated unit tests to verify memory cleanup

💼 Why Changed:
• Jira BD-1290: Memory leak causing crashes in production
• Customer reported crashes after 24 hours of uptime
• Priority: P1 - Production issue

⚠️ Risks & Testing:
• Memory leak fix - Requires testing with valgrind/ASAN
• Error path changes - Test all error scenarios
• Unit tests updated - Verify coverage

🚀 Deployment:
• Deploy to staging first
• Monitor memory usage for 48 hours
• Rollback plan: Revert to previous version if issues

🔗 Links:
• PR: https://github.com/rdkcentral/telemetry/pull/123
• Jira: BD-1290
• Related PRs: #120 (initial fix attempt)
```

## Customization for Your Team

### For RDK/CMF Context:
- Include component name (telemetry, hal, etc.)
- Reference BD tickets (Black Duck compliance)
- Mention Apache license compliance if relevant
- Include build/test status

### For Slack Format:
- Use emojis for visual scanning
- Keep each section concise (2-3 bullets max)
- Include action items if needed
- Tag relevant team members

### For Email Format:
- More formal language
- Include full context
- Add executive summary at top
- Include metrics/impact if available

## Copilot Chat Variations

### For Non-Technical Stakeholders:
```
Summarize this PR for a non-technical manager:
- Focus on business impact
- Avoid technical jargon
- Include timeline/deadline
- Format as email
```

### For Security Review:
```
Summarize this PR for security review:
- Highlight security-related changes
- Identify potential vulnerabilities
- Suggest security testing needed
- Format as checklist
```

### For Release Notes:
```
Generate release notes for this PR:
- User-facing changes only
- Breaking changes highlighted
- Migration steps if needed
- Format as markdown
```

