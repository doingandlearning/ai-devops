# Hybrid Approach: Deterministic Filtering + LLM Analysis

## Overview

This approach combines the best of both worlds:
1. **Deterministic filtering** - Use Python/grep to find relevant error lines with context
2. **LLM analysis** - Send only filtered sections to LLM for intelligent analysis
3. **Cost efficiency** - Reduces token usage by 70-90% compared to sending entire log

## Why This Approach?

### Benefits

✅ **Cost savings** - Only send relevant error sections, not entire log  
✅ **Faster processing** - Less data to analyze  
✅ **Better focus** - LLM analyzes actual errors, not noise  
✅ **More accurate** - Context around errors helps LLM understand better  
✅ **Auditable** - Deterministic filtering is reproducible  

### When to Use

- **Large logs** (>1000 lines) - Too expensive to send entire log
- **Cost-sensitive** - Need to minimize token usage
- **High volume** - Many builds to analyze
- **Mixed approach** - Want deterministic + AI benefits

## How It Works

### Step 1: Deterministic Filtering
```python
# Find error lines with context
errors = find_error_lines_with_context(lines, context_lines=5)
```

Extracts:
- Error lines (compilation errors, linker errors, etc.)
- Context before (5 lines) - shows what led to error
- Context after (5 lines) - shows error consequences
- Line numbers for reference

### Step 2: Categorization
```python
# Categorize errors by type
categories = categorize_errors(errors)
```

Groups into:
- Compilation errors
- Linker errors (missing libraries)
- Linker errors (undefined references)
- Other errors

### Step 3: Create Focused Prompt
```python
# Create prompt with only relevant sections
prompt = create_focused_prompt(errors, build_info)
```

Includes:
- Build metadata (component, build ID, compiler)
- Only error sections with context
- Focused instructions for LLM

### Step 4: LLM Analysis
```python
# Send filtered data to LLM
response = call_llm_with_filtered_data(prompt, backend='ollama')
```

LLM analyzes:
- Only relevant error sections
- With surrounding context
- More focused and accurate

## Example: Token Savings

**Full log approach:**
- Log size: 5000 lines
- Estimated tokens: ~12,500 tokens
- Cost (GPT-4): ~$0.38 per analysis

**Hybrid approach:**
- Filtered sections: 10 error sections × 10 lines = 100 lines
- Estimated tokens: ~1,250 tokens
- Cost (GPT-4): ~$0.04 per analysis
- **Savings: ~90%**

## Usage

```bash
# Run hybrid approach
python3 04_hybrid_approach.py

# Or specify backend
python3 04_hybrid_approach.py --backend ollama --model codellama:7b
python3 04_hybrid_approach.py --backend openai --model gpt-4o
```

## Output Format

The script outputs:
1. **Filtering summary** - How many errors found, categorized
2. **Token savings** - Estimated cost reduction
3. **LLM analysis** - Root causes with evidence, confidence, actions
4. **Summary** - Ready for PR/Slack

## Comparison with Other Approaches

| Approach | Speed | Cost | Accuracy | Auditability |
|----------|-------|------|----------|-------------|
| **Grep/Awk** | ⚡⚡⚡ Fast | 💰 Free | ⚠️ Low (pattern only) | ✅✅✅ High |
| **Python** | ⚡⚡ Fast | 💰 Free | ⚠️ Medium (structured) | ✅✅✅ High |
| **LLM (full log)** | ⚡ Slow | 💰💰💰 Expensive | ✅✅✅ High | ⚠️ Low |
| **Hybrid** | ⚡⚡ Medium | 💰💰 Moderate | ✅✅✅ High | ✅✅ Medium |

## Best Practices

1. **Context size** - Use 3-5 lines of context (balance between info and cost)
2. **Error filtering** - Be selective - only include actual errors, not warnings
3. **Categorization** - Group similar errors to reduce redundancy
4. **Build info** - Include build metadata for better context
5. **Token limits** - If filtered data is still large, further reduce context

## When NOT to Use

❌ **Small logs** (<100 lines) - Overhead not worth it  
❌ **Simple errors** - Grep/Python sufficient  
❌ **Real-time analysis** - Deterministic faster  
❌ **Offline only** - Need LLM API access  

## Integration with CI/CD

```python
# Example: Use in Jenkins pipeline
def analyze_build_failure(log_file):
    # Step 1: Filter errors
    errors = find_error_lines_with_context(log_file)
    
    # Step 2: If too many errors, prioritize
    if len(errors) > 20:
        errors = prioritize_errors(errors)  # Keep top 10
    
    # Step 3: Send to LLM
    analysis = call_llm_with_filtered_data(errors)
    
    # Step 4: Post to Slack/PR
    post_to_slack(analysis['summary'])
```

## Cost Optimization Tips

1. **Batch similar errors** - Group related errors together
2. **Limit context** - Use 3 lines instead of 5 if cost is concern
3. **Use cheaper models** - GPT-3.5-turbo or Ollama for routine analysis
4. **Cache results** - Same error pattern = reuse analysis
5. **Set token limits** - Cap maximum tokens per analysis

