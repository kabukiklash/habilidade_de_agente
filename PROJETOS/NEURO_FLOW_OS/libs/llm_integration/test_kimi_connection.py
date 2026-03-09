import asyncio
import os
import sys

# Ensure the parent directory is in the path so we can import llm_integration
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from llm_integration.kimi_client import KimiClient

async def test_connectivity():
    print("📡 Testing Moonshot AI Connectivity...")
    try:
        client = KimiClient()
        models = await client.list_models()
        print(f"✅ Connection Successful! Found {len(models)} models.")
        
        # Filter for k2.5 or latest models
        relevant_models = [m["id"] for m in models if "kimi" in m["id"] or "moonshot" in m["id"]]
        print("📋 Relevant Models:")
        for m_id in relevant_models[:10]:
            print(f"  - {m_id}")
            
        # Optional: Quick chat test (Instant Mode)
        print("\n💬 Testing Instant Mode...")
        response = await client.chat_instant("Olá Kimi! Você está pronto para ser o cérebro do Antigravity?")
        print(f"🤖 Kimi: {response}")
        
    except Exception as e:
        print(f"❌ Error during connectivity test: {e}")

if __name__ == "__main__":
    asyncio.run(test_connectivity())
