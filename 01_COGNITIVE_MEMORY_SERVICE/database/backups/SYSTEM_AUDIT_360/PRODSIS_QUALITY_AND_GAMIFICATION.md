# AfixControl: Integração de Qualidade e Gamificação (PRODSIS)

Este documento detalha o ecossistema PRODSIS, o subsistema responsável pelo controle de qualidade (RNC) e pelo engajamento produtivo através de gamificação.

---

## 1. O Conceito PRODSIS
Diferente do core administrativo, o PRODSIS foca no **Fator Humano** e na **Eficiência Técnica**. Ele opera como um PWA (Progressive Web App) minimalista para ser resiliente no ambiente de fábrica.

### 1.1 Gamificação e Meritocracia
O sistema implementa um algoritmo de pontuação baseado em:
- **Timer de Produção:** Tempo real gasto em cada tarefa.
- **Bônus de Pontos:** Recompensas por superar metas mínimas.
- **Medalhas:** 
  - **Ouro:** Performance excepcional (Acima de 110% da meta).
  - **Prata:** Meta atingida com consistência.
  - **Bronze:** Produtividade básica mantida.

---

## 2. Gestão de Não-Conformidades (RNC)
O coração da qualidade ISO do AfixControl.

### 2.1 O Ciclo da RNC (`prodsis/rnc.php`)
1.  **Abertura:** Quando um erro é detectado, registra-se a RNC vinculada ao setor (Impressão, Corte, Arte).
2.  **Responsáveis:** Utiliza a tabela `rnc_responsaveis` para atribuir a correção.
3.  **Análise de Causa Raiz:** Espaço para descrever por que o erro ocorreu (Erro de arquivo, Falha de máquina, Erro humano).
4.  **Custo do Erro:** O campo `add_valor_rnc.sql` indica que o sistema agora rastreia o prejuízo financeiro direto de cada falha.

---

## 3. Arquitetura Técnica PRODSIS
O PRODSIS utiliza uma arquitetura moderna de APIs RESTful internas.

| Endpoint | Função |
| :--- | :--- |
| `api/producao.php` | CRUD de registros de tempo e produtividade. |
| `api/ranking.php` | Cálculo em tempo real da posição dos funcionários. |
| `api/rnc.php` | Gestão do ciclo de vida das falhas técnicas. |
| `api/medalhas.php` | Regras de negócio para atribuição de recompensas. |

---

## 4. Persistência e Resiliência
- **LocalStorage:** O timer de produção é salvo no navegador do operador. Se houver queda de energia ou fechamento acidental, o tempo continua contando ao reabrir.
- **Service Worker:** Permite o funcionamento básico offline ou em redes Wi-Fi instáveis da fábrica.

---
**Documento Gerado por Antigravity Sentry v3 - Auditoria de Sistemas de Qualidade.**
