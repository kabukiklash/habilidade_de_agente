# CMS — Relatório de Auditoria (Código Real)
**Atualizado:** 2026-04-16 | **Base:** Inspeção de código + testes de execução

## Infraestrutura
- **Docker:** `cms_api` (FastAPI/Uvicorn porta 8090) + `cms_postgres` (pgvector porta 5433)
- **Banco:** `cognitive_memory` — PostgreSQL com extensão pgvector v0.5.1
- **Auth:** Zero-Trust via header `X-ACE-API-KEY` — Confirmado: 401 sem key, 403 key errada

## Arquivos de Código Real Verificados

### `client/cms_client_master.py` — 134 linhas
- Classe `CMSClient` com httpx async
- Métodos: `append_event`, `query_memory`, `pin`, `forget`, `consolidate`
- Default: `localhost:8090` + key `ace-genesis-sovereign-key-2026`

### `api/app/main.py` — 47 linhas
- FastAPI com CORS, ZeroTrustMiddleware
- Routers: `/tables`, `/stream`, `/memory`, `/governance`, `/audits`
- Dashboard estático montado em `/dashboard`

### `api/app/security.py` — 107 linhas
- `ZeroTrustMiddleware`: Valida API Key em todas as rotas (exceto /health, /docs, /dashboard)
- Rate limiter: 200 falhas/60s por IP
- Websocket auth via handshake JSON com timeout 3s

### `api/app/routes/` — 5 arquivos
- `tables.py` (7.264 bytes) — CRUD de eventos
- `memory.py` (5.100 bytes) — Query híbrida vetorial+grafo
- `audits.py` (3.985 bytes) — Trilha de auditoria
- `governance.py` (3.371 bytes) — Pin/Forget/Policies
- `stream.py` (3.759 bytes) — SSE em tempo real

## Dados no Banco (Verificado por execução)
- **7.979 eventos** armazenados
- **32.630 tokens** consumidos
- **2.918.791 tokens** economizados (98.9% eficiência)
- **7 auditorias** com dados reais do AfixControl

## Status: 🟢 OPERACIONAL (10/10)
