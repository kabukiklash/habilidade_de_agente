import sys
import os
import json
from llm_integration import AnthropicProvider, LLMRequest

def brain_bridge(task_description, target_data=None, model="claude-3-haiku-20240307"):
    """
    Antigravity Brain Bridge: Delegates heavy context tasks to Claude.
    Used for: Code analysis, long log processing, and drafting.
    """
    provider = AnthropicProvider()
    
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
        print(f"[*] Antigravity Bridge: Delegating to Anthropic ({model})...", file=sys.stderr)
        response = provider.generate(request)
        return response.text
    except Exception as e:
        return f"[!] Brain Bridge Error: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python brain_bridge.py <task_description> [file_path]")
        sys.exit(1)
        
    task = sys.argv[1]
    data = ""
    
    if len(sys.argv) > 2:
        file_path = sys.argv[2]
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                data = f.read()
    
    print(brain_bridge(task, data))
