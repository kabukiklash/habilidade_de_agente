import sys
import os
import json
from llm_integration import AnthropicProvider, InceptionProvider, LLMRequest

def brain_bridge(task_description, target_data=None, model="claude-3-haiku-20240307", provider_name="anthropic"):
    """
    Antigravity Brain Bridge: Delegates heavy context tasks to external LLMs.
    """
    if provider_name == "inception":
        provider = InceptionProvider()
        default_model = "mercury-2"
    else:
        provider = AnthropicProvider()
        default_model = "claude-3-haiku-20240307"
    
    target_model = model if model != "claude-3-haiku-20240307" else default_model
    
    # Construct the instruction for a "Passive Auditor"
    prompt = f"""
    [ANTIGRAVITY EVOLUTION - BRAIN BRIDGE]
    Role: Senior Technical Auditor & Context Compressor.
    Constraint: Passive-Only (Analyze, do not execute).
    
    Task: {task_description}
    
    Data/Context:
    {target_data if target_data else "No additional data provided."}
    
    Output Format:
    1. Summary (token-efficient)
    2. Critical Findings
    3. Suggested Next Step (Antigravity scope)
    """
    
    request = LLMRequest(
        prompt=prompt,
        model=model,
        max_tokens=2048,
        temperature=0.3 # Low temperature for analytical rigor
    )
    
    try:
        from llm_integration.reporter import print_token_economy_report
        import time
        print(f"[*] Antigravity Bridge: Delegating to {provider_name.upper()} ({target_model})...", file=sys.stderr)
        
        start_time = time.time()
        response = provider.generate(request)
        end_time = time.time()
        
        # Calculate tokens
        tokens_used = 0
        if hasattr(response, 'usage') and hasattr(response.usage, 'total_tokens'):
            tokens_used = response.usage.total_tokens
        
        # Approximate raw context cost vs actual prompt cost
        tokens_saved = max(0, (len(target_data) if target_data else 0) // 4 - tokens_used)
        
        print_token_economy_report(tokens_used, tokens_saved, int((end_time - start_time) * 1000))
        
        return response.text
    except Exception as e:
        return f"[!] Brain Bridge Error: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python brain_bridge.py <task_description> [file_path] [provider] [model]")
        sys.exit(1)
        
    task = sys.argv[1]
    data = ""
    provider = "anthropic"
    model = "claude-3-haiku-20240307"
    
    if len(sys.argv) > 2:
        file_path = sys.argv[2]
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                data = f.read()
    
    if len(sys.argv) > 3:
        provider = sys.argv[3]
    
    if len(sys.argv) > 4:
        model = sys.argv[4]
    
    print(brain_bridge(task, data, model=model, provider_name=provider))
