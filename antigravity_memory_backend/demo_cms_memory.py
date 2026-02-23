"""
Antigravity CMS Integration - Demo Script
Proves that memory persists across sessions via CMS.

Run this script twice to see memory persistence:
  Day 1: python demo_cms_memory.py --action=store
  Day 2: python demo_cms_memory.py --action=recall
"""
import asyncio
import argparse
import json
from datetime import datetime


async def store_decision():
    """Simulate Day 1: Store a decision in CMS."""
    from antigravity_memory_backend.memory_adapter import MemoryAdapter
    
    adapter = MemoryAdapter()
    print(f"📡 Backend Mode: {adapter.mode}")
    
    # Store decision
    result = await adapter.append_event(
        event_type="DECISION",
        payload={
            "decision": "PER precisa passar pelo Watchdog",
            "context": "Decisão arquitetural para validação de intents",
            "author": "ARCHITECT"
        },
        justification="Requisito de governança para execução segura de ferramentas"
    )
    
    print(f"✅ Decision stored!")
    print(f"   event_id: {result.get('event_id')}")
    print(f"   created_at: {result.get('created_at')}")
    print(f"   backend: {result.get('backend')}")
    
    return result


async def recall_decision():
    """Simulate Day 2: Recall the decision from CMS."""
    from antigravity_memory_backend.memory_adapter import MemoryAdapter
    from antigravity_memory_backend.context_injector import ContextInjector
    
    adapter = MemoryAdapter()
    injector = ContextInjector(adapter)
    
    print(f"📡 Backend Mode: {adapter.mode}")
    
    # Query memory
    query = "O que foi decidido sobre PER e Watchdog?"
    print(f"\n🔍 Query: {query}")
    
    result = await adapter.query_memory(
        query_text=query,
        vector_topk=10,
        graph_hops=2
    )
    
    print(f"\n📦 Context Pack:")
    print(f"   query_id: {result.get('query_id')}")
    print(f"   latency_ms: {result.get('latency_ms')}")
    print(f"   backend: {result.get('backend')}")
    
    context = result.get("context", {})
    print(f"\n   Facts: {len(context.get('facts', []))}")
    print(f"   Artifacts: {len(context.get('artifacts', []))}")
    print(f"   Concepts: {len(context.get('concepts', []))}")
    print(f"   Links: {len(context.get('links', []))}")
    
    # Show explain
    explains = context.get("explain", [])
    if explains:
        print(f"\n📋 Explain (why each item was returned):")
        for exp in explains[:5]:
            print(f"     - [{exp.get('score', 0):.2f}] {exp.get('ref_id')}: {exp.get('why')}")
    
    # Demonstrate context injection
    print("\n" + "="*60)
    print("📝 Context Injection Demo:")
    print("="*60)
    
    user_prompt = "O que decidimos sobre a arquitetura de segurança?"
    enriched = await injector.inject(user_prompt)
    print(enriched)
    
    return result


async def check_audit():
    """Check retrieval_audit in CMS."""
    import httpx
    
    cms_url = "http://localhost:8090"
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{cms_url}/tables/events",
            json={"limit": 5, "sort": "created_at DESC"}
        )
        events = response.json()
        
        print("\n📋 Recent Events in CMS:")
        for event in events.get("data", []):
            print(f"   [{event.get('event_type')}] {event.get('justification', '')[:50]}...")


async def main():
    parser = argparse.ArgumentParser(description="CMS Memory Demo")
    parser.add_argument(
        "--action",
        choices=["store", "recall", "audit"],
        default="recall",
        help="Action to perform"
    )
    args = parser.parse_args()
    
    print(f"\n🚀 Antigravity CMS Demo - {datetime.now().isoformat()}")
    print("="*60)
    
    if args.action == "store":
        await store_decision()
    elif args.action == "recall":
        await recall_decision()
    elif args.action == "audit":
        await check_audit()
    
    print("\n✅ Demo complete!")


if __name__ == "__main__":
    asyncio.run(main())
