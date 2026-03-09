    # import asyncio
    # import sys
    # import os

    # # 1. Mapeia o caminho exato para a sua infraestrutura soberana
    # caminho_infra = os.path.join(os.getcwd(), "EVOLUTION_SOVEREIGN_TEMPLATE", "02_SOVEREIGN_INFRA")
    # sys.path.append(caminho_infra)

    # print("⏳ Carregando o Córtex Cognitivo...")

    # try:
    #     from llm_integration.cognitive_cortex import cognitive_cortex
    # except ModuleNotFoundError as e:
    #     print(f"❌ Erro de importação: Não consegui achar os módulos do Evolution. Caminho buscado: {caminho_infra}")
    #     print(f"Detalhe do erro: {e}")
    #     sys.exit(1)

    # async def run_test():
    #     print("========================================")
    #     print("🛡️ INICIANDO TESTE DO DISJUNTOR (FAIL-CLOSED)")
    #     print("========================================")
        
    #     # Mandamos uma tarefa simulando o Cursor pedindo ajuda
    #     resultado = await cognitive_cortex.solve_task("Escreva um script Python de automação simples.")
        
    #     print("\n========================================")
    #     print("📋 RESULTADO DEVOLVIDO PELA FUNÇÃO:")
    #     print("========================================")
    #     print(resultado)

    # if __name__ == "__main__":
    #     asyncio.run(run_test())

import asyncio
import sys
import os

# 1. Mapeia o caminho exato para a sua infraestrutura soberana
caminho_infra = os.path.join(os.getcwd(), "EVOLUTION_SOVEREIGN_TEMPLATE", "02_SOVEREIGN_INFRA")
sys.path.append(caminho_infra)

print("⏳ Carregando o Córtex Cognitivo...")

try:
    from llm_integration.cognitive_cortex import cognitive_cortex
except ModuleNotFoundError as e:
    print(f"❌ Erro de importação: Não consegui achar os módulos do Evolution. Caminho buscado: {caminho_infra}")
    print(f"Detalhe do erro: {e}")
    sys.exit(1)

async def run_test():
    print("========================================")
    print("🛡️ INICIANDO TESTE DO DISJUNTOR (FAIL-CLOSED)")
    print("========================================")
    
    # Mandamos uma tarefa simulando o Cursor pedindo ajuda
    resultado = await cognitive_cortex.solve_task("Escreva um script Python de automação simples.")
    
    print("\n========================================")
    print("📋 RESULTADO DEVOLVIDO PELA FUNÇÃO:")
    print("========================================")
    print(resultado)

if __name__ == "__main__":
    asyncio.run(run_test())