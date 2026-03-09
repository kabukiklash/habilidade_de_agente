import sys
import os
import asyncio
from typing import Optional

# Ensure path is correct for Antigravity imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from llm_integration.cms_client import CMSClient
from antigravity_memory_backend.memory_adapter import memory_adapter
from llm_integration.reporter import print_token_economy_report

async def log_manual_session(tokens_used: int, tokens_saved: int, description: str):
    """
    Manually injects IDE Chat Session tokens into the Antigravity Token Economy Ledger.
    """
    print(f"[*] Connecting to Antigravity CMS Ledger...")
    
    correlation_id = f"ide_session_{int(asyncio.get_event_loop().time())}"
    
    payload = {
        "source": "IDE_CHAT_EXTENSION",
        "session_description": description
    }
    
    try:
        # Append to the dual-layered memory (CMS Postgres + Local SQLite)
        result = await memory_adapter.append_event(
            event_type="IDE_SESSION_AUDIT",
            payload=payload,
            justification=f"IDE Chat Manual Log: {description}",
            correlation_id=correlation_id,
            tokens_used=tokens_used,
            tokens_saved=tokens_saved
        )
        
        print(f"[+] Successfully injected into Ledger! (Backend: {result.get('backend', 'UNKNOWN')})")
        print_token_economy_report(tokens_used, tokens_saved)
        
    except Exception as e:
        print(f"[!] Critical Error injecting into Ledger: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python log_session.py <tokens_used> <tokens_saved> \"<description>\"")
        print("Example: python log_session.py 1500 5000 \"Refactoring the backend with Gemini IDE\"")
        sys.exit(1)
        
    try:
        t_used = int(sys.argv[1])
        t_saved = int(sys.argv[2])
        desc = sys.argv[3]
        
        asyncio.run(log_manual_session(t_used, t_saved, desc))
    except ValueError:
        print("[!] Error: tokens_used and tokens_saved must be integers.")
        sys.exit(1)
