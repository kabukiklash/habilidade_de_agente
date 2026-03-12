# ⚙️ MANUAL TÉCNICO: CIRCUIT BREAKER V3 (ESCUDO ATÔMICO)

Este documento explica o funcionamento do mecanismo de proteção do Antigravity e como gerenciar seus limites de segurança.

## 1. O que é o Circuit Breaker?
O **Circuit Breaker** é o "fusível" do sistema. Ele monitora a saúde da infraestrutura e bloqueia chamadas à IA (economizando tokens) se detectar instabilidade.

### Estados de Operação:
*   🟢 **CLOSED (Fechado)**: Sistema saudável. Operação normal.
*   🔴 **OPEN (Aberto)**: Falha detectada. Fluxo bloqueado para proteger contra erros e gastos inúteis.
*   🟡 **HALF_OPEN (Meio-Aberto)**: Período de teste para verificar se o sistema se recuperou.

## 2. Fluxo de Operação (Passo a Passo)
1.  **Verificação**: Antes de cada tarefa, o Cortex consulta o Breaker.
2.  **Teste de Pulso**: O Breaker tenta conectar-se ao CMS (Tecnologia 01).
3.  **Bloqueio**: Se o limite de falhas for atingido, o estado muda para **OPEN**.
4.  **Resfriamento**: O sistema espera 30 segundos antes de tentar novamente.
5.  **Restauração**: Se o teste em HALF_OPEN for bem-sucedido, o sistema volta a operar normalmente.

## 3. Configuração de Soberania (Tolerância Zero)

Atualmente, o sistema está configurado para **Tolerância Zero**:
*   `failure_threshold`: **1**
*   `recovery_timeout`: **30**

> [!IMPORTANT]
> **Tolerância Zero** significa que 1 única falha de conexão bloqueia o sistema. Isso garante que nenhuma decisão seja tomada sem acesso total à memória.

## 4. Como Ajustar a Tolerância (Guia Futuro)

Quando a infraestrutura estiver totalmente consolidada e você desejar uma operação mais fluida (menos sensível a pequenas oscilações de rede), siga este procedimento:

### Procedimento para Aumentar a Tolerância:
1.  Abra o arquivo: `03_CIRCUIT_BREAKER_V3/core/circuit_breaker_master.py`.
2.  Localize a linha de inicialização da classe: `def __init__(self, failure_threshold: int = 1, recovery_timeout: int = 30):`.
3.  Altere o valor de `failure_threshold`:
    *   **Sugestão**: Altere para **3**. Isso permitirá 2 tentativas automáticas antes de bloquear.
4.  (Opcional) Ajuste o `recovery_timeout` (ex: para **60**) se desejar que o sistema espere mais tempo para esfriar após uma falha real.
5.  Salve o arquivo. A mudança é aplicada instantaneamente no próximo carregamento do Cortex.

---
**Documentado por:** Antigravity (Sovereign Mode) 🦅🛡️⚙️
