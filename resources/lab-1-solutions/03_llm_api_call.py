#!/usr/bin/env python3
"""
LLM API call for build log analysis.
Demonstrates Approach 3: Using LLM to understand context and provide explanations.

Supports multiple backends:
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude)
- Ollama (local models)
"""

import json
import sys
from pathlib import Path

# Uncomment the backend you want to use:
# import openai
# from anthropic import Anthropic
# import requests  # For Ollama


def read_build_log(log_file='build.log'):
    """Read build log file."""
    try:
        with open(log_file, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: {log_file} not found")
        sys.exit(1)


def create_prompt(build_log):
    """Create the LLM prompt for build log analysis."""
    prompt = f"""You are assisting the RDK CMF team. Analyse the following CI build log.

Return:
1) A JSON array of the top 3 failure causes with fields:
   - cause: Brief description of the root cause
   - evidence: Line numbers or code snippets that support this finding
   - confidence: high/medium/low
   - next_action: Specific, actionable steps to fix this issue

2) A 3-bullet human summary suitable for a PR comment or Slack message.

Prefer evidence over speculation. If uncertain, mark confidence low.
Cite specific line numbers or code snippets when possible.

LOG:
{build_log}
"""
    return prompt


def call_openai(prompt, model='gpt-4'):
    """Call OpenAI API (requires OPENAI_API_KEY environment variable)."""
    try:
        import openai
    except ImportError:
        print("Error: openai package not installed. Install with: pip install openai")
        return None
    
    client = openai.OpenAI()
    
    # Models that support response_format with json_object
    json_supported_models = ['gpt-4-turbo', 'gpt-4-turbo-preview', 'gpt-3.5-turbo', 'gpt-4o', 'gpt-4o-mini']
    
    # Prepare request parameters
    request_params = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful DevOps engineer analyzing build logs. Always respond with valid JSON."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,  # Lower temperature for more consistent output
    }
    
    # Add response_format only for supported models
    if any(supported in model for supported in json_supported_models):
        request_params["response_format"] = {"type": "json_object"}
    else:
        # For models that don't support response_format, add JSON request to prompt
        request_params["messages"][1]["content"] = prompt + "\n\nIMPORTANT: Respond with valid JSON only, no additional text."
    
    try:
        response = client.chat.completions.create(**request_params)
        return response.choices[0].message.content
    except openai.BadRequestError as e:
        # If response_format fails, try without it
        if "response_format" in str(e):
            print(f"Warning: {model} doesn't support response_format, trying without it...")
            request_params.pop("response_format", None)
            request_params["messages"][1]["content"] = prompt + "\n\nIMPORTANT: Respond with valid JSON only, no additional text."
            response = client.chat.completions.create(**request_params)
            return response.choices[0].message.content
        else:
            raise


