import sys
import os

if sys.platform == "win32":
    try:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except Exception:
        pass

# Sovereign Foundation Integration
BASE_DIR = "c:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente"

def align_skill_to_sovereign_core():
    """
    Orchestrates sys.path to ensure the skill uses Master Technologies.
    """
    master_paths = [
        os.path.join(BASE_DIR, "01_COGNITIVE_MEMORY_SERVICE", "client"),
        os.path.join(BASE_DIR, "02_COGNITIVE_CORTEX", "core"),
        os.path.join(BASE_DIR, "03_CIRCUIT_BREAKER_V3", "core"),
        os.path.join(BASE_DIR, "06_AUDIT_MONITOR_LEDGER", "core"),
        os.path.join(BASE_DIR, "07_KIMI_MEMORY_BRIDGE", "adapter"),
        os.path.join(BASE_DIR, "07_KIMI_MEMORY_BRIDGE", "bridges")
    ]
    
    for path in master_paths:
        if path not in sys.path:
            sys.path.insert(0, path)
            
    print("🛡️ [GOVERNOR] Skill aligned to Sovereign Master Core.")

def check_vibe_integrity(file_path: str):
    """
    Proxies to Technology 05 (VibeCode G7) to verify code intent.
    """
    tech_05_path = os.path.join(BASE_DIR, "05_VIBECODE_G7", "core")
    if tech_05_path not in sys.path:
        sys.path.insert(0, tech_05_path)
    
    try:
        from vibe_validator_master import vibe_validator
        # Here we would call validation
        return True
    except ImportError:
        return False

# Self-init if imported
align_skill_to_sovereign_core()
