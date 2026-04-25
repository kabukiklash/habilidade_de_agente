# AfixControl: Matriz de Segurança e Permissões (Security & RBAC)

Este documento detalha as camadas de blindagem do sistema e a matriz de acesso baseada em papéis (Role-Based Access Control).

---

## 1. Níveis de Soberania (The Level Ladder)

O sistema utiliza a variável global `$level` para filtrar permissões de UI e Backend.

| Nível | Papel Técnico | Responsabilidades |
| :--- | :--- | :--- |
| **0** | Visitante/Erro | Sem acesso às áreas protegidas. |
| **1** | Produção | Visualização do Kanban e execução de O.S. |
| **2** | Gerente Produção | Priorização de fila e gestão de status industriais. |
| **3** | Comercial | Criação de propostas e gestão de seus próprios clientes. |
| **4** | Gerente Comercial | Supervisão de todas as propostas e aprovação de margens. |
| **5** | Administrador | Gestão de Predefinições Técnicas, Usuários e Reprecificação. |

### 1.1 Bloqueio de Perfil Comercial
Vendedores (Níveis 3 e 4) possuem um "Hard Lock": Se o campo `usuario_codigo_vendedor` estiver nulo ou zero, o sistema redireciona automaticamente para a página de perfil e impede qualquer operação comercial até a regularização.

---

## 2. Camadas de Blindagem de Dados

### 2.1 Sovereign Safety V2 (SQL Protection)
Identificado em métodos críticos como `Usuario::GetAll`.
- **Regex de Filtragem:** Bloqueia caracteres de controle SQL (`;`, `--`, `/*`).
- **White-listing:** Permite apenas comandos estruturais seguros. Se uma query malformada for detectada, o sistema gera um `error_log` ISO e aborta a execução.

### 2.2 Rate Limiting (`requires/rate_limiter.php`)
Protege os endpoints AJAX contra ataques de força bruta e sobrecarga de requisições, garantindo a disponibilidade do sistema em momentos de alta demanda (ex: reprecificação global).

### 2.3 Sanitização de Input (`CalculadoraCore::parseDecimal`)
Previne erros de injeção e falhas de cálculo ao forçar a conversão de strings monetárias em floats puros, removendo caracteres não numéricos antes do processamento aritmético.

---

## 3. Segurança de Sessão e Tokens
- **Session Token:** O sistema utiliza o cookie `afx_session` vinculado ao IP e agente do usuário.
- **Double Token Integration:** Para a RD Station, o sistema armazena dois tokens distintos para garantir que a falha de um não interrompa o fluxo de CRM.

---

## 4. Auditoria e Rastreabilidade (Snapshots)
- **Baseline de Propostas:** Toda alteração em proposta aprovada gera um snapshot na tabela `proposta_produtos_historico`.
- **Logs de Registro:** A tabela `registros` carimba cada ação administrativa com: `Usuario`, `Ação`, `Tabela`, `ID do Objeto` e `Timestamp`.

---
**Documento Gerado por Antigravity Sentry v3 - Auditoria de Segurança e Governança.**
