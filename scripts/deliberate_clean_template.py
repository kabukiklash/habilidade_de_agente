import asyncio
import os
import sys
import json

# Add root directory to sys.path
sys.path.append(os.getcwd())

from llm_integration import consilium

async def deliberate_reorg_strategy():
    task = """
    ESCRUTÍNIO DE ESTRATÉGIA: "Criação de Repositório Template Limpo" vs "Reorganização do Repositório Vivo".
    
    CONCEITO:
    Em vez de mover os arquivos no repositório atual (Habilidade de Agente), que contém lixo legado e caminhos frágeis, 
    devemos criar um 'SOVEREIGN_TEMPLATE' (O Gabarito) com a estrutura [00-04] purificada. 
    O repositório atual ficaria como 'Legacy/Dev' e o novo seria o padrão 'Gold' para novas instalações.
    
    SUBMETIDO AO ESCRUTÍNIO COM O COMANDO "A SAGA":
    1. Análise de ROI: Esforço de re-instalação vs risco de quebra no vivo.
    2. Risco de Drift: Manter duas versões (Legada vs Template) causará dessincronização de conhecimento?
    3. Distribuição Nômade: Como isso acelera a clonagem do Antigravity em novos ambientes?
    4. Veredito: É melhor limpar o ninho ou construir uma nova casa?
    """
    
    # Evidence: current reorg plan and recent build artifacts
    evidence_files = [
        "PROJETOS/NEURO_FLOW_OS/README.md",
        "llm_integration/consilium_engine.py",
        "NEURO_FLOW_Requirements_Ledger.md"
    ]
    
    print("🏛️ [SAGA] O Concílio está sendo convocado para decidir o destino do Repositório...")
    try:
        result = await consilium.deliberate(task, evidence_files)
        
        with open("ops/strategy_deliberation.json", "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
            
        print("✅ [SAGA] Veredito registrado no Ledger.")
    except Exception as e:
        print(f"❌ [SAGA] Erro na deliberação: {e}")

if __name__ == "__main__":
    asyncio.run(deliberate_reorg_strategy())
