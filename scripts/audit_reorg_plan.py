import asyncio
import os
import sys
import json

# Add root directory to sys.path
sys.path.append(os.getcwd())

from llm_integration import consilium

async def audit_reorg():
    plan_path = r"C:\Users\RobsonSilva-AfixGraf\.gemini\antigravity\brain\460d72a8-2989-42ce-82e1-2e5e5665e46d\implementation_plan_reorg.md"
    with open(plan_path, "r", encoding="utf-8") as f:
        plan_content = f.read()

    task = f"""
    ANALISAR RISCOS TÉCNICOS E DE SEGURANÇA DO PLANO DE REORGANIZAÇÃO:
    
    {plan_content}
    
    FOCO:
    1. Importações Python quebradas (sys.path).
    2. Caminhos relativos em scripts (.bat, .ps1, .py).
    3. Localização de arquivos de ambiente (.env).
    4. Quebra de fluxos de CI/CD (GitHub Actions / Sincronização EVO_IA).
    5. Impacto na Soberania do Antigravity (Antigravity Bridge).
    """
    
    # Evidence: critical infrastructure files
    evidence_files = [
        "llm_integration/consilium_engine.py",
        "llm_integration/__init__.py",
        "scripts/test_consilium.py",
        "PROJETOS/NEURO_FLOW_OS/backend/neuro_consilium.py",
        "cognitive-memory-service/ops/expor_cms_cloudflared.bat"
    ]
    
    print("🏛️ [AUDIT] Iniciando Escrutínio do Concílio...")
    try:
        result = await consilium.deliberate(task, evidence_files)
        
        with open("ops/reorg_audit_result.json", "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
            
        print("✅ [AUDIT] Escrutínio concluído.")
    except Exception as e:
        print(f"❌ [AUDIT] Erro: {e}")

if __name__ == "__main__":
    asyncio.run(audit_reorg())
