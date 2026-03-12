
import asyncio
import sys
import os

# Add parent directory to sys.path
sys.path.append(os.getcwd())

from llm_integration.kimi_client import kimi_client
from llm_integration.cognitive_cortex import cognitive_cortex
from antigravity_memory_backend.memory_adapter import memory_adapter

async def sync():
    # 1. Load context files
    try:
        with open("ANTIGRAVITY_MANUAL.md", "r", encoding="utf-8") as f:
            manual = f.read()
        with open("ANTIGRAVITY_SYSTEM_REPORT_2026.md", "r", encoding="utf-8") as f:
            report = f.read()
        
        skills_raw = os.listdir(".agent/skills")
        skills_list = "\n".join([f"- {s}" for s in skills_raw if os.path.isdir(f".agent/skills/{s}")])
    except Exception as e:
        print(f"❌ Error loading docs: {e}")
        return

    # 2. Build the "Sync Prompt"
    sync_prompt = f"""
ROLE: You are the COGNITIVE CORTEX for the Antigravity system.
STATUS: Knowledge Synchronization (Evolution Phase 3)

Below is the INTERNAL KNOWLEDGE of this local instance. You must LEARN this to perform as the expert orchestrator.

### 🧠 SYSTEM MANUAL
{manual}

### 🛡️ SYSTEM REPORT
{report}

### 🛠️ LOCAL SKILLS INVENTORY (42 SKILLS)
{skills_list}

---
QUIZ: Based on the knowledge above, what is the RELATIONSHIP between the CMS (8090) and the ResistOS Kernel (Foundation)?
Explain in one paragraph to demonstrate your sync success.
"""

    print("🚀 [Sync] Sending Context Injection to Kimi...")
    try:
        # We use chat_thinking for high-density context
        messages = [
            {"role": "system", "content": "You are the Antigravity Cognitive Cortex. Synchronize your knowledge with the provided local context."},
            {"role": "user", "content": sync_prompt}
        ]
        response = await kimi_client.chat_completion(messages, model="kimi-k2-turbo-preview", use_thinking=True)
        solution = response["choices"][0]["message"]["content"]
        
        print("\n--- SYNC VERIFICATION FROM KIMI ---")
        print(solution)
        print("-----------------------------------")

        # 3. Record Sync in CMS
        await memory_adapter.append_event(
            event_type="KNOWLEDGE_SYNC",
            payload={
                "manual_version": "v4.0.0",
                "skills_count": len(skills_raw),
                "kimi_model": "kimi-k2-turbo-preview",
                "sync_verification_preview": solution[:200]
            },
            justification="Full context injection to synchronize Kimi with local Antigravity environment."
        )
        
        with open("kimi_sync_result.txt", "w", encoding="utf-8") as f:
            f.write(solution)
            
    except Exception as e:
        print(f"❌ Sync Error: {e}")

if __name__ == "__main__":
    asyncio.run(sync())
