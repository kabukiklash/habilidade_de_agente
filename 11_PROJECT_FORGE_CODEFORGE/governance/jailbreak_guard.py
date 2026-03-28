import os
import sys

# ID: AG-T11-GOV-001
# PROTOCOLO: JAILBREAK_GUARD

def verify_path_integrity(target_path: str):
    """
    Prevents path traversal attacks by ensuring the agent remains 
    within the allowed workspace for client projects.
    """
    absolute_target = os.path.abspath(target_path)
    allowed_root = os.path.abspath("c:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente/WORKSPACE/PROJETOS")
    
    if not absolute_target.startswith(allowed_root):
        print(f"🚨 [GOVERNANÇA] Tentativa de fuga detectada! Acesso negado a: {absolute_target}")
        sys.exit(1)
    
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1:
        verify_path_integrity(sys.argv[1])
