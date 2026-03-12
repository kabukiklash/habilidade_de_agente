import asyncio
import os
import sys
import json

# Add root directory to sys.path
sys.path.append(os.getcwd())

from llm_integration import consilium

async def final_scrutiny():
    task = """
    ESCRUTÍNIO FINAL: DETECÇÃO DE BRECHAS NO PROTOCOLO MILITAR (MIP) EM AMBIENTE WINDOWS.
    
    CONTEXTO:
    O plano MIP foi atualizado com Independência de Auditoria e Assinaturas Ed25519. 
    Agora, precisamos detectar 'Brechas Técnicas' específicas de implementação:
    1. Bloqueio de Arquivos: Como lidar com arquivos presos por processos ativos (main.py, dev servers)?
    2. Isolamento de Credenciais: O script de cópia pode ignorar .env, mas e se as credenciais estiverem no Registry ou User Profile?
    3. Merkle Root: O cálculo do hash em Windows pode divergir em Linux (Line Endings CRLF vs LF). Como garantir o Gold Standard Cross-Platform?
    4. Rollback: Um script PowerShell é suficiente para garantir idempotência total?
    
    A SAGA:
    Analisar a 'Cozinha da Implementação' para garantir que não haja falhas no dia do Deploy.
    """
    
    evidence_files = [
        "C:\\Users\\RobsonSilva-AfixGraf\\.gemini\\antigravity\\brain\\460d72a8-2989-42ce-82e1-2e5e5665e46d\\implementation_plan_mip.md",
        "scripts/sovereign_audit.py"
    ]
    
    print("🏛️ [SAGA] Invoquei o Concílio para a varredura final de brechas...")
    try:
        result = await consilium.deliberate(task, evidence_files)
        
        with open("ops/final_scrutiny_result.json", "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
            
        print("✅ [SAGA] Varredura final concluída.")
    except Exception as e:
        print(f"❌ [SAGA] Erro: {e}")

if __name__ == "__main__":
    asyncio.run(final_scrutiny())
