"""
Antigravity Memory Backend - CMS-First Mode
Provides a unified interface for memory operations.
"""
import os
import asyncio
import sys
import json
from typing import Optional, Dict, List, Any
from datetime import datetime

# Normalize paths for Sovereign Technologies - DO THIS FIRST
base_dir = "c:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente"
tech_01_path = os.path.join(base_dir, "01_COGNITIVE_MEMORY_SERVICE", "client")

# Prioritize Technology 01 Master Client
if tech_01_path not in sys.path:
    sys.path.insert(0, tech_01_path)
if base_dir not in sys.path:
    sys.path.append(base_dir)

class MemoryAdapter:
    """
    Unified memory adapter for Antigravity.
    """
    def __init__(self, sqlite_path: Optional[str] = None):
        self.actor = "MEMORY_ADAPTER"
        self.mode = "OFFLINE"
        self.sqlite_path = sqlite_path
        
        if os.getenv("CMS_BASE_URL"):
            self.mode = "CMS"
        
        self.sqlite_ledger = None
        self.cms_client = None

    def _ensure_backend(self):
        """Lazy load backends to avoid circular imports during module initialization."""
        if self.mode == "CMS" and self.cms_client is None:
            try:
                # Import from cms_client_master.py in Tech 01
                from cms_client_master import CMSClient
                self.cms_client = CMSClient()
            except ImportError:
                print("[!] Failed to import Master CMS Client from Technology 01")
                pass
        
        if self.sqlite_ledger is None:
            try:
                # Prioritize Sovereign Ledger Manager from Technology 06
                tech_06_path = os.path.join(base_dir, "06_AUDIT_MONITOR_LEDGER", "core")
                if tech_06_path not in sys.path:
                    sys.path.insert(0, tech_06_path)
                
                from ledger_manager_master import LedgerManager
                db_file = self.sqlite_path or os.environ.get("EVOLUTION_LEDGER_DB", os.path.join(base_dir, "01_COGNITIVE_MEMORY_SERVICE", "database", "evolution.db"))
                self.sqlite_ledger = LedgerManager(db_file)
            except ImportError:
                print("[!] Failed to import Sovereign Ledger Manager from Technology 06")
                pass

    def is_cognitive(self, event_type: str) -> bool:
        """Classifies events into Cognitive (Strategic) or Operational (Tactical)."""
        COGNITIVE_TYPES = [
            "KNOWLEDGE_SYNC", "GOAL_UPDATE", "DECISION_LOG", 
            "CONCEPTS", "SOLUTIONS", "AUDIT_REPORT", "CORTEX_DECISION"
        ]
        return event_type in COGNITIVE_TYPES or event_type.startswith("KIM")

    async def append_event(
        self,
        event_type: str,
        payload: Dict[str, Any],
        justification: Optional[str] = None,
        correlation_id: Optional[str] = None,
        event_id: Optional[str] = None,
        tokens_used: int = 0,
        tokens_saved: int = 0,
        usd_saved: float = 0.0
    ) -> Dict[str, str]:
        """Append an event to the selected memory backend."""
        self._ensure_backend()
        
        # Ensure event_id exists (implements 'Platform-Grade' DedupeKey/Idempotency)
        import uuid
        event_id = event_id or str(uuid.uuid4())
        
        # 1. Classification
        is_cog = self.is_cognitive(event_type)
        
        # 1.5 Semantic Deduplication (Phase 1 Governance)
        if is_cog and self.mode == "CMS":
            try:
                # Create a small string representation for search
                query_str = json.dumps(payload)
                if len(query_str) > 500:
                    query_str = query_str[:500]
                
                # Check directly with CMS
                search_res = await self.query_memory(query_str, vector_topk=1)
                facts = search_res.get("context", {}).get("facts", [])
                
                if facts:
                    top_fact = facts[0]
                    # Score might be 'score', 'similarity', or 'distance' (if distance, lower is better but we assume score here)
                    score = top_fact.get("score", top_fact.get("similarity", 0.0))
                    
                    if isinstance(score, (int, float)) and score > 0.85:
                        print(f"[*] Semantic Deduplication TRIGGERED: Similar knowledge found (Score: {score}). Blocking persistence.")
                        return {
                            "status": "deduplicated", 
                            "event_id": top_fact.get("id", top_fact.get("event_id", "EXISTING_REF")), 
                            "backend": "CMS_CACHE",
                            "score": score
                        }
            except Exception as e:
                print(f"[!] Semantic Dedupe check failed: {e}. Proceeding directly to append.")
        
        # 2. Routing Logic
        if is_cog:
            # Cognitive events MUST go to CMS
            if self.mode == "CMS" and self.cms_client:
                try:
                    res = await self.cms_client.append_event(
                        event_type, self.actor, payload, justification, correlation_id, event_id, tokens_used, tokens_saved, usd_saved
                    )
                    # If we have a local ledger, we can still record it as SYNCED for forensic trail if needed,
                    # but the directive says "No Duplication". 
                    # We'll skip local record if CMS succeeds, unless it's a critical audit.
                    return res
                except Exception as e:
                    print(f"CMS Failure for Cognitive Event: {e}. Buffered in SQLite (PENDING).")
            
            # Fallback for Cognitive: Buffer in SQLite as PENDING
            if self.sqlite_ledger:
                return self._append_sqlite(event_type, payload, justification, correlation_id, event_id, tokens_used, tokens_saved, usd_saved)
        else:
            # Operational events go to SQLite ONLY (05_PROJECT_GRAPH / 06_PER_FRICTION)
            if self.sqlite_ledger:
                if event_type == "PROJECT_GRAPH_SYNC":
                    self.sqlite_ledger.record_graph(payload.get("file_path"), payload.get("hash"), payload.get("node_type"), payload.get("metadata", {}))
                elif event_type == "IO_FRICTION":
                    self.sqlite_ledger.record_friction(payload.get("op"), payload.get("latency"), payload.get("error"), correlation_id)
                
                return self._append_sqlite(event_type, payload, justification, correlation_id, event_id, tokens_used, tokens_saved, usd_saved)

        raise RuntimeError(f"No memory backend available for routing")

    def _append_sqlite(self, event_type, payload, justification, correlation_id, event_id, tokens_used, tokens_saved, usd_saved) -> Dict[str, str]:
        e_id = self.sqlite_ledger.record_event(
            event_type, payload, justification, correlation_id, self.actor, tokens_used, tokens_saved, usd_saved, event_id
        )
        return {"status": "recorded", "event_id": e_id, "backend": "SQLITE"}

    async def query_memory(self, query_text: str, vector_topk: int = 5) -> Dict[str, Any]:
        """Query memory using hybrid approach."""
        self._ensure_backend()
        
        if self.mode == "CMS" and self.cms_client:
            try:
                return await self.cms_client.query_memory(query_text, vector_topk=vector_topk)
            except Exception as e:
                return self._query_sqlite(query_text)
        
        return self._query_sqlite(query_text)
    
    def _query_sqlite(self, query_text: str) -> Dict[str, Any]:
        """Fallback: Busca real no ledger local quando o CMS falha."""
        self._ensure_backend()
        
        if not self.sqlite_ledger:
            return {"context": {"facts": []}, "backend": "SQLITE_EMPTY"}
            
        event_type = None
        search_term = query_text
        if "VIBE_SIGNATURE" in query_text:
            event_type = "VIBE_SIGNATURE"
            if "for " in query_text:
                search_term = query_text.split("for ")[1].strip()
        
        events = self.sqlite_ledger.query_events(event_type=event_type, query_text=search_term)
        facts = []
        for ev in events:
            payload_str = json.dumps(ev["payload"])
            facts.append(f"[{ev['timestamp']}] {ev['event_type']} - justification: {ev['justification']} | payload: {payload_str}")
            
        return {
            "context": {
                "facts": facts,
                "artifacts": [],
                "concepts": [],
                "links": [],
                "explain": [{"why": "Busca direta no Ledger SQLite (Modo Offline/Fallback)"}]
            },
            "query_id": "local",
            "latency_ms": 1,
            "backend": "SQLITE"
        }

    async def sync_pending_events(self) -> Dict[str, Any]:
        """Drains the SQLite buffer to CMS."""
        self._ensure_backend()
        if not (self.mode == "CMS" and self.cms_client and self.sqlite_ledger):
            return {"status": "skipped", "reason": "CMS or SQLite not available"}
        
        # Query PENDING events
        pending = self.sqlite_ledger.query_events(sync_status="PENDING", limit=100)
        
        synced_count = 0
        for ev in pending:
            try:
                await self.cms_client.append_event(
                    ev["event_type"], self.actor, ev["payload"], ev["justification"], None, ev["event_id"]
                )
                self.sqlite_ledger.mark_as_synced(ev["event_id"])
                synced_count += 1
            except Exception as e:
                print(f"Failed to sync event {ev['event_id']}: {e}")
                break # Stop if CMS is still down
        
        return {"status": "completed", "synced": synced_count}

