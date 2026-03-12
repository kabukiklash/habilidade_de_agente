# 🗺️ MAPA TÉCNICO: ARQUIVOS SOLTOS (Raiz) -> TECNOLOGIAS

Este documento mapeia os arquivos técnicos ativos da raiz às suas **Tecnologias Soberanas** e define seus destinos definitivos para a limpeza total da raiz.

| Arquivo | Tecnologia Relacionada | Função Técnica | Novo Lar Sugerido |
| :--- | :--- | :--- | :--- |
| `audit_db.py` | **Audit Monitor / Ledger** | Consulta os últimos 10 eventos do ledger SQLite. | `core/database/utils/` |
| `brain_bridge.py` | **Cognitive Cortex** | Ponte para delegação de análise a LLMs externos. | `core/llm/bridges/` |
| `cms_validation_data.json`| **CMS** | Cache de validação da integridade do DB. | `core/database/cache/` |
| `EMERGENCY_KILL.bat` | **Escudo Atômico** | Kill Switch de processos em caso de drift crítico. | `core/ops/safety/` |
| `evolution.db` | **Audit Monitor / Ledger** | Banco de dados SQLite principal do Ledger local. | `core/database/` |
| `antigravity.db` | **CMS Fallback** | SQLite de fallback para o CMS (Postgres). | `core/database/` |
| `example_integration.py` | **Cognitive Cortex** | Exemplo de integração externa do Cortex. | `examples/` |
| `inspect_db.py` | **CMS** | Inspeção de esquemas e tabelas nos bancos locais. | `core/database/utils/` |
| `kimi_bridge.py` | **Cognitive Cortex** | Interface direta para prompts via Cortex/Kimi. | `core/llm/bridges/` |
| `log_session.py` | **Audit Monitor / Ledger** | Injeção manual de logs de IDE Chat no Ledger. | `core/ops/utils/` |
| `migrate_db.py` | **CMS / Ledger** | Script de migração de campos (Tokens/USD). | `core/database/migrations/` |
| `STATE_CERTIFICATE.json` | **VibeCode G7** | Certificado de integridade matemática do estado. | `core/governance/` |
| `sync_kimi_knowledge.py` | **Cognitive Cortex** | Injeção de contexto local (Manual/Skills) no Kimi. | `core/llm/sync/` |
| `test_adapter.py` | **Memory Adapter** | Teste unitário do adaptador híbrido de memória. | `tests/unit/` |
| `test_import.py` | **Core** | Debug da árvore de imports e caminhos. | `tests/debug/` |
| `tmp_audit_db.py` | **Audit Monitor** | Auditoria temporária (Obsolescente). | `QUARENTENA_ANTIGRAVITY/` |
| `update_adapter.py` | **Memory Adapter** | Patch estrutural para o adaptador de memória. | `core/database/utils/` |
| `update_cortex.py` | **Cognitive Cortex** | Patch estrutural para o orquestrador Cortex. | `core/llm/utils/` |
| `update_events_history.py`| **Audit Monitor** | Atualização de metadados históricos no ledger. | `core/database/utils/` |
| `update_index_link.py` | **CMS** | Gerenciador de links de indexação vetorial. | `core/database/utils/` |
| `update_kimi.py` | **Cognitive Cortex** | Ajuste de parâmetros do cliente Kimi. | `core/llm/utils/` |
| `update_tables_stats.py` | **CMS** | Coleta de estatísticas de uso do banco. | `core/database/utils/` |
| `update_tables.py` | **CMS** | Manutenção geral de tabelas do CMS. | `core/database/utils/` |
| `verify_cms_api.py` | **CMS** | Validação de API CMS (FastAPI). | `tests/smoke/` |
| `verify_cms_data.py` | **CMS** | Validação de consistência interna de dados. | `tests/smoke/` |
| `verify_fixes_final.py` | **Audit Monitor / Core** | Teste final de regressão (Encoding + Persistência). | `tests/smoke/` |
| `verify_kimi_security.py` | **Cognitive Cortex** | Validação de filtros e segurança (G7/Drift). | `tests/smoke/` |

---
**Protocolo**: Após aprovação deste mapa, cada arquivo será movido para seu destino, os caminhos de import serão corrigidos/validados e o `verify_fixes_final.py` será rodado em cada etapa para garantir **Zero Crash**. 🦅🛡️⚙️
