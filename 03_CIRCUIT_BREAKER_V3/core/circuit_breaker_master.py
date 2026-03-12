import asyncio
import httpx
import time
import os
import sys
from typing import Optional

# Sovereign Path Orchestration
base_dir = "c:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente"
tech_01_client = os.path.join(base_dir, "01_COGNITIVE_MEMORY_SERVICE", "client")
if tech_01_client not in sys.path:
    sys.path.insert(0, tech_01_client)

# Fallback Logger logic
try:
    from .logger import logger
except ImportError:
    class DummyLogger:
        def info(self, m): print(f"[INFO] {m}")
        def error(self, m): print(f"[ERROR] {m}")
        def warning(self, m): print(f"[WARN] {m}")
    logger = DummyLogger()

from cms_client_master import cms_client

class CircuitBreakerV3:
    """
    Escudo Atômico: Gerenciador de Estados Fail-Closed para o Antigravity.
    Estados: CLOSED (Normal), OPEN (Bloqueado), HALF_OPEN (Teste).
    """
    
    def __init__(self, failure_threshold: int = 1, recovery_timeout: int = 30):
        self.state = "CLOSED"
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.last_failure_time: Optional[float] = None
        self.cms_url = "http://localhost:8090/"
        
    def _open_breaker(self, reason: str):
        """Abre o disjuntor e bloqueia fluxos."""
        if self.state != "OPEN":
            self.state = "OPEN"
            self.last_failure_time = time.time()
            logger.error(f"⛔ [Circuit Breaker] ESCUDO ATIVADO! Estado: OPEN. Motivo: {reason}")
            # Hook para o Dashboard via CMS
            asyncio.create_task(self._report_to_cms(reason))

    async def _report_to_cms(self, reason: str):
        """Notifica o CMS sobre a ativação do escudo para visualização no HUD."""
        try:
            await cms_client.append_event(
                event_type="SYSTEM_ALERT_BREAKER",
                actor="CIRCUIT_BREAKER_V3",
                payload={"reason": reason, "state": "OPEN"},
                justification="Ativação automática do Circuit Breaker V3 devido a falha de infraestrutura."
            )
        except Exception as e:
            logger.warning(f"⚠️ [Breaker] Falha ao reportar alerta ao CMS: {e}")

    async def verify_safety(self) -> bool:
        """
        Verifica se é seguro prosseguir com a chamada LLM.
        Retorna True se o sistema estiver saudável, False se estiver bloqueado.
        """
        
        # 1. Se estiver OPEN, verifica se já passou o tempo de recuperação
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "HALF_OPEN"
                logger.info("🟡 [Circuit Breaker] Estado: HALF-OPEN. Tentando teste de pulso...")
            else:
                return False

        # 2. Executa Smart Ping de saúde
        try:
            async with httpx.AsyncClient() as client:
                # Ping com timeout curto
                response = await client.get(self.cms_url, timeout=2.0)
                
                if response.status_code == 429:
                    self._open_breaker("CMS bloqueou requisições (Rate Limit 429).")
                    return False
                
                if response.status_code == 401 or response.status_code == 403:
                    self._open_breaker("Violação Zero-Trust detectada (Auth Error).")
                    return False

                # Se chegamos aqui e estávamos em HALF-OPEN ou CLOSED, resetamos
                if self.state in ["HALF_OPEN", "OPEN"]:
                    logger.info("🟢 [Circuit Breaker] Restauração detectada. Estado: CLOSED.")
                
                self.state = "CLOSED"
                self.failure_count = 0
                return True

        except (httpx.ConnectError, httpx.TimeoutException, Exception) as e:
            self.failure_count += 1
            reason = f"Falha de conexão com a infraestrutura: {str(e)}"
            
            if self.failure_count >= self.failure_threshold:
                self._open_breaker(reason)
            
            return False

# Global Instance
circuit_breaker = CircuitBreakerV3()
