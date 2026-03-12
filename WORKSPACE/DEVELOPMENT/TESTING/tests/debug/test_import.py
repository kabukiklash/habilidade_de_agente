import os
import sys

# Simular ambiente de teste
base_dir = "c:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente"
sys.path.append(base_dir)
sys.path.append(os.path.join(base_dir, "EVOLUTION_SOVEREIGN_TEMPLATE", "02_SOVEREIGN_INFRA"))

print("--- Tentando importar MemoryAdapter ---")
try:
    from antigravity_memory_backend.memory_adapter import memory_adapter, SQLITE_AVAILABLE
    print(f"Sucesso! Mode={memory_adapter.mode}, SQLITE_AVAIL={SQLITE_AVAILABLE}")
except Exception as e:
    print(f"Erro na importação: {e}")
    import traceback
    traceback.print_exc()
