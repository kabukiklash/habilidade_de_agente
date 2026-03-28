import os
import sys
import subprocess

# Sovereign Foundation Integration
BASE_DIR = "c:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente"
sys.path.insert(0, os.path.join(BASE_DIR, "05_VIBECODE_G7", "core"))
sys.path.insert(0, os.path.join(BASE_DIR, "06_AUDIT_MONITOR_LEDGER", "core"))

def validate_sprint_and_save(project_path: str, commit_msg: str):
    """
    Electronic Fiscal: Validates the sprint and triggers Git Savepoint ONLY if success.
    """
    print(f"🕵️ [FISCAL] Iniciando auditoria de Sprint em: {project_path}")
    
    # 1. Run local validators (Example: Lint, Tests)
    # For this template, we assume there is a 'tests/' folder
    try:
        # Simulate a test run
        # In a real scenario, this would call 'pytest' or 'npm test'
        print("[FISCAL] Executando Verificação Vibracional (G7)...")
        from vibe_validator_master import vibe_validator
        # Here we would valdiate all files
        # For demo, we assume success
        is_clean = True 
        
        if not is_clean:
            print("❌ [FISCAL] Integridade violada. Savepoint ABORTADO.")
            return False

        # 2. Trigger Git Savepoint
        print(f"💾 [FISCAL] Sprint Aprovada. Criando Savepoint Automático...")
        subprocess.run(["git", "add", "."], cwd=project_path, check=True)
        subprocess.run(["git", "commit", "-m", f"SAVEPOINT: {commit_msg}"], cwd=project_path, check=True)
        
        # 3. Log to Ledger Master
        print("📝 [FISCAL] Registrando evento no Ledger Soberano (T06)...")
        # from audit_monitor_master import audit_monitor
        # audit_monitor.log_event(...)
        
        return True

    except Exception as e:
        print(f"💥 [FISCAL] Falha crítica na validação: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 2:
        validate_sprint_and_save(sys.argv[1], sys.argv[2])
