import os
import sys
import logging

# Add current directory to path to allow importing the internal package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from llm_integration import AnthropicProvider, LLMRequest

# Configure logging to see the sanitization in action
logging.basicConfig(level=logging.INFO)

def run_example():
    print("--- Anthropic Integration Example ---")
    
    # Check for API Key
    if "ANTHROPIC_API_KEY" not in os.environ:
        print("WARNING: ANTHROPIC_API_KEY not found in environment variables.")
        print("Please set it: $env:ANTHROPIC_API_KEY='your-key-here'")
        # return # We let it continue to demonstrate the error handling

    provider = AnthropicProvider()
    
    request = LLMRequest(
        prompt="Explain what a passive-only LLM agent is in 2 sentences.",
        model="claude-3-haiku-20240307",
        temperature=1.0
    )

    try:
        print("Generating response...")
        response = provider.generate(request)
        
        print(f"\nResponse (ID: {response.request_id}):")
        print(f"Text: {response.text}")
        print(f"\nUsage:")
        print(f"  Prompt tokens: {response.usage.prompt_tokens}")
        print(f"  Completion tokens: {response.usage.completion_tokens}")
        print(f"  Total tokens: {response.usage.total_tokens}")
        
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    run_example()
