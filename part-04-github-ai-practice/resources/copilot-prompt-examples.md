# Copilot Chat Prompt Examples
# Examples for Part 4 Demo - Effective Prompting

## Infrastructure Code Prompts

### GitHub Actions Workflow

**Good Prompt:**
```
Create a GitHub Actions workflow for a C/C++ project using CMake. 
Requirements:
- Build with GCC and Clang
- Run tests with CTest
- Generate coverage with lcov
- Upload coverage to Codecov
- Only run on PRs and main branch
- Cache CMake build artifacts
- Run CodeQL security analysis
```

**Bad Prompt:**
```
Create a CI workflow
```

**Why Good:**
- Specific requirements (languages, tools, versions)
- Includes context (CMake, C/C++ project)
- Requests specific features (caching, CodeQL)

### Shell Script Generation

**Good Prompt:**
```
Create a bash script that:
- Clones a C dependency from GitHub
- Builds it with CMake using Release mode
- Installs to ${HOME}/local
- Sets up environment variables (PATH, LD_LIBRARY_PATH)
- Includes error handling and colored output
- Works on Ubuntu 20.04+
```

**Bad Prompt:**
```
Write a build script
```

**Why Good:**
- Specific requirements (CMake, Release mode)
- Includes constraints (Ubuntu version)
- Requests features (error handling, colors)

### Dockerfile Generation

**Good Prompt:**
```
Create a Dockerfile for a C/C++ build environment:
- Base: Ubuntu 22.04
- Install: GCC, Clang, CMake, build-essential
- Install: CTest, lcov, cppcheck
- Set up non-root user for builds
- Optimize for layer caching
- Include healthcheck
```

**Bad Prompt:**
```
Make a Dockerfile
```

## Code Explanation Prompts

### Explain Function

**Good Prompt:**
```
@workspace Explain this function:
- What does it do?
- What are the inputs/outputs?
- Are there any edge cases or potential issues?
- How does it relate to the rest of the codebase?

[PASTE FUNCTION CODE]
```

**Bad Prompt:**
```
What does this do?
```

### Explain Error

**Good Prompt:**
```
Explain this CMake configuration error:
- What caused it?
- How to fix it?
- How to prevent it in the future?

Error:
[PASTE ERROR MESSAGE]
```

**Bad Prompt:**
```
Fix this error
```

## Code Review Prompts

### Security Review

**Good Prompt:**
```
Review this code for security issues:
- Buffer overflows
- Memory leaks
- Unsafe function usage (strcpy, sprintf)
- Input validation
- Error handling

[PASTE CODE]
```

**Bad Prompt:**
```
Is this secure?
```

### Performance Review

**Good Prompt:**
```
Analyze this code for performance issues:
- Time complexity
- Memory usage
- Potential bottlenecks
- Optimization opportunities

[PASTE CODE]
```

## Log Analysis Prompts

### Build Failure Analysis

**Good Prompt:**
```
Analyze this CI build log and identify:
1. Primary error that caused the build to fail
2. Secondary errors (if any)
3. Root cause analysis
4. Specific fix steps (file names, line numbers)
5. Prevention strategies

Build log:
[PASTE LOG CONTENT]
```

**Bad Prompt:**
```
Why did this fail?
```

### Test Failure Analysis

**Good Prompt:**
```
Analyze this test failure:
- Which test failed?
- Why did it fail?
- Is it a flaky test or a real bug?
- How to reproduce?
- Suggested fix

Test output:
[PASTE TEST OUTPUT]
```

## Best Practices

### 1. Be Specific
- ✅ "Create a GitHub Actions workflow for C/C++ with CMake"
- ❌ "Create a CI workflow"

### 2. Include Context
- ✅ "For a C/C++ project using CMake on Ubuntu 22.04"
- ❌ "For a project"

### 3. Request Explanations
- ✅ "Explain why you chose this approach"
- ❌ Just accept the code

### 4. Iterate and Refine
- ✅ Generate → Review → Ask follow-up → Refine
- ❌ Accept first suggestion blindly

### 5. Use @workspace for Repository Context
- ✅ "@workspace How does this function work?"
- ❌ "How does this function work?" (without @workspace)

### 6. Request Structured Output
- ✅ "Format as JSON with fields: error, cause, fix"
- ❌ "Tell me about this error"

### 7. Include Constraints
- ✅ "Must work on Ubuntu 20.04+, use CMake 3.16+"
- ❌ "Make it work"

### 8. Ask for Alternatives
- ✅ "Show me 3 different approaches and trade-offs"
- ❌ "Do this"

## Common Patterns

### Pattern 1: Generate → Review → Refine
```
1. Generate initial code
2. Review what was generated
3. Ask: "Add error handling"
4. Ask: "Optimize for performance"
5. Final review
```

### Pattern 2: Explain → Modify → Verify
```
1. Explain existing code
2. Request modification
3. Verify changes are correct
```

### Pattern 3: Compare → Choose → Implement
```
1. Show multiple approaches
2. Compare trade-offs
3. Choose best approach
4. Implement
```

## RDK-Specific Examples

### CMake Configuration
```
Create a CMake configuration for an RDK component:
- Component name: telemetry
- Dependencies: json-c, libcurl
- Install to: /usr/local/rdk
- Include RDK standard headers
- Support both GCC and Clang
- Enable coverage in Debug mode
```

### Black Duck Compliance
```
Generate a NOTICE file entry for this code:
- Source: Adapted from iw (wireless tools)
- License: ISC
- Copyright: Use placeholders {{ YEAR }}, {{ COPYRIGHT HOLDER }}
- Format: RDK standard two-liner
- Include evidence (file path, line numbers)

[PASTE CODE SNIPPET]
```

### Build Script for RDK
```
Create a build script for RDK component:
- Clone from github.com/rdkcentral
- Build with Yocto build system
- Install to RDK image
- Set up environment for RDK development
- Include error handling for network issues
```

