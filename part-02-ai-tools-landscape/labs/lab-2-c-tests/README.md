# Lab 2: C/C++ Unit Test Generation

**Time:** 30 minutes  
**Goal:** Generate tests, then reject unsafe ones; keep only high-value, safe tests.

## Setup

```bash
# From repo root
cd part-02-ai-tools-landscape/labs/lab-2-c-tests

# Example library structure:
# include/string_utils.h
# src/string_utils.c
# tests/ (Catch2 or GoogleTest)

# Build the project
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug
cmake --build build -j

# Verify build
ls build/
```

## Exercise 2.4: Manual Baseline (5 minutes)

**Task:** Write one golden-path test manually.

### Example Function

```c
// include/string_utils.h
#ifndef STRING_UTILS_H
#define STRING_UTILS_H

#include <stddef.h>

/**
 * Safely calculate string length with maximum bound
 * @param str: String to measure
 * @param max_len: Maximum length to check
 * @return: Length of string (up to max_len), or -1 if str is NULL
 */
int safe_strlen(const char* str, size_t max_len);

/**
 * Safely copy string with size check
 * @param dest: Destination buffer
 * @param src: Source string
 * @param dest_size: Size of destination buffer
 * @return: 0 on success, -1 on error
 */
int safe_strcpy(char* dest, const char* src, size_t dest_size);

#endif // STRING_UTILS_H
```

### Test Framework: Catch2

```cpp
// tests/test_string_utils.cpp
#include <catch2/catch.hpp>
#include "string_utils.h"

TEST_CASE("safe_strlen - normal string") {
    const char* str = "hello";
    REQUIRE(safe_strlen(str, 10) == 5);
}
```

### RDK Context

**For RDK context:** Use a function from github.com/rdkcentral/telemetry or similar RDK component.

**Question:** How do you currently write tests for RDK components?

## Exercise 2.5: AI Test Generation (15 minutes)

**Task:** Use an LLM to propose additional edge tests.

### Prompt Template

```
Generate unit tests for this C function:

Function signature:
[paste from header file]

Function implementation:
[paste from source file]

Requirements:
1. Test golden path (normal operation)
2. Test edge cases:
   - NULL inputs
   - Empty strings
   - Boundary conditions (max_len, buffer size)
   - Invalid inputs
3. Test error conditions:
   - Buffer overflows
   - Invalid parameters
4. Use Catch2/GoogleTest framework
5. Complete, compilable test cases

IMPORTANT:
- Do NOT suggest tests that assert undefined behavior
- Do NOT test implementation details, only public API
- Do NOT test non-deterministic behavior
- All tests must be safe and deterministic

Output format:
- Test name: [descriptive]
- Test code: [complete test case]
- What it tests: [one sentence]
```

### Generate Tests

1. **Paste function code** into your LLM tool (GitHub Copilot, ChatGPT, Claude, Ollama)
2. **Use the prompt template** above
3. **Save AI-generated tests** to `tests/ai_proposals/` directory
4. **Do NOT run yet** - review first!

### Example AI Output

```cpp
// tests/ai_proposals/test_safe_strlen_edges.cpp
#include <catch2/catch.hpp>
#include "string_utils.h"

TEST_CASE("safe_strlen - NULL input") {
    REQUIRE(safe_strlen(NULL, 10) == -1);
}

TEST_CASE("safe_strlen - empty string") {
    REQUIRE(safe_strlen("", 10) == 0);
}

TEST_CASE("safe_strlen - string at max_len") {
    const char* str = "1234567890";  // 10 chars
    REQUIRE(safe_strlen(str, 10) == 10);
}

TEST_CASE("safe_strlen - string exceeds max_len") {
    const char* str = "12345678901";  // 11 chars
    REQUIRE(safe_strlen(str, 10) == 10);  // Should cap at max_len
}
```

## Exercise 2.6: Safety Review (10 minutes)

**Task:** Review each AI-generated test and create an acceptance checklist.

### Review Checklist

For each AI-generated test, check:

- [ ] **No undefined behavior** (NULL dereference, signed overflow, uninitialized memory)
- [ ] **Tests public API only** (no private state, no `#define` poking)
- [ ] **Clear assertions** (not just execution, actually tests something)
- [ ] **Deterministic** (same input = same output, no randomness)
- [ ] **Compiles with strict warnings** (`-Wall -Wextra -Werror`)
- [ ] **Sensible resource handling** (no leaks, proper cleanup)

### Reject Any Test That:

- Asserts undefined behavior
- Accesses private implementation details
- Lacks proper error handling
- Tests non-deterministic behavior
- Triggers compiler warnings

### Organize Tests

1. **Move accepted tests** to `tests/accepted/`
2. **Keep rejected tests** in `tests/ai_proposals/` with notes
3. **Add rejection notes** for each rejected test:

```
// REJECTED: test_safe_strlen_overflow.cpp
// Reason: Asserts undefined behavior (signed overflow)
// AI suggested: REQUIRE(safe_strlen(str, SIZE_MAX) == SIZE_MAX)
// Problem: SIZE_MAX may cause signed overflow
```

### Run Accepted Tests (Optional - if time permits)

```bash
# Build with coverage
cmake -S . -B build -DENABLE_COVERAGE=ON
cmake --build build -j

# Run tests
CTEST_OUTPUT_ON_FAILURE=1 cmake --build build --target test

# Generate coverage report
lcov --capture --directory build --output-file coverage.info
genhtml coverage.info --output-directory coverage_html

# View coverage
open coverage_html/index.html  # or xdg-open on Linux
```

## Deliverables

Submit:

1. **1 manual test** (`tests/test_string_utils.cpp`)
2. **Accepted AI tests** (`tests/accepted/*.cpp`)
3. **Rejection notes** for each rejected test
4. **Coverage report** (if time permits)

## Debrief Questions

Be ready to discuss:

1. **Unsafe suggestions:** Did the AI propose any tests with undefined behavior?
2. **Coverage gain:** How much additional coverage did AI tests provide?
3. **Quality:** Were AI-generated tests maintainable?
4. **Acceptance checklist:** What would you add to your checklist?
5. **For RDK context:** How would you use AI test generation for github.com/rdkcentral components?

## RDK Context

**For RDK context:** Generate tests for RDK component code from github.com/rdkcentral.

**Test frameworks commonly used in RDK:**
- Catch2
- GoogleTest
- CMake test framework

**RDK testing practices:**
- Always run with sanitizers (ASan, UBSan)
- Compile with `-Werror -Wall -Wextra`
- Test public API only
- No undefined behavior allowed

