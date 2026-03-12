import asyncio
import os
import sys

# Add root directory to sys.path
sys.path.append(os.getcwd())

from llm_integration import consilium

async def deliberate_neuro_flow():
    task = """
    PROJETAR E IMPLEMENTAR O "NEURO-FLOW OS"
    Requisitos:
    - Ledger com tabelas: NeuralTask, BrainState, FlowSession.
    - Algoritmos: FocusScorer e PriorityMatrix.
    - Segurança: Bio-JWT e E2EE para BrainState.
    - Interface: Dashboard de Calor Cerebral e Grafo de Tarefas (React Flow).
    - Modos: Deep Work e Burnout Recovery.
    """
    
    # PER Context: Most relevant files for architecture
    evidence_files = [
        "llm_integration/models.py", 
        "llm_integration/consilium_engine.py",
        "GEMINI.md"
    ]
    
    print("🧠 [SAGA] Iniciando Deliberação do Concílio para o NEURO-FLOW OS...")
    try:
        result = await consilium.deliberate(task, evidence_files)
        
        # Save results to a file for the next step
        with open("ops/neuro_flow_deliberation.json", "w", encoding="utf-8") as f:
            import json
            json.dump(result, f, indent=2)
            
        print("✅ [SAGA] Veredito Soberano obtido e salvo em ops/neuro_flow_deliberation.json")
    except Exception as e:
        print(f"❌ [SAGA] Erro na deliberação: {e}")

if __name__ == "__main__":
    asyncio.run(deliberate_neuro_flow())
