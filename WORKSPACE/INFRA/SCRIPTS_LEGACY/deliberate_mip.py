import asyncio
import os
import sys
import json

# Add root directory to sys.path
sys.path.append(os.getcwd())

from llm_integration import consilium

async def deliberate_mip():
    task = """
    ESCRUTÍNIO DO PROTOCOLO MILITAR DE INSTALAÇÃO (MIP).
    
    CONCEITO:
    Criar um processo de 'Checkpoint de Linha de Chegada' pós-instalação. 
    O sistema deve gerar um Sovereign Audit Report (SAR) que mapeia:
    1. Integridade da Topologia [00-04].
    2. Ausência de 'Slag' (lixo legado/credenciais).
    3. Conformidade com ISO 27002 (Controle 8.19).
    
    A SAGA:
    1. É seguro delegar a auditoria ao próprio sistema instalado ou deve ser um agente externo?
    2. Como o relatório gerado deve ser formatado para ser 'impossível de falsificar' sem o GPG?
    3. O protocolo atende aos requisitos de 'Defesa em Profundidade'?
    4. Veredito: O protocolo militar é soberano ou apenas burocrático?
    """
    
    # Evidence: MIP implementation plan and Sovereign Audit script
    evidence_files = [
        "scripts/sovereign_audit.py",
        "C:\\Users\\RobsonSilva-AfixGraf\\.gemini\\antigravity\\brain\\460d72a8-2989-42ce-82e1-2e5e5665e46d\\implementation_plan_mip.md"
    ]
    
    print("🏛️ [SAGA] Invoquei o Concílio para auditar o Protocolo Militar...")
    try:
        result = await consilium.deliberate(task, evidence_files)
        
        with open("ops/mip_deliberation.json", "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
            
        print("✅ [SAGA] O Protocolo Militar foi escrutinado.")
    except Exception as e:
        print(f"❌ [SAGA] Erro: {e}")

if __name__ == "__main__":
    asyncio.run(deliberate_mip())
