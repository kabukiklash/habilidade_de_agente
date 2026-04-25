# AfixControl: Fluxos de Trabalho Detalhados (Business Workflows)

Este documento descreve as engrenagens operacionais do sistema, detalhando como o dado transita entre os departamentos Comercial, Arte e Produção.

---

## 1. O Ritual da Aprovação Comercial
O momento em que uma **Proposta** se materializa em um **Pedido**.

### 1.1 Processamento (`ajax/propostas.php` -> `classes/propostas.php`)
- **Gatilho:** O vendedor clica em "Aprovar Proposta".
- **Ações em Cascata:**
  1.  **Snapshot Final:** O sistema gera uma última revisão (`proposta_revisao`) para congelar o estado negociado.
  2.  **Criação do Pedido:** Os itens da proposta são copiados para a tabela de pedidos, gerando números de O.S. únicos para cada produto.
  3.  **Validação Fiscal:** Verifica se o CNPJ e os contatos (HML015) estão presentes para permitir o faturamento futuro.
  4.  **Notificação:** O sistema dispara alertas para os departamentos de Produção e Financeiro.

---

## 2. Protocolo de Solicitação de Layout (A Interação com a Arte)
Este fluxo é vital para produtos customizados que exigem aprovação visual do cliente.

### 2.1 Abertura da Solicitação (`ajax/solicitacao.php`)
- **Briefing:** O vendedor anexa especificações técnicas e arquivos vetoriais (`.cdr`, `.ai`).
- **Estado de Espera:** A proposta entra em modo de bloqueio para faturamento até que o layout seja "Finalizado".
- **Colaboração:** A classe `LayoutConversa` permite um chat persistente entre o vendedor e o designer, garantindo que o briefing seja seguido.

---

## 3. Fluxo Industrial (O Chão de Fábrica)
Gerido pelo módulo `producao.php` e pela inteligência de renderização da O.S.

### 3.1 Estágios do Kanban
1.  **Montagem:** Preparação técnica do arquivo aprovado no layout.
2.  **Impressão:** Primeira etapa de materialização física (Digital UV, Ecossolvente).
3.  **Pós-Processamento:** Laser (corte) ou Plotter (recorte).
4.  **Finalização Manual:** Acabamentos como furos, cantos arredondados ou colagem de adesivos.

### 3.2 Feedback de Qualidade (RNC/Prodsis)
Se um item falha em qualquer estágio (ex: erro de impressão), o sistema de **Não Conformidade (RNC)** é disparado.
- **Impacto:** O custo da perda é registrado, retroalimentando os relatórios de lucratividade real da proposta original.

---

## 4. Lógica de Logística e Frete
- **Cálculo:** Pode ser automático (VIPP) baseado no peso calculado pela `CalculadoraCore` ou manual (Transportadora).
- **Consolidação:** O valor do frete é anexado ao primeiro item do pedido de venda para fins de faturamento, mas mantido como custo global da proposta.

---
**Documento Gerado por Antigravity Sentry v3 - Mapeamento de Processos de Negócio.**