# Singleton handle
memory_adapter = MemoryAdapter()

if __name__ == "__main__":
    if "--test-2-layer" in sys.argv:
        print("🚀 [Test] Running 2-Layer Memory Routing Test...")
        
        async def run_test():
            # 1. Test Cognitive Routing
            cog_event = "KNOWLEDGE_SYNC"
            cog_payload = {"test": "cognitive_data"}
            print(f"[*] Testing Cognitive Routing for {cog_event}...")
            
            # Use a mock or just check the return backend if possible
            # For now, we'll check where it lands in SQLite if CMS is not set or fails
            res = await memory_adapter.append_event(cog_event, cog_payload, justification="Unit Test")
            print(f"[+] Result: {res}")
            
            # 2. Test Operational Routing
            op_event = "PROJECT_GRAPH_SYNC"
            op_payload = {"file_path": "test.py", "hash": "abc"}
            print(f"[*] Testing Operational Routing for {op_event}...")
            res_op = await memory_adapter.append_event(op_event, op_payload, justification="Unit Test")
            print(f"[+] Result: {res_op}")
            
            # 3. Verification in DB
            from ledger_manager_master import LedgerManager
            db_file = os.environ.get("EVOLUTION_LEDGER_DB", os.path.join(base_dir, "01_COGNITIVE_MEMORY_SERVICE", "database", "evolution.db"))
            lm = LedgerManager(db_file)
            
            # Check Op table
            import sqlite3
            with sqlite3.connect(db_file) as conn:
                cursor = conn.execute("SELECT count(*) FROM project_graph WHERE file_path='test.py'")
                cnt = cursor.fetchone()[0]
                print(f"[+] Project Graph count for test.py: {cnt}")
            
            # Check Audit Ledger status
            events = lm.query_events(limit=5)
            for ev in events:
                if ev["event_type"] == cog_event:
                    print(f"[+] Cog Event {ev['event_id']} Sync Status: {ev.get('sync_status')}")
                if ev["event_type"] == op_event:
                    print(f"[+] Op Event {ev['event_id']} Sync Status: {ev.get('sync_status')}")

        asyncio.run(run_test())
