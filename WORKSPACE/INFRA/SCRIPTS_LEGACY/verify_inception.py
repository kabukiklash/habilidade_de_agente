import asyncio
import sys
import os

# Adiciona o diretório raiz ao sys.path para importar llm_integration
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm_integration import inception_client, InceptionProvider, LLMRequest

async def verify_async_client():
    print("[*] Testando InceptionClient (Async)...")
    try:
        prompt = "Consigo te ouvir? Responda apenas 'SIM' se este teste de fumaça foi bem sucedido."
        response = await inception_client.chat_instant(prompt)
        print(f"[+] Resposta do Mercury-2: {response}")
        return True
    except Exception as e:
        print(f"[-] Erro no InceptionClient: {e}")
        return False

def verify_provider():
    print("\n[*] Testando InceptionProvider (Sync Wrapper)...")
    try:
        provider = InceptionProvider()
        request = LLMRequest(
            prompt="Qual a capital da França?",
            model="mercury-2",
            max_tokens=50
        )
        response = provider.generate(request)
        print(f"[+] Resposta do Provider: {response.text}")
        print(f"[+] Uso de Tokens: {response.usage.total_tokens}")
        return True
    except Exception as e:
        print(f"[-] Erro no InceptionProvider: {e}")
        return False

async def main():
    print("=== ANTIGRAVITY LLM VERIFIER: INCEPTION LABS ===\n")
    
    # Verifica se a chave está configurada
    api_key = os.environ.get("INCEPTION_API_KEY")
    if not api_key:
        print("[-] ERRO: INCEPTION_API_KEY não encontrada no ambiente.")
        print("[!] Certifique-se de que o arquivo .env.inception existe ou a variável está definida.")
        sys.exit(1)
        
    success_async = await verify_async_client()
    success_provider = verify_provider()
    
    if success_async and success_provider:
        print("\n[🎉] INTEGRAÇÃO CERTIFICADA: Inception Labs está operacional!")
    else:
        print("\n[🚫] FALHA NA INTEGRAÇÃO: Verifique os logs e a API Key.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
