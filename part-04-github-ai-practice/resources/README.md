# Part 4 Resources

This directory contains example code and templates for Part 4: GitHub & AI in Practice.

## Files

### `github-actions-ci-cpp.yml`
Example GitHub Actions workflow for C/C++ projects.

**Features:**
- Builds with GCC and Clang
- Runs tests with CTest
- Generates coverage reports with lcov
- Uploads coverage to Codecov
- CodeQL security scanning
- Caching for build artifacts

**Usage:**
```bash
# Copy to your repository
cp github-actions-ci-cpp.yml .github/workflows/ci.yml

# Customize for your project
# - Update branch names
# - Adjust CMake flags
# - Add/remove steps as needed
```

**Demo Notes:**
- Show how Copilot Chat generated this
- Point out what's good (caching, multiple compilers)
- Show what might need adjustment (CodeQL setup, coverage paths)

### `build-dependency.sh`
Example shell script for building C dependencies.

**Features:**
- Clones dependency from GitHub
- Builds with CMake
- Installs to local directory
- Sets up environment variables
- Error handling and colored output

**Usage:**
```bash
# Make executable
chmod +x build-dependency.sh

# Run with default settings
./build-dependency.sh

# Or specify URL and install prefix
./build-dependency.sh https://github.com/example/lib.git ~/local
```

**Demo Notes:**
- Show how Copilot Chat generated this
- Point out security considerations (no hardcoded secrets)
- Show error handling (set -e, set -u)
- Demonstrate environment setup

### `pr-summary-template.md`
Template for generating PR summaries with Copilot Chat.

**Features:**
- Prompt templates for different audiences
- Example output formats
- Customization for RDK/CMF context
- Slack/Email/Release notes variations

**Usage:**
1. Copy prompt template
2. Fill in PR number and Jira ticket
3. Use with Copilot Chat
4. Customize output format

**Demo Notes:**
- Show how to use template with Copilot Chat
- Demonstrate different formats (Slack vs. Email)
- Connect to their workflow (Jira tickets, Slack updates)

### `copilot-prompt-examples.md`
Collection of effective Copilot Chat prompts.

**Sections:**
- Infrastructure code prompts
- Code explanation prompts
- Code review prompts
- Log analysis prompts
- Best practices
- RDK-specific examples

**Usage:**
- Reference during demos
- Share with participants
- Use as starting point for their own prompts

### `slackbot_demo.md`
Guide for demonstrating the Slackbot in Part 4.

**Sections:**
- What the Slackbot does (PR summaries, build failures)
- Connection to Lab 1 (hybrid approach)
- Demo setup and steps
- Code walkthrough
- Troubleshooting

**Usage:**
- Reference during Demo 4
- Show Lab 1 output in production
- Demonstrate automated vs. manual approaches

**Demo Notes:**
- Show good vs. bad prompts
- Demonstrate iterative refinement
- Connect to Part 2 argument (LLM wrappers)

## Demo Flow

### Demo 1: Infrastructure Code (15 min)
1. Show `github-actions-ci-cpp.yml` - "Copilot generated this"
2. Walk through what's good, what needs adjustment
3. Exercise: Generate `build-dependency.sh` with Copilot Chat
4. Review generated script

### Demo 2: PR Summaries (15 min)
1. Show `pr-summary-template.md` - "Template for PR summaries"
2. Use template with Copilot Chat on example PR
3. Exercise: Generate PR summary for their context
4. Show how to format for Slack/Jira

### Demo 3: Log Analysis (10 min)
1. Use `build.log` from Lab 1 (if available)
2. Show Copilot Chat analyzing log
3. Compare to Lab 1 hybrid approach
4. Exercise: Analyze different log types

## Key Connections

### Connection to Lab 1:
- Lab 1: Automated log analysis (DIY)
- Part 4: Manual log analysis (Copilot)
- **Same pattern:** Extract → Prompt → Structure

### Connection to Part 2:
- Part 2 argument: "Most AI tools are LLM wrappers"
- Copilot = LLM wrapper
- **You can build similar things**

### Connection to Part 3:
- Part 3: Evidence required
- Part 4: Always review Copilot output
- **Same principle:** Review everything

## Tips for Instructors

1. **Show both approaches:** Copilot (manual) vs. DIY (automated)
2. **Connect to Lab 1:** Same pattern, different context
3. **Emphasize review:** Always review Copilot output
4. **Use examples:** These resources are starting points
5. **Customize:** Adapt to their workflow (Jira, Slack, RDK context)

## Customization for RDK Context

### GitHub Actions:
- Update branch names (main, develop → RDK branches)
- Add RDK-specific build steps
- Include Black Duck scanning if needed

### Build Scripts:
- Add RDK environment setup
- Include Yocto build system support
- Set up RDK-specific paths

### PR Summaries:
- Include BD ticket references
- Format for RDK Slack channels
- Add component names (telemetry, hal, etc.)

## Troubleshooting

**Copilot not available?**
- Use screenshots from these examples
- Or use ChatGPT/Claude with same prompts
- Show the pattern, not the tool

**No GitHub access?**
- Use example PRs/logs from resources
- Focus on the pattern, not the platform
- Emphasize: "You can do this with any LLM"

**Time pressure?**
- Focus on Demo 1 (infrastructure code)
- Skip other demos if needed
- Emphasize: "Same pattern as Lab 1"

