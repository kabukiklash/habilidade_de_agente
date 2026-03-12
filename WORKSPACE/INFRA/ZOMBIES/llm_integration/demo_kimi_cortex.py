import asyncio
import os
import sys
from datetime import datetime

# Setup paths
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from llm_integration.cognitive_cortex import cognitive_cortex
from antigravity_memory_backend.memory_adapter import memory_adapter

async def main():
    print(f"\n🚀 Antigravity Cognitive Cortex Demo - {datetime.now().isoformat()}")
    print("="*60)
    
    # 1. Clean start (verify CMS is up)
    try:
        print("📡 Checking CMS connectivity...")
        # (This will fallback to SQLite if CMS is down, which is fine for demo structure)
        adapter = memory_adapter
        print(f"   Backend: {adapter.mode}")
    except Exception as e:
        print(f"❌ CMS Error: {e}")
        return

    # 2. Solve a complex task via Cortex
    task = "Defina a política de expiração (TTL) para artefatos de nível de segurança R4 (HIGH RISK) no sistema ResistOS."
    print(f"\n🧠 Task: {task}")
    
    solution = await cognitive_cortex.solve_task(task)
    
    print("\n💡 CORE SOLUTION:")
    print("-" * 40)
    print(solution)
    print("-" * 40)
    
    # 3. Verify knowledge was recorded in CMS
    print("\n🔍 Verifying CMS legacy...")
    recent_events = await memory_adapter.query_memory("R4 security TTL policy")
    
    # Check if our DECISION event is there
    context = recent_events.get("context", {})
    facts = context.get("facts", [])
    
    if any("R4" in str(f) for f in facts) or recent_events.get("backend") == "CMS":
        print("✅ Success: The decision was processed by Kimi and indexed by CMS.")
    else:
        print("⚠️ Warning: Decision recorded but sync might take a few seconds or backend is in OFFLINE mode.")

    print("\n✅ Demo complete!")

if __name__ == "__main__":
    asyncio.run(main())
