import asyncio
import os
import sys

# Add base directory to sys.path
base_dir = r"c:\Users\RobsonSilva-AfixGraf\Habilidade_de_agente"
if base_dir not in sys.path:
    sys.path.append(base_dir)

# Add master bridge core to sys.path
bridge_core_path = os.path.join(base_dir, "07_KIMI_MEMORY_BRIDGE", "core")
if bridge_core_path not in sys.path:
    sys.path.insert(0, bridge_core_path)

from memory_adapter_master import memory_adapter

async def migrate(db_path=None):
    print(f"🚀 [Migration] Initializing Knowledge Migration to CMS (Target: {db_path or 'Default'})...")
    
    # Ensure backend and CMS mode
    os.environ["CMS_BASE_URL"] = "http://localhost:8090"
    if db_path:
        os.environ["EVOLUTION_LEDGER_DB"] = db_path
    
    # Re-initialize to pickup env changes
    from memory_adapter_master import MemoryAdapter
    local_adapter = MemoryAdapter()
    local_adapter.mode = "CMS"
    local_adapter._ensure_backend()
    
    total_synced = 0
    while True:
        result = await local_adapter.sync_pending_events()
        if result["status"] == "completed" and result["synced"] > 0:
            total_synced += result["synced"]
            print(f"Synced {result['synced']} events (Total: {total_synced})...")
        else:
            break
    
    if total_synced > 0 or result["status"] == "completed":
        print(f"✅ Migration successful! Synced {total_synced} cognitive events to CMS.")
    else:
        print(f"⚠️ Migration skipped or failed: {result.get('reason', 'No events to sync or error')}")

if __name__ == "__main__":
    target_db = sys.argv[1] if len(sys.argv) > 1 else None
    asyncio.run(migrate(target_db))
