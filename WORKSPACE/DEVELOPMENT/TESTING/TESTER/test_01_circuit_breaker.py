import asyncio
import sys
import os

# Ajuste do path para encontrar a infraestrutura soberana a partir da pasta TESTER
raiz = os.path.abspath(os.path.join(os.getcwd(), ".."))
if not os.path.exists(os.path.join(raiz, "EVOLUTION_SOVEREIGN_TEMPLATE")):
    # Caso o script seja rodado da raiz do projeto
    raiz = os.getcwd()

caminho_infra = os.path.join(raiz, "EVOLUTION_SOVEREIGN_TEMPLATE", "02_SOVEREIGN_INFRA")
sys.path.insert(0, caminho_infra)
sys.path.insert(0, raiz)

print("[INFO] Carregando o Córtex Cognitivo Soberano...")
try:
    from llm_integration.cognitive_cortex import cognitive_cortex
except ImportError as e:
    print(f"[ERROR] Falha ao carregar Córtex: {e}")
    sys.exit(1)

async def run_test():
    print("----------------------------------------")
    print("🛡️ SENSOR 01: CIRCUIT BREAKER (FAIL-CLOSED)")
    print("----------------------------------------")
    
    # O teste é bem-sucedido se:
    # 1. O CMS estiver online e responder (Sucesso Nominal)
    # 2. O CMS estiver offline e o Córtex ABORTAR (Sucesso de Segurança)
    
    print("Executando chamada de teste via Córtex...")
    resultado = await cognitive_cortex.solve_task("Teste de integridade do sensor de observabilidade.")
    
    print("\n[RESULTADO DO SENSOR]:")
    if "Circuit Breaker" in resultado:
        print("✅ STATUS: SEGURO (Fail-Closed Ativo)")
    elif "ERROR" in resultado:
        print(f"❌ STATUS: FALHA CRÍTICA ({resultado})")
    else:
        print("✅ STATUS: OPERACIONAL (Conexão Nominal)")
    
    print("----------------------------------------")

if __name__ == "__main__":
    asyncio.run(run_test())
