import hashlib
import os
import sys
from typing import Dict, List, Optional, Any

# Sovereign Path Orchestration
base_dir = "c:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente"
tech_07_adapter = os.path.join(base_dir, "07_KIMI_MEMORY_BRIDGE", "adapter")
if tech_07_adapter not in sys.path:
    sys.path.insert(0, tech_07_adapter)

# Fallback Logger logic
try:
    from .logger import logger
except ImportError:
    class DummyLogger:
        def info(self, m): print(f"[INFO] {m}")
        def error(self, m): print(f"[ERROR] {m}")
        def warning(self, m): print(f"[WARN] {m}")
    logger = DummyLogger()

class VibeValidator:
    """
    Motor de Integridade VibeCode G7.
    Verifica se arquivos críticos foram alterados sem autorização.
    """
    
    def __init__(self, critical_files: Optional[List[str]] = None):
        self.critical_files = critical_files or [
            "02_COGNITIVE_CORTEX/core/cognitive_cortex_master.py",
            "03_CIRCUIT_BREAKER_V3/circuit_breaker_master.py",
            "03_CIRCUIT_BREAKER_V3/policy_engine_master.py",
            "06_AUDIT_MONITOR_LEDGER/audit_monitor_master.py"
        ]
        self.base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def calculate_hash(self, file_rel_path: str) -> str:
        """Calcula o SHA-256 de um arquivo."""
        abs_path = os.path.join(self.base_path, file_rel_path)
        if not os.path.exists(abs_path):
            return "FILE_NOT_FOUND"
        
        sha256_hash = hashlib.sha256()
        with open(abs_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    async def verify_integrity(self) -> Dict[str, Any]:
        """
        Verifica a integridade de todos os arquivos críticos contra o Ledger via MemoryAdapter.
        """
        from memory_adapter_master import memory_adapter
        
        report = {"status": "GREEN", "details": []}
        
        for rel_path in self.critical_files:
            current_hash = self.calculate_hash(rel_path)
            
            # Busca a assinatura recente no CMS/Ledger
            # Usamos uma query específica que deve ser indexada pelo CMS
            search_query = f"VIBE_SIGNATURE for {rel_path}"
            search_result = await memory_adapter.query_memory(search_query, vector_topk=10)
            
            # Filtra os fatos para encontrar o evento exato de assinatura
            facts = search_result.get("context", {}).get("facts", [])
            signed_hash = None
            
            for fact in facts:
                if rel_path.lower() in fact.replace("\\", "/").lower() and "hash" in fact:
                    # Tenta extrair o hash (Flexível para JSON ou texto plano)
                    import re
                    match = re.search(r'["\']?hash["\']?\s*:\s*["\']?([a-f0-9]{64})["\']?', fact)
                    if match:
                        signed_hash = match.group(1)
                        break

            if not signed_hash:
                # Fallback: Se não encontrou via busca semântica, tenta direto no Ledger se possível
                # ou reporta como não assinado (Baseline necessária)
                report["status"] = "YELLOW"
                report["details"].append({
                    "file": rel_path,
                    "status": "UNSIGNED",
                    "msg": "Sem assinatura válida encontrada na Memória Cognitiva."
                })
                continue
                
            if current_hash != signed_hash:
                report["status"] = "RED"
                report["details"].append({
                    "file": rel_path,
                    "status": "DRIFT_DETECTED",
                    "msg": f"HASH MISMATCH! Atual: {current_hash[:8]}... vs Assinado: {signed_hash[:8]}..."
                })
            else:
                report["details"].append({
                    "file": rel_path,
                    "status": "VALID",
                    "msg": "Integridade G7 confirmada."
                })

        return report

vibe_validator = VibeValidator()
