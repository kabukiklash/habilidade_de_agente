import asyncio
import sys
import os

# Ajuste do path para encontrar a infraestrutura soberana
raiz = os.path.abspath(os.path.join(os.getcwd(), ".."))
if not os.path.exists(os.path.join(raiz, "EVOLUTION_SOVEREIGN_TEMPLATE")):
    raiz = os.getcwd()

caminho_infra = os.path.join(raiz, "EVOLUTION_SOVEREIGN_TEMPLATE", "02_SOVEREIGN_INFRA")
sys.path.insert(0, caminho_infra)
sys.path.insert(0, raiz)

print("[INFO] Carregando o Neuro Consilium...")
try:
    from llm_integration.consilium_engine import consilium
except ImportError as e:
    print(f"[ERROR] Falha ao carregar Consilium: {e}")
    sys.exit(1)

async def run_smoke_test():
    print("----------------------------------------")
    print("🗳️ SENSOR 02: NEURO CONSILIUM (SMOKE TEST)")
    print("----------------------------------------")
    
    tarefa = "Ping de observabilidade: O conselho está operacional?"
    
    # Usamos uma tarefa trivial e sem arquivos para minimizar consumo
    print(f"Enviando deliberação ultra-rápida...")
    try:
        resultado = await consilium.deliberate(tarefa, [])
        
        veredito = resultado.get("verdict", "")
        if veredito and "ERROR" not in veredito:
            print(f"✅ STATUS: OPERACIONAL")
            print(f"Veredito Final consolidado por: {resultado.get('council_opinions', {}).keys()}")
        else:
            print(f"❌ STATUS: FALHA NA DELIBERAÇÃO")
            print(f"Erro: {veredito}")
            
    except Exception as e:
        print(f"❌ STATUS: ERRO DE EXECUÇÃO ({e})")
    
    print("----------------------------------------")

if __name__ == "__main__":
    asyncio.run(run_smoke_test())
