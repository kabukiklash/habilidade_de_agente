"""
Antigravity Context Injector
Automatically injects CMS memory context into LLM prompts before completion.
"""
from typing import Optional, Dict, Any
from antigravity_memory_backend.memory_adapter import MemoryAdapter


class ContextInjector:
    """
    Injects memory context from CMS into prompts before LLM completion.
    
    Usage:
        injector = ContextInjector()
        enriched_prompt = await injector.inject(user_prompt)
        # Use enriched_prompt for LLM completion
    """
    
    CONTEXT_TEMPLATE = """
=== MEMORY CONTEXT (CMS) ===
QUERY: {query_text}
BACKEND: {backend}
LATENCY: {latency_ms}ms

FACTS:
{facts}

ARTIFACTS:
{artifacts}

CONCEPTS:
{concepts}

EXPLAIN:
{explain}
===========================

{original_prompt}
"""
    
    def __init__(self, memory_adapter: Optional[MemoryAdapter] = None):
        self.adapter = memory_adapter or MemoryAdapter()
    
    async def inject(
        self,
        prompt: str,
        query_override: Optional[str] = None,
        vector_topk: int = 10,
        graph_hops: int = 2
    ) -> str:
        """
        Inject memory context into the prompt.
        
        Args:
            prompt: Original user prompt
            query_override: Custom query for memory search (defaults to prompt)
            vector_topk: Number of top vector results
            graph_hops: Number of graph expansion hops
            
        Returns:
            Enriched prompt with memory context prepended
        """
        query_text = query_override or prompt
        
        try:
            result = await self.adapter.query_memory(
                query_text=query_text,
                vector_topk=vector_topk,
                graph_hops=graph_hops
            )
            
            context = result.get("context", {})
            
            # Format each section
            facts_str = self._format_list(context.get("facts", []), "content")
            artifacts_str = self._format_list(context.get("artifacts", []), "title")
            concepts_str = self._format_list(context.get("concepts", []), "name")
            explain_str = self._format_explain(context.get("explain", []))
            
            # Build enriched prompt
            enriched = self.CONTEXT_TEMPLATE.format(
                query_text=query_text[:100] + "..." if len(query_text) > 100 else query_text,
                backend=result.get("backend", "UNKNOWN"),
                latency_ms=result.get("latency_ms", 0),
                facts=facts_str or "(none)",
                artifacts=artifacts_str or "(none)",
                concepts=concepts_str or "(none)",
                explain=explain_str or "(no explanation)",
                original_prompt=prompt
            )
            
            return enriched
            
        except Exception as e:
            # On failure, return original prompt with error note
            return f"[CMS Error: {e}]\n\n{prompt}"
    
    def _format_list(self, items: list, key: str) -> str:
        """Format a list of items into bullet points."""
        if not items:
            return ""
        lines = []
        for item in items[:10]:  # Limit to 10 items
            value = item.get(key, str(item))
            if isinstance(value, str) and len(value) > 200:
                value = value[:200] + "..."
            lines.append(f"  - {value}")
        return "\n".join(lines)
    
    def _format_explain(self, explains: list) -> str:
        """Format explain entries."""
        if not explains:
            return ""
        lines = []
        for exp in explains[:5]:  # Limit to 5 explanations
            ref_id = exp.get("ref_id", "?")
            why = exp.get("why", "no reason")
            score = exp.get("score", 0)
            lines.append(f"  - [{score:.2f}] {ref_id}: {why}")
        return "\n".join(lines)
    
    async def get_raw_context(
        self,
        query_text: str,
        vector_topk: int = 10,
        graph_hops: int = 2
    ) -> Dict[str, Any]:
        """
        Get raw context without injection (for debugging/inspection).
        """
        return await self.adapter.query_memory(
            query_text=query_text,
            vector_topk=vector_topk,
            graph_hops=graph_hops
        )


# Global instance for easy import
context_injector = ContextInjector()
