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
        
        if self.mode == "CMS" and self.cms_client:
            try:
                return await self.cms_client.append_event(
                    event_type, self.actor, payload, justification, correlation_id, event_id, tokens_used, tokens_saved, usd_saved
                )
            except Exception as e:
                print(f"CMS Failure: {e}. Falling back to SQLite.")

        if self.sqlite_ledger:
            return self._append_sqlite(event_type, payload, justification, correlation_id, event_id, tokens_used, tokens_saved, usd_saved)
            
        raise RuntimeError(f"No memory backend available (Fallback failed)")

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

    async def consolidate(self, query_text: str) -> Dict[str, Any]:
        self._ensure_backend()
        if self.mode == "CMS" and self.cms_client:
            return await self.cms_client.consolidate(query_text)
        return self._query_sqlite(query_text)

# Singleton handle
memory_adapter = MemoryAdapter()
