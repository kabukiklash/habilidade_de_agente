import asyncio
import hashlib
import json
from typing import Dict, Any, List, Optional
from antigravity_memory_backend.memory_adapter import memory_adapter

class KimiAuditMonitor:
    """
    Monitor de Auditoria Forense para o Kimi.
    Rastreia intenções, detecta desvios e gera relatórios de conformidade.
    """
    
    def __init__(self):
        self.actor = "AUDIT_MONITOR"

    def _generate_integrity_hash(self, payload: Dict[str, Any]) -> str:
        """Gera um hash SHA-256 para garantir a integridade do log."""
        data_str = json.dumps(payload, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()

    async def log_decision_with_intent(
        self, 
        intent_id: str, 
        decision_payload: Dict[str, Any], 
        justification: str,
        tokens_used: int = 0,
        tokens_saved: int = 0
    ):
        """
        Vincula uma decisão do Kimi a uma intenção original do usuário.
        Adds an integrity hash for forensic verification.
        """
        integrity_hash = self._generate_integrity_hash(decision_payload)
        
        audit_payload = {
            "intent_id": intent_id,
            "decision": decision_payload,
            "integrity_hash": integrity_hash,
            "audit_timestamp": asyncio.get_event_loop().time()
        }
        
        await memory_adapter.append_event(
            event_type="KIMI_AUDIT_LOG",
            payload=audit_payload,
            justification=f"Auditoria vinculada à intenção {intent_id}: {justification}",
            correlation_id=intent_id,
            tokens_used=tokens_used,
            tokens_saved=tokens_saved
        )
        print(f"🛡️ [Audit] Decision logged and hashed for intent: {intent_id}")

    async def check_drift(self, intent_id: str, current_solution: str) -> bool:
        """
        Verifica se a solução atual do Kimi desvia drasticamente da intenção original.
        (Implementação simplificada: busca por palavras-chave proibidas ou desvios de escopo)
        """
        # Exemplo: Se a intenção era "Analisar" e a solução contém "Deletar" ou "Modificar Infra"
        prohibited_actions = ["delete", "rm -rf", "shutdown", "format"]
        
        solution_lower = current_solution.lower()
        for forbidden in prohibited_actions:
            if forbidden in solution_lower:
                print(f"⚠️ [ALERT] DRIFT DETECTED! Forbidden action found in Kimi solution.")
                return True
        return False

    async def get_kimi_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Recupera o histórico recente de auditoria do Kimi."""
        # Consulta o CMS por eventos do tipo KIMI_AUDIT_LOG
        result = await memory_adapter.query_memory("KIMI_AUDIT_LOG history", vector_topk=limit)
        return result.get("context", {}).get("facts", [])

audit_monitor = KimiAuditMonitor()
