import os
import sys
import shutil
import datetime
import subprocess

# Sovereign Foundation Integration
BASE_DIR = "c:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente"
T11_DIR = os.path.join(BASE_DIR, "11_PROJECT_FORGE_CODEFORGE")

def create_client_project(client_name: str, project_name: str):
    """
    Orchestrates the creation of a new client project using Clean Architecture.
    """
    client_code = client_name.upper()[:3]
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M")
    project_id = f"CP-{client_code}-{timestamp}"
    
    target_dir = os.path.join(BASE_DIR, "WORKSPACE", "PROJETOS", project_name)
    template_dir = os.path.join(T11_DIR, "templates", "CODEFORGE_v1")
    
    print(f"🏗️ [FORGE] Gerando projeto: {project_name} ({project_id})")
    
    if os.path.exists(target_dir):
        print(f"❌ [ERRO] O diretório {target_dir} já existe.")
        return
        
    # 1. Clone Template
    shutil.copytree(template_dir, target_dir)
    
    # 2. Inject Manifest & ID Lineage
    manifest_path = os.path.join(target_dir, "manifest", "SOVEREIGN_MANIFEST.md")
    os.makedirs(os.path.dirname(manifest_path), exist_ok=True)
    
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write(f"# MANIFESTO DE SOBERANIA: {project_name}\n")
        f.write(f"ID: {project_id}\n")
        f.write(f"DATA_CRIACAO: {datetime.datetime.now().isoformat()}\n")
        f.write("ORIGEM: Antigravity Project Forge T11\n")
        f.write("STATUS: PROTECTED BY CODEFORGE GOVERNANCE\n")

    # 3. Provision Satellites (Lite Versions)
    provision_satellites(target_dir)
    
    print(f"✅ [FORGE] Projeto {project_name} criado em WORKSPACE/PROJETOS/")

def provision_satellites(target_dir: str):
    """
    Copies lite versions of sovereign tech to the project's satellite folder.
    """
    satellite_path = os.path.join(target_dir, "satellites")
    os.makedirs(satellite_path, exist_ok=True)
    
    # Example: Audit Lite
    with open(os.path.join(satellite_path, "audit_lite.py"), "w") as f:
        f.write("# ID: CP-AUDIT-LITE\n# Proxy to Ledger Manager (T06)\n")
        
    print("🛡️ [FORGE] Satélites provisionados com sucesso.")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        create_client_project(sys.argv[1], sys.argv[2])
    else:
        print("Uso: python project_generator.py <CLIENT_NAME> <PROJECT_NAME>")
