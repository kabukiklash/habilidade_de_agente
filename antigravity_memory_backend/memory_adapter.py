"""
Antigravity Memory Backend - CMS-First Mode
Provides a unified interface for memory operations, using CMS as primary backend.
"""
import os
import asyncio
from typing import Optional, Dict, List, Any
from datetime import datetime

# Try to import CMS client
try:
    from llm_integration.cms_client import CMSClient
    CMS_AVAILABLE = True
except ImportError:
    CMS_AVAILABLE = False

# Fallback to local SQLite if CMS is unavailable
try:
    from llm_integration.ledger_manager import LedgerManager
    SQLITE_AVAILABLE = True
except ImportError:
    SQLITE_AVAILABLE = False


class MemoryAdapter:
    """
    Unified memory adapter for Antigravity.
    Primary: CMS (Cognitive Memory Service)
    Fallback: Local SQLite Ledger (offline only)
    """
    
    def __init__(
        self,
        cms_url: Optional[str] = None,
        sqlite_path: Optional[str] = None,
        actor: str = "ANTIGRAVITY"
    ):
        self.actor = actor
        self.cms_client = None
        self.sqlite_ledger = None
        self.mode = "OFFLINE"
        
        # Initialize CMS client (primary)
        if CMS_AVAILABLE:
            cms_url = cms_url or os.getenv("CMS_BASE_URL", "http://localhost:8090")
            self.cms_client = CMSClient(base_url=cms_url)
            self.mode = "CMS"
        
        # Initialize SQLite fallback
        if SQLITE_AVAILABLE and sqlite_path:
            self.sqlite_ledger = LedgerManager(sqlite_path)
            if self.mode == "OFFLINE":
                self.mode = "SQLITE"
    
    async def append_event(
        self,
        event_type: str,
        payload: Dict[str, Any],
        justification: Optional[str] = None,
        correlation_id: Optional[str] = None,
        tokens_used: int = 0,
        tokens_saved: int = 0
    ) -> Dict[str, str]:
        """
        Write an event to the memory backend.
        Returns: {"event_id": ..., "created_at": ..., "backend": "CMS" | "SQLITE"}
        """
        if self.mode == "CMS" and self.cms_client:
            try:
                result = await self.cms_client.append_event(
                    event_type=event_type,
                    actor=self.actor,
                    payload=payload,
                    justification=justification,
                    correlation_id=correlation_id,
                    tokens_used=tokens_used,
                    tokens_saved=tokens_saved
                )
                result["backend"] = "CMS"
                return result
            except Exception as e:
                # Fallback to SQLite on CMS failure
                if self.sqlite_ledger:
                    return self._append_sqlite(event_type, payload, justification, correlation_id, tokens_used, tokens_saved)
                raise e
        
        if self.sqlite_ledger:
            return self._append_sqlite(event_type, payload, justification, correlation_id, tokens_used, tokens_saved)
        
        raise RuntimeError("No memory backend available")
    
    def _append_sqlite(
        self,
        event_type: str,
        payload: Dict[str, Any],
        justification: Optional[str] = None,
        correlation_id: Optional[str] = None,
        tokens_used: int = 0,
        tokens_saved: int = 0
    ) -> Dict[str, str]:
        """Fallback: Write to local SQLite ledger."""
        import json
        event_id = self.sqlite_ledger.record_event(
            event_type=event_type,
            payload=payload,
            justification=justification or "Direct SQLite Append",
            correlation_id=correlation_id,
            tokens_used=tokens_used,
            tokens_saved=tokens_saved
        )
        return {
            "event_id": str(event_id),
            "created_at": datetime.utcnow().isoformat(),
            "backend": "SQLITE"
        }
    
    async def query_memory(
        self,
        query_text: str,
        vector_topk: int = 10,
        graph_hops: int = 1,
        max_nodes: int = 50
    ) -> Dict[str, Any]:
        """
        Query memory for relevant context.
        Returns: ContextPack with facts, artifacts, concepts, links, explain.
        """
        if self.mode == "CMS" and self.cms_client:
            try:
                result = await self.cms_client.query_memory(
                    query_text=query_text,
                    requester=self.actor,
                    vector_topk=vector_topk,
                    graph_hops=graph_hops,
                    max_nodes=max_nodes
                )
                result["backend"] = "CMS"
                return result
            except Exception as e:
                # Fallback to local search
                return self._query_sqlite(query_text)
        
        return self._query_sqlite(query_text)
    
    def _query_sqlite(self, query_text: str) -> Dict[str, Any]:
        """Fallback: Simple keyword search in local ledger."""
        # Basic implementation - returns empty context
        return {
            "context": {
                "facts": [],
                "artifacts": [],
                "concepts": [],
                "links": [],
                "explain": [{"why": "OFFLINE mode - no semantic search"}]
            },
            "query_id": "local",
            "latency_ms": 0,
            "backend": "SQLITE"
        }
    
    async def consolidate(self, query_text: str) -> Dict[str, Any]:
        """
        Convenience method: Query and return structured context for LLM injection.
        """
        if self.mode == "CMS" and self.cms_client:
            return await self.cms_client.consolidate(query_text)
        return self._query_sqlite(query_text)
    
    async def pin(self, artifact_id: str) -> Dict[str, str]:
        """Pin an artifact to survive TTL expiration."""
        if self.mode == "CMS" and self.cms_client:
            return await self.cms_client.pin(artifact_id)
        return {"status": "not_available", "reason": "CMS not connected"}
    
    async def forget(
        self,
        target_type: str,
        target_ids: List[str],
        reason: str
    ) -> Dict[str, Any]:
        """Revoke and deindex items (soft delete)."""
        if self.mode == "CMS" and self.cms_client:
            return await self.cms_client.forget(target_type, target_ids, reason)
        return {"affected_count": 0, "reason": "CMS not connected"}
    
    def get_status(self) -> Dict[str, str]:
        """Return current backend status."""
        return {
            "mode": self.mode,
            "cms_available": CMS_AVAILABLE and self.cms_client is not None,
            "sqlite_available": SQLITE_AVAILABLE and self.sqlite_ledger is not None,
            "actor": self.actor
        }


# Global instance for easy import
memory_adapter = MemoryAdapter()
