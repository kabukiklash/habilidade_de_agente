# 🛫 PREFLIGHT_GATE_01.md (UNIFIED DATABASE PROVIDER)

**Auditor:** Antigravity  
**Alvo:** `server/db/index.ts`  
**Objetivo:** Criar uma Fonte da Verdade Única (SSoT) para conexões de banco de dados, suportando SQLite e Postgres dinamicamente com pooling e encerramento gracioso.

---

## 1. 🧠 DRY-RUN MENTAL (O CAMINHO DO DADO)
O `DatabaseProvider` será o único ponto de entrada para consultas ao banco.
- **Boot:** O sistema lê `DATABASE_URL` do `env.ts`.
- **Initialization:** Se `postgres://`, o provider inicia o pool do `pg`. Se não (ou se apontar para arquivo), inicia o `better-sqlite3`.
- **Consumption:** Serviços (`IntentService`, `ApprovalService`) importam o singleton `db`.
- **Shutdown:** Ao receber `SIGINT/SIGTERM`, o provider fecha o pool do Postgres ou encerra o WAL do SQLite antes de sair.

## 2. ⚡ TRÍADE DE FALHAS ANTECIPÁVEIS
1.  **Connection Refused (Postgres):** O backend tentar subir com Postgres mas a base estar offline (Mitigação: Fallback estratégico ou erro fatal explícito com LOG de diagnóstico).
2.  **Pool Exhaustion:** Múltiplos serviços criando conexões paralelas sem reutilizar o pool (Mitigação: Singleton rigoroso e limite de conexões no config).
3.  **Zumbi Lock (SQLite):** O processo ser morto no Windows sem fechar a conexão, deixando o arquivo `.sqlite-wal` órfão e travando o próximo boot (Mitigação: Hook de `process.on('exit')` e `process.on('uncaughtException')`).

## 3. 🛡️ INVARIANTES DE PROTEÇÃO
- **Atomicidade:** Transações (`db.transaction`) devem funcionar de forma idêntica em ambos os drivers.
- **Soberania do Caminho:** No modo SQLite, o caminho do arquivo **DEVE** ser absoluto para evitar o BS-09 (Fricção de Paths no Windows).
- **Interface Drizzle:** O objeto exportado `db` deve manter a interface `DrizzleDBSchema` para não quebrar a tipagem dos serviços.

## 4. ✅ CRITÉRIOS DE SUCESSO (PASS/FAIL)
- **PASS:** O `smoke.ts` funciona tanto com SQLite local quanto (quando configurado) com Postgres.
- **PASS:** O processo encerra sem deixar conexões pendentes (verificado via logs de shutdown).
- **FAIL:** Se houver importação duplicada de driver em outros arquivos (violando o Singleton).

---
**ESTADO:** AGUARDANDO REVISÃO DO ENGENHEIRO.
**AUTORIZAÇÃO:** Nenhuma mudança aplicada até aprovação deste Pre-flight.
