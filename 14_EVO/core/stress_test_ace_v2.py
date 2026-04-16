import sys
import os
import time
import asyncio
import hashlib
import json
from unittest.mock import patch, MagicMock

# Setup paths
base_dir = "c:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente"
ace_dir = os.path.join(base_dir, "14_EVO", "core")
sys.path.insert(0, ace_dir)
sys.path.insert(0, os.path.join(base_dir, "03_CIRCUIT_BREAKER_V3", "core"))

from loop_guard_master import loop_guard
from circuit_breaker_master import circuit_breaker
from ace_memory_gateway import MemoryGateway
from ace_server import ACEEventHandler

# Mock CMS Response
class MockResponse:
    def __init__(self, status_code, text="{}"):
        self.status_code = status_code
        self.text = text
    def json(self): return {}

class ValidationLog:
    def __init__(self):
        self.results = []
        self.logs = []
    
    def log(self, msg):
        print(msg)
        self.logs.append(f"[{time.strftime('%H:%M:%S')}] {msg}")
    
    def add_result(self, name, status):
        self.results.append(f"{name}: {status}")

v_log = ValidationLog()

async def run_validation():
    v_log.log("🚀 Iniciando Validação Completa ACE v2.0 (Governança Soberana)")
    
    with patch('requests.post') as mock_post:
        mock_post.return_value = MockResponse(201)
        
        # ---------------------------------------------------------
        # 1. TESTE A — LOOP DE FILE WATCHER (SELF-TRIGGER)
        # ---------------------------------------------------------
        v_log.log("\n--- TESTE A: LOOP DE FILE WATCHER ---")
        handler = ACEEventHandler()
        class Event:
            def __init__(self, path): self.src_path = path; self.is_directory = False
        
        # Simular arquivo de saída do ACE (deve ser ignorado)
        ace_file = os.path.join(os.getcwd(), ".cursorrules")
        v_log.log(f"Simulando evento em arquivo do ACE: {ace_file}")
        
        # Capturamos o sys.stdout para ver o print de rejeição se houver, 
        # mas aqui o loop_guard.should_process_event deve retornar False silenciosamente
        should = loop_guard.should_process_event(ace_file, origin="system")
        if not should:
            v_log.log("✅ PASS: Arquivo interno do ACE foi ignorado pelo Loop Guard.")
            v_log.add_result("TESTE A", "PASS")
        else:
            v_log.log("❌ FAIL: ACE permitiu processamento de arquivo interno!")
            v_log.add_result("TESTE A", "FAIL")

        # ---------------------------------------------------------
        # 2. TESTE B — LOOP COGNITIVO (SEMÂNTICO)
        # ---------------------------------------------------------
        v_log.log("\n--- TESTE B: LOOP COGNITIVO (SEMÂNTICO) ---")
        gateway = MemoryGateway("http://localhost:8090", "key_test")
        content = "Insight Soberano: O Circuit Breaker protege o fluxo."
        
        v_log.log("Persistindo 1ª vez...")
        gateway.append_concept("Insight Teste", content, "LESSON", {})
        
        v_log.log("Tentando persistir duplicata semântica...")
        success, msg = gateway.append_concept("Insight Teste", content, "LESSON", {})
        
        if not success and "Semantic Duplicate" in msg:
            v_log.log(f"✅ PASS: Deduplicação bloqueou duplicata. Motivo: {msg}")
            v_log.add_result("TESTE B", "PASS")
        else:
            v_log.log("❌ FAIL: Gateway permitiu duplicata semântica!")
            v_log.add_result("TESTE B", "FAIL")

        # ---------------------------------------------------------
        # 3. TESTE C — CIRCUIT BREAKER OPEN
        # ---------------------------------------------------------
        v_log.log("\n--- TESTE C: CIRCUIT BREAKER OPEN ---")
        circuit_breaker.state = "OPEN"
        circuit_breaker.last_failure_time = time.time()
        
        v_log.log("Simulando evento com Breaker OPEN...")
        is_safe = await circuit_breaker.verify_safety()
        if not is_safe:
            v_log.log("✅ PASS: Operação bloqueada pelo Veto do Circuit Breaker.")
            v_log.add_result("TESTE C", "PASS")
        else:
            v_log.log("❌ FAIL: Breaker permitiu operação em estado OPEN!")
            v_log.add_result("TESTE C", "FAIL")
        
        # Restaurar para próximos testes
        circuit_breaker.state = "CLOSED"

        # ---------------------------------------------------------
        # 4. TESTE D — AVALANCHE DE EVENTOS (STRESS)
        # ---------------------------------------------------------
        v_log.log("\n--- TESTE D: AVALANCHE DE EVENTOS (STRESS) ---")
        loop_guard.action_history = []
        v_log.log("Disparando 10 eventos em sequência rápida...")
        blocked_count = 0
        for i in range(10):
            if loop_guard.check_rate_limit():
                loop_guard.register_action()
            else:
                blocked_count += 1
        
        v_log.log(f"Eventos bloqueados pelo Rate Limiter: {blocked_count}/10")
        if blocked_count >= 5: # Esperamos que 5 passem e 5 sejam bloqueados (limite é 5/min)
            v_log.log("✅ PASS: Rate Limiter controlou a avalanche de eventos.")
            v_log.add_result("TESTE D", "PASS")
        else:
            v_log.log("❌ FAIL: Rate Limiter falhou em conter o burst!")
            v_log.add_result("TESTE D", "FAIL")

        # ---------------------------------------------------------
        # 5. TESTE E — FLUXO NORMAL CONTROLADO
        # ---------------------------------------------------------
        v_log.log("\n--- TESTE E: FLUXO NORMAL CONTROLADO ---")
        loop_guard.action_history = [] # Reset
        loop_guard._recent_hashes = {} # Reset
        
        valid_file = "core_logic.py"
        v_log.log(f"Monitorando arquivo: {valid_file}")
        
        if loop_guard.should_process_event(valid_file):
            v_log.log("1. Loop Guard aprovou evento legítimo.")
            if await circuit_breaker.verify_safety():
                v_log.log("2. Circuit Breaker aprovou operação saudável.")
                success, msg = gateway.append_event("test_type", "test_actor", {"val": 1}, "justification")
                if success:
                    v_log.log("3. Memory Gateway persistiu evento com sucesso.")
                    v_log.log("✅ PASS: Fluxo normal completo e governado.")
                    v_log.add_result("TESTE E", "PASS")
                else:
                    v_log.log(f"❌ FAIL: Gateway falhou na persistência: {msg}")
                    v_log.add_result("TESTE E", "FAIL")
        
        # ---------------------------------------------------------
        # 6. TESTE F — SOURCE TAGGING
        # ---------------------------------------------------------
        v_log.log("\n--- TESTE F: SOURCE TAGGING ---")
        try:
            last_call_json = mock_post.call_args[1].get('json', {})
            governance = last_call_json.get('payload', {}).get('_governance') if 'payload' in last_call_json else last_call_json.get('properties', {}).get('_governance')
            
            if governance and governance.get('origin') == 'ace':
                v_log.log(f"Metadados encontrados: {json.dumps(governance)}")
                v_log.log("✅ PASS: Tagging de origem auditável presente.")
                v_log.add_result("TESTE F", "PASS")
            else:
                v_log.log(f"⚠️ Debug: last_call_json keys: {list(last_call_json.keys())}")
                v_log.log("❌ FAIL: Tagging de governança ausente ou incorreto!")
                v_log.add_result("TESTE F", "FAIL")
        except Exception as e:
            v_log.log(f"❌ FAIL: Erro ao validar tagging: {e}")
            v_log.add_result("TESTE F", "FAIL")

        # ---------------------------------------------------------
        # 7. TESTE G — DEDUPE EM CARGA
        # ---------------------------------------------------------
        v_log.log("\n--- TESTE G: DEDUPE EM CARGA ---")
        v_log.log("Enviando 5 conteúdos idênticos em sucessão...")
        dup_attempts = 5
        dup_blocked = 0
        for i in range(dup_attempts):
            success, msg = gateway.append_concept("Carga", "Conteúdo Repetitivo", "STRESS", {})
            if not success and "Duplicate" in msg:
                dup_blocked += 1
        
        v_log.log(f"Duplicatas bloqueadas: {dup_blocked}/{dup_attempts-1}")
        if dup_blocked == dup_attempts - 1:
            v_log.log("✅ PASS: Deduplicação resistiu à carga massiva.")
            v_log.add_result("TESTE G", "PASS")
        else:
            v_log.log("❌ FAIL: Vazamento de duplicatas sob carga!")
            v_log.add_result("TESTE G", "FAIL")

    # ---------------------------------------------------------
    # RELATÓRIO FINAL
    # ---------------------------------------------------------
    v_log.log("\n" + "="*50)
    v_log.log("📊 RELATÓRIO FINAL DE VALIDAÇÃO ACE V2.0")
    v_log.log("="*50)
    for res in v_log.results:
        v_log.log(res)
    
    all_pass = all("PASS" in res for res in v_log.results)
    verdict = "APTO" if all_pass else "NÃO APTO"
    v_log.log(f"\nVEREDITO FINAL: {verdict}")
    v_log.log("="*50)

    # Persistir relatório em arquivo
    with open("validation_report_ace_v2.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(v_log.logs))

if __name__ == "__main__":
    asyncio.run(run_validation())
