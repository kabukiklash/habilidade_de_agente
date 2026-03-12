# 🧰 UTILIDADES — Central de Análise de Desempenho

Esta pasta contém scripts utilitários para análise de performance, economia de tokens e auditoria operacional do sistema Evolution.

## 📋 Scripts Disponíveis

| Script | Descrição | Uso |
|--------|-----------|-----|
| `session_token_estimator.py` | Estima tokens consumidos em uma sessão de trabalho com base nos arquivos modificados | `python session_token_estimator.py --hours 8` |

## 🚀 Como usar

### Estimador de Tokens de Sessão
```bash
# Estimativa das últimas 8 horas (sessão do dia)
python UTILIDADES/session_token_estimator.py

# Estimativa das últimas 72 horas (sessão longa)
python UTILIDADES/session_token_estimator.py --hours 72

# Com nome de sessão + salvar no log
python UTILIDADES/session_token_estimator.py --session "Minha Sessao" --hours 8 --log

# Ver log histórico de sessões
type UTILIDADES\token_log.json
```

## 📈 Futuros Scripts (Roadmap)
- `performance_audit.py` — Auditoria completa de performance (RAM, CPU, processos)
- `cms_health_check.py` — Health check detalhado do CMS com métricas
- `dependency_report.py` — Relatório de dependências e versões instaladas
- `workspace_size_analyzer.py` — Análise de tamanho e crescimento do workspace
