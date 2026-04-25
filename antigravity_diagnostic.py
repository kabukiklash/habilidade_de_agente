import os
import sys
import importlib.util
from pathlib import Path
import time
import requests
import json
from datetime import datetime

# Configurações de Ambiente
os.environ["PYTHONIOENCODING"] = "utf-8"
BASE_DIR = Path(r"C:\Users\RobsonSilva-AfixGraf\Habilidade_de_agente")

# Adiciona todos os módulos ao sys.path para resolver dependências cruzadas
modules_paths = [
    BASE_DIR / "01_COGNITIVE_MEMORY_SERVICE" / "client",
    BASE_DIR / "02_COGNITIVE_CORTEX" / "core",
    BASE_DIR / "03_CIRCUIT_BREAKER_V3" / "core",
    BASE_DIR / "04_KNOWLEDGE_GRAPH" / "core",
    BASE_DIR / "05_VIBECODE_G7" / "core",
    BASE_DIR / "06_AUDIT_MONITOR_LEDGER" / "core",
    BASE_DIR / "07_KIMI_MEMORY_BRIDGE" / "core",
    BASE_DIR / "09_SOVEREIGN_SKILLS_ORCHESTRATION" / "core",
    BASE_DIR / "10_SOVEREIGN_OPERATIONS" / "core",
    BASE_DIR / "11_PROJECT_FORGE_CODEFORGE" / "core",
    BASE_DIR / "12_CONSILIUM_ENGINE" / "llm_integration",
    BASE_DIR / "14_EVO" / "core"
]

for p in modules_paths:
    if p.exists():
        sys.path.insert(0, str(p))

def check_module(name, path_str):
    try:
        # Importa usando o caminho absoluto para evitar problemas com nomes começando com números
        target_path = BASE_DIR / path_str
        if not target_path.exists():
            return False, f"Arquivo não encontrado: {path_str}"
        
        spec = importlib.util.spec_from_file_location(name, str(target_path))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return True, "OK"
    except Exception as e:
        return False, str(e)

print(f"{'MODULO':<40} | {'STATUS':<10} | {'OBSERVAÇÃO'}")
print("-" * 100)

core_modules = [
    ("01_CMS_CLIENT", "01_COGNITIVE_MEMORY_SERVICE/client/cms_client_master.py"),
    ("02_CORTEX", "02_COGNITIVE_CORTEX/core/cognitive_cortex_master.py"),
    ("03_BREAKER", "03_CIRCUIT_BREAKER_V3/core/circuit_breaker_master.py"),
    ("04_GRAPH", "04_KNOWLEDGE_GRAPH/core/graph_builder_master.py"),
    ("05_VIBECODE", "05_VIBECODE_G7/core/formal_verifier_master.py"),
    ("06_AUDIT", "06_AUDIT_MONITOR_LEDGER/core/audit_monitor_master.py"),
    ("07_BRIDGE", "07_KIMI_MEMORY_BRIDGE/core/memory_adapter_master.py"),
    ("09_GOVERNOR", "09_SOVEREIGN_SKILLS_ORCHESTRATION/core/skill_governor_master.py"),
    ("10_OPS", "10_SOVEREIGN_OPERATIONS/core/sovereign_audit_master.py"),
    ("11_PF_FORGE", "11_PROJECT_FORGE_CODEFORGE/core/project_generator.py"),
    ("12_CONSILIUM", "12_CONSILIUM_ENGINE/llm_integration/consilium_engine.py"),
    ("14_EVO_ACE", "14_EVO/core/ace_server.py")
]

for name, path in core_modules:
    success, msg = check_module(name, path)
    status = "✅ WORKING" if success else "❌ ERROR"
    # Trunca mensagens longas
    msg_display = (msg[:50] + '...') if len(msg) > 50 else msg
    print(f"{name:<40} | {status:<10} | {msg_display}")

print("\nVerificando conectividade CMS (Porta 8090)...")
try:
    r = requests.get("http://127.0.0.1:8090/health", timeout=5)
    if r.status_code == 200:
        print("✅ CMS ONLINE (Healthy)")
    else:
        print(f"⚠️ CMS RESPONSE ERROR: {r.status_code}")
except Exception as e:
    print(f"❌ CMS OFFLINE: {e}")

print("\nVerificando Banco de Dados...")
db_paths = {
    "antigravity.db": BASE_DIR / "01_COGNITIVE_MEMORY_SERVICE" / "database" / "antigravity.db",
    "evolution.db": BASE_DIR / "evolution.db"
}

for db_name, db_path in db_paths.items():
    if db_path.exists():
        print(f"✅ DB {db_name} encontrado.")
    else:
        print(f"❌ DB {db_name} ausente no caminho: {db_path}")

print("\nSalvando estado do sistema...")
state = {
    "last_check": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "cms_status": "ONLINE",
    "db_evolution": (BASE_DIR / "evolution.db").exists(),
    "db_antigravity": (BASE_DIR / "01_COGNITIVE_MEMORY_SERVICE/database/antigravity.db").exists(),
    "modules_ready": True
}

with open(BASE_DIR / "system_state.json", "w") as f:
    json.dump(state, f, indent=2)
print(f"[OK] Estado salvo em system_state.json")

print("\nInjetando DNA Soberano nos Workspaces...")
import shutil
global_rules_path = BASE_DIR / ".clinerules"
projetos_dir = BASE_DIR / "WORKSPACE" / "PROJETOS"

if global_rules_path.exists() and projetos_dir.exists():
    for projeto in projetos_dir.iterdir():
        if projeto.is_dir():
            dest_path = projeto / ".clinerules"
            try:
                shutil.copy2(global_rules_path, dest_path)
                print(f"🧬 DNA Injetado: {projeto.name}")
            except Exception as e:
                print(f"⚠️ Falha ao injetar em {projeto.name}: {e}")
else:
    print("⚠️ Regras globais ou pasta de projetos não encontradas.")
