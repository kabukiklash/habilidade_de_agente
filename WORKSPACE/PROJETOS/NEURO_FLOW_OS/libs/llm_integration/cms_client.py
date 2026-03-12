"""
CMS Client: Integration Layer for Antigravity -> Cognitive Memory Service
Provides high-level functions for memory operations.
"""
import httpx
from typing import Optional, Dict, List, Any
import os


class CMSClient:
    """Client for interacting with the Cognitive Memory Service."""
    
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or os.getenv("CMS_BASE_URL", "http://localhost:8090")
    
    async def append_event(
        self,
        event_type: str,
        actor: str,
        payload: Dict[str, Any],
        justification: Optional[str] = None,
        correlation_id: Optional[str] = None,
        tokens_used: int = 0,
        tokens_saved: int = 0
    ) -> Dict[str, str]:
        """Append an event to the immutable log."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/tables/events/append",
                json={
                    "event_type": event_type,
                    "actor": actor,
                    "payload": payload,
                    "justification": justification,
                    "correlation_id": correlation_id,
                    "tokens_used": tokens_used,
                    "tokens_saved": tokens_saved
                }
            )
            response.raise_for_status()
            return response.json()
    
    async def query_memory(
        self,
        query_text: str,
        requester: str = "ANTIGRAVITY",
        vector_topk: int = 10,
        graph_hops: int = 1,
        max_nodes: int = 50,
        exclude_expired: bool = True,
        policy_scope: Optional[str] = None
    ) -> Dict[str, Any]:
        """Hybrid memory retrieval: vector + graph + rerank."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/memory/query",
                json={
                    "query_text": query_text,
                    "requester": requester,
                    "vector_topk": vector_topk,
                    "graph_hops": graph_hops,
                    "max_nodes": max_nodes,
                    "exclude_expired": exclude_expired,
                    "policy_scope": policy_scope
                }
            )
            response.raise_for_status()
            return response.json()
    
    async def pin(self, artifact_id: str) -> Dict[str, str]:
        """Pin an artifact to survive TTL expiration."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/governance/pin/artifact/{artifact_id}"
            )
            response.raise_for_status()
            return response.json()
    
    async def forget(
        self,
        target_type: str,
        target_ids: List[str],
        reason: str
    ) -> Dict[str, Any]:
        """Revoke and deindex items (soft delete)."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/governance/forget",
                json={
                    "target_type": target_type,
                    "target_ids": target_ids,
                    "reason": reason
                }
            )
            response.raise_for_status()
            return response.json()
    
    async def consolidate(self, query_text: str) -> Dict[str, Any]:
        """
        Consolidate memory: Query, then return a structured Context Pack.
        This is a convenience method that wraps query_memory.
        """
        result = await self.query_memory(
            query_text=query_text,
            vector_topk=20,
            graph_hops=2
        )
        
        # Build a simplified context pack for the LLM
        context = result.get("context", {})
        return {
            "facts": context.get("facts", []),
            "artifacts": context.get("artifacts", []),
            "concepts": context.get("concepts", []),
            "links": context.get("links", []),
            "explain": context.get("explain", []),
            "query_id": result.get("query_id"),
            "latency_ms": result.get("latency_ms")
        }


# Convenience instance for direct import
cms_client = CMSClient()
