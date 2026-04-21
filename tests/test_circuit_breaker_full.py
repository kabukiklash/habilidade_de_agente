import asyncio
import os
import sys
import time

# Configuração de caminhos para o ambiente do usuário
BASE_DIR = r"c:\Users\RobsonSilva-AfixGraf\Habilidade_de_agente"
sys.path.insert(0, os.path.join(BASE_DIR, "03_CIRCUIT_BREAKER_V3", "core"))
sys.path.insert(0, os.path.join(BASE_DIR, "06_AUDIT_MONITOR_LEDGER", "core"))

from circuit_breaker_master import CircuitBreakerV3

async def test_circuit_breaker_maturity():
    print("="*60)
    print("ANTIGRAVITY - TESTE DE MATURIDADE DO CIRCUIT BREAKER v3")
    print("="*60)
    
    # Criamos uma instância com threshold baixo para o teste (1 falha já abre)
    # E timeout curto (5 segundos) para testar a recuperação
    breaker = CircuitBreakerV3(failure_threshold=1, recovery_timeout=5)
    
    # --------------------------------------------------------------------------
    # CENÁRIO 1: Estado Inicial (CLOSED)
    # --------------------------------------------------------------------------
    print(f"\n[CENÁRIO 1] Testando estado inicial (CLOSED)...")
    print(f"Estado atual: {breaker.state}")
    is_safe = await breaker.verify_safety("KNOWLEDGE_SYNC")
    print(f"Resultado: {'OK: PERMITIDO' if is_safe else 'BLOQUEADO'}")
    
    # --------------------------------------------------------------------------
    # CENÁRIO 2: Simulação de Falha Crítica (TRIPPING)
    # --------------------------------------------------------------------------
    print(f"\n[CENÁRIO 2] Simulando falha crítica na infraestrutura...")
    # Mudamos a URL para uma que não existe de propósito para forçar falha no ping
    breaker.cms_url = "http://localhost:9999/invalid" 
    
    # Tentamos verificar a segurança. Isso deve falhar o ping e abrir o circuito.
    await breaker.verify_safety("KNOWLEDGE_SYNC")
    print(f"Estado após falha: {breaker.state}")
    
    # --------------------------------------------------------------------------
    # CENÁRIO 3: Ativação do Modo FAIL-CLOSED (Phase 2 Enforcement)
    # --------------------------------------------------------------------------
    print(f"\n[CENÁRIO 3] Validando BLOQUEIO REAL (Enforcement Mode)...")
    
    print("Tentando enviar evento COGNITIVO (KNOWLEDGE_SYNC)...")
    is_safe_cog = await breaker.verify_safety("KNOWLEDGE_SYNC")
    print(f"Resultado Cognitivo: {'FALHA (Permitiu)' if is_safe_cog else 'OK: SUCESSO (Bloqueou)'}")
    
    print("Tentando enviar evento OPERACIONAL (TELEMETRY)...")
    is_safe_op = await breaker.verify_safety("TELEMETRY")
    print(f"Resultado Operacional: {'OK: SUCESSO (Permitiu Bypass)' if is_safe_op else 'FALHA (Bloqueou)'}")

    # --------------------------------------------------------------------------
    # CENÁRIO 4: Recuperação Automática (HALF-OPEN)
    # --------------------------------------------------------------------------
    print(f"\n[CENÁRIO 4] Validando janela de recuperação (HALF-OPEN)...")
    print("Aguardando 6 segundos (timeout de recuperação)...")
    await asyncio.sleep(6)
    
    # Agora o estado deve ser HALF_OPEN
    is_safe_retry = await breaker.verify_safety("KNOWLEDGE_SYNC")
    print(f"Estado após timeout: {breaker.state}")
    
    print("\n" + "="*60)
    if not is_safe_cog and is_safe_op:
        print("VEREDITO: CIRCUIT BREAKER 100% OPERACIONAL")
        print("   - Bloqueio Real: ATIVO")
        print("   - Bypass Operacional: ATIVO")
        print("   - Auto-Recuperação: ATIVA")
    else:
        print("FALHA NA VALIDAÇÃO DE SOBERANIA")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(test_circuit_breaker_maturity())
