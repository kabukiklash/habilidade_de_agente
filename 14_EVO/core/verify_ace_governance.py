import sys
import os
import time
import asyncio
import json

# Setup paths
base_dir = "c:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente"
ace_dir = os.path.join(base_dir, "14_EVO", "core")
sys.path.insert(0, ace_dir)
sys.path.insert(0, os.path.join(base_dir, "03_CIRCUIT_BREAKER_V3", "core"))

from loop_guard_master import loop_guard
from circuit_breaker_master import circuit_breaker
from ace_memory_gateway import MemoryGateway

# Mock CMS for testing (to avoid network dependency in verification)
class MockResponse:
    def __init__(self, status_code, text=""):
        self.status_code = status_code
        self.text = text

import requests
from unittest.mock import patch

@patch('requests.post')
def test_governance_suite(mock_post):
    mock_post.return_value = MockResponse(201, "Created")
    
    print("🧪 [TEST] Iniciando Suite de Verificação de Governança ACE v2.0\n")
    
    # 1. Test Loop Guard: Source Filter
    print("1. Verificando Source Guard (Auto-Trigger Prevention)...")
    should_process = loop_guard.should_process_event("test.md", origin="ace")
    assert should_process is False, "ERRO: ACE processou evento com origem 'ace'!"
    print("✅ Source Guard: Bloqueou evento de origem recursiva.")
    
    # 2. Test Watcher Guard: Ignored Patterns
    print("2. Verificando Watcher Guard (Ignored Files)...")
    should_process = loop_guard.should_process_event(".cursorrules")
    assert should_process is False, "ERRO: ACE processou .cursorrules!"
    print("✅ Watcher Guard: Ignored patterns detectados corretamente.")
    
    # 3. Test Circuit Breaker: OPEN State
    print("3. Verificando Circuit Breaker (Veto de Segurança)...")
    circuit_breaker.state = "OPEN"
    circuit_breaker.last_failure_time = time.time()
    
    # Simular verify_safety que é async
    loop = asyncio.new_event_loop()
    is_safe = loop.run_until_complete(circuit_breaker.verify_safety())
    assert is_safe is False, "ERRO: ACE permitiu operação com Breaker OPEN!"
    print("✅ Circuit Breaker: Veto de segurança ativo (Fail-Closed).")
    
    # 4. Test Semantic Dedup Guard
    print("4. Verificando Semantic Dedup (Anti-Noise)...")
    content = "A arquitetura Antigravity é soberana."
    # Reset dedup state for test
    loop_guard._recent_hashes = {}
    
    gateway = MemoryGateway("http://localhost:8090", "test_key")
    
    success1, msg1 = gateway.append_concept("Insight 1", content, "INSIGHT", {})
    success2, msg2 = gateway.append_concept("Insight 2", content, "INSIGHT", {}) # Duplicata
    
    assert success1 is True, f"ERRO: Gateway rejeitou 1ª escrita: {msg1}"
    assert success2 is False, f"ERRO: Gateway permitiu duplicata semântica!"
    print(f"✅ Semantic Dedup: Bloqueou insight repetido. Msg: {msg2}")
    
    # 5. Test Rate Limit Guard
    print("5. Verificando Rate Limit (Burst Protection)...")
    loop_guard.action_history = []
    for i in range(5):
        loop_guard.register_action()
    
    can_act = loop_guard.check_rate_limit()
    assert can_act is False, "ERRO: Rate limit não disparou após 5 ações!"
    print("✅ Rate Limit: Proteção contra burst de eventos ativa.")
    
    # 6. Test Source Tagging (Auditoria)
    print("6. Verificando Source Tagging (Audit Trail)...")
    loop_guard.action_history = [] # Reset for next test
    payload = {"test": "data"}
    gateway.append_event("test_event", "test_actor", payload, "test_justification")
    
    sent_payload = mock_post.call_args[1]['json']['payload']
    assert "_governance" in sent_payload, "ERRO: Tagging de governança ausente!"
    assert sent_payload["_governance"]["origin"] == "ace", "ERRO: Origem incorreta no tagging!"
    print("✅ Source Tagging: Metadados de soberania injetados com sucesso.")

    print("\n🏆 TODOS OS TESTES PASSARAM. O TEC 14 ESTÁ SOB GOVERNANÇA TOTAL.")

if __name__ == "__main__":
    test_governance_suite()