def call_anthropic(prompt, model='claude-3-5-sonnet-20241022'):
    """Call Anthropic API (requires ANTHROPIC_API_KEY environment variable)."""
    try:
        from anthropic import Anthropic
    except ImportError:
        print("Error: anthropic package not installed. Install with: pip install anthropic")
        return None
    
    client = Anthropic()
    
    response = client.messages.create(
        model=model,
        max_tokens=2000,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    
    return response.content[0].text


def call_ollama(prompt, model='llama3:instruct'):
    """Call Ollama API (requires Ollama running locally)."""
    import requests
    
    url = "http://localhost:11434/api/generate"
    
    # Normalize model name (handle variations like 'codellama' -> 'codellama:7b')
    # Check available models if needed
    if ':' not in model:
        # Try common variations
        model_variations = [f"{model}:7b", f"{model}:latest", model]
        model = model_variations[0]  # Default to :7b for code models
    
    # Add JSON format request to prompt (Ollama format parameter may not work consistently)
    json_prompt = prompt + "\n\nIMPORTANT: Respond with valid JSON only, no additional text. Use this format: {\"root_causes\": [...], \"summary\": [...]}"
    
    payload = {
        "model": model,
        "prompt": json_prompt,
        "stream": False,
        "format": "json"  # Request JSON output (may not work for all models)
    }
    
    try:
        response = requests.post(url, json=payload, timeout=120)  # Longer timeout for local models
        response.raise_for_status()
        result = response.json()
        
        # Ollama returns response in 'response' field
        if 'response' in result:
            return result['response']
        else:
            print(f"Warning: Unexpected Ollama response format: {result.keys()}")
            return str(result)
            
    except requests.exceptions.RequestException as e:
        print(f"Error calling Ollama: {e}")
        print("Make sure Ollama is running: ollama serve")
        print(f"Trying to verify model '{model}' is available...")
        
        # Try to list available models
        try:
            models_response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if models_response.status_code == 200:
                models = models_response.json().get('models', [])
                model_names = [m.get('name', '') for m in models]
                print(f"Available models: {', '.join(model_names)}")
                if model not in model_names:
                    print(f"Warning: Model '{model}' not found. Try one of the available models.")
        except:
            pass
        
        return None


def parse_llm_response(response_text):
    """Parse LLM JSON response and handle errors."""
    if not response_text:
        print("Warning: Empty response")
        return None
    
    # Debug: show what we got
    print(f"Debug: Response type: {type(response_text)}")
    print(f"Debug: Response preview: {str(response_text)[:200]}...")
    print()
    
    try:
        # Try to extract JSON from response (in case LLM adds extra text)
        # Look for JSON object in the response
        start = response_text.find('{')
        end = response_text.rfind('}') + 1
        
        if start == -1 or end == 0:
            print("Warning: No JSON found in response")
            print(f"Full response: {response_text}")
            return None
        
        json_str = response_text[start:end]
        parsed = json.loads(json_str)
        
        # Validate structure
        if not isinstance(parsed, dict):
            print(f"Warning: Parsed JSON is not a dict, it's {type(parsed)}")
            return parsed
        
        return parsed
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        print(f"Response was: {response_text[:500]}...")
        print()
        print("Trying to extract JSON manually...")
        
        # Try to find JSON array instead
        start = response_text.find('[')
        end = response_text.rfind(']') + 1
        if start != -1 and end > 0:
            try:
                json_str = response_text[start:end]
                parsed = json.loads(json_str)
                # Wrap in expected format
                return {"root_causes": parsed if isinstance(parsed, list) else [parsed]}
            except:
                pass
        
        return None


def format_output(analysis):
    """Format LLM analysis for human-readable output."""
    if not analysis:
        print("No analysis data available")
        return
    
    # Debug: check what we got
    if not isinstance(analysis, dict):
        print(f"Warning: Analysis is not a dict, it's a {type(analysis)}")
        print(f"Content: {str(analysis)[:200]}...")
        return
    
    print("=" * 60)
    print("LLM Build Log Analysis")
    print("=" * 60)
    print()
    
    # Print root causes
    if 'root_causes' in analysis:
        print("Top 3 Root Causes:")
        print()
        root_causes = analysis['root_causes']
        
        # Handle both list of dicts and list of strings
        if isinstance(root_causes, list):
            for i, cause in enumerate(root_causes, 1):
                if isinstance(cause, dict):
                    print(f"{i}. {cause.get('cause', 'Unknown')}")
                    print(f"   Evidence: {cause.get('evidence', 'N/A')}")
                    print(f"   Confidence: {cause.get('confidence', 'N/A')}")
                    print(f"   Next Action: {cause.get('next_action', 'N/A')}")
                elif isinstance(cause, str):
                    print(f"{i}. {cause}")
                else:
                    print(f"{i}. {str(cause)}")
                print()
        else:
            print(f"Warning: root_causes is not a list: {type(root_causes)}")
            print(f"Content: {root_causes}")
    
    # Print summary
    if 'summary' in analysis:
        print("Summary (for PR/Slack):")
        summary = analysis['summary']
        if isinstance(summary, list):
            for bullet in summary:
                print(f"  • {bullet}")
        elif isinstance(summary, str):
            print(f"  • {summary}")
        else:
            print(f"  • {str(summary)}")
        print()
    
    # Print full JSON for reference
    print("Full JSON Response:")
    print(json.dumps(analysis, indent=2))


def main():
    """Main function - demonstrates LLM API call."""
    # Read build log
    build_log = read_build_log()
    
    # Create prompt
    prompt = create_prompt(build_log)
    
    # Choose backend (uncomment one):
    # For OpenAI:
    # Recommended models that support JSON format:
    # response = call_openai(prompt, model='gpt-4o')  # Recommended: supports JSON format
    # response = call_openai(prompt, model='gpt-4-turbo')  # Also supports JSON format
    # response = call_openai(prompt, model='gpt-3.5-turbo')  # Cheaper option, supports JSON
    # response = call_openai(prompt, model='gpt-4')  # May not support response_format, will fallback
    
    # For Anthropic:
    # response = call_anthropic(prompt, model='claude-3-5-sonnet-20241022')
    # response = call_anthropic(prompt, model='claude-3-haiku-20240307')  # Cheaper option
    
    # For Ollama (local):
    response = call_ollama(prompt, model='codellama:7b')  # Code-focused model (use exact model name)
    # response = call_ollama(prompt, model='llama3:latest')  # General purpose model
    
    # Process response if available
    if response:
        analysis = parse_llm_response(response)
        format_output(analysis)
    else:
        # For demo purposes, show what the prompt looks like
        print("=" * 60)
        print("LLM Prompt (first 500 chars):")
        print("=" * 60)
        print(prompt[:500] + "...")
        print()
        print("=" * 60)
        print("To use this script:")
        print("=" * 60)
        print("1. Install required package:")
        print("   - OpenAI: pip install openai")
        print("   - Anthropic: pip install anthropic")
        print("   - Ollama: pip install requests (usually pre-installed)")
        print()
        print("2. Set API key:")
        print("   - OpenAI: export OPENAI_API_KEY='your-key'")
        print("   - Anthropic: export ANTHROPIC_API_KEY='your-key'")
        print("   - Ollama: Start with 'ollama serve' (no API key needed)")
        print()
        print("3. Uncomment the backend you want to use in main()")
        print()
        print("4. Run: python3 03_llm_api_call.py")
        print()


if __name__ == '__main__':
    main()

