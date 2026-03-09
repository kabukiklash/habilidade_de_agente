import asyncio
import os
import sys

# Add root directory to sys.path
sys.path.append(os.getcwd())

from llm_integration import openai_client, openai_provider
from llm_integration.models import LLMRequest

async def verify():
    print("=== ANTIGRAVITY LLM VERIFIER: OPENAI ===")
    
    # Test OpenAIClient (Async)
    print("[*] Testando OpenAIClient (Async)...")
    try:
        response = await openai_client.chat_instant("Respond only with 'OK' if you can read this.")
        print(f"[+] Resposta do OpenAI: {response}")
    except Exception as e:
        print(f"[!] Erro no Client: {e}")
        return

    # Test OpenAIProvider (Sync Wrapper)
    print("\n[*] Testando OpenAIProvider (Sync Wrapper)...")
    try:
        req = LLMRequest(prompt="Qual é a capital do Japão? Responda em uma frase.")
        res = openai_provider.generate(req)
        print(f"[+] Resposta do Provider: {res.text}")
        print(f"[+] Provedor Identificado: {res.provider}")
    except Exception as e:
        print(f"[!] Erro no Provider: {e}")

if __name__ == "__main__":
    asyncio.run(verify())
