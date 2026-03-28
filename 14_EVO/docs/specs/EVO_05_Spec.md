# Especificação Funcional: [EVO-05] O Tradutor Semântico de Ações

## 1. Objetivo da Evolução
Transformar dados operacionais crus, técnicos e massantes ("JSONs frios") em logs narrativos humanizados e acionáveis. Em vez do painel exibir *`{"event": "save", "path": "auth.ts", "rule_applied": "local_db", "tokens": 1200}`*, ele exibirá no Glass Brain: *"🧠 O Agente salvou 1200 tokens no arquivo auth.ts forçando a IA a seguir a invariante do Banco de Dados Local"*.

## 2. Princípio Arquitetural Aplicado
**Observabilidade Semântica (Semantic Observability) e Interceptação Assíncrona.** A arquitetura não deve acoplar a tradução de linguagem natural ao fluxo crítico de injeção de prompt. A tradução do log técnico para o humano ocorre em *background* (processamento reativo), consumindo pacotes do ACE e gerando frases ricas sem atrasar os milissegundos do dev na IDE.

---

## 3. Topologia e Arquivos Afetados

A tradução ocorrerá na fronteira entre a API Central do CMS e a camada de WebSocket que entrega os dados para a interface visual. O ACE continua enviando apenas os dados leves, e o "Heavy Lifting" cognitivo ocorre no backend do QG.

### 3.1. Arquivos Backend (A Serem Modificados/Criados)

#### `cognitive-memory-service/app/services/semantic_translator.py` (ou dentro do `stream.py` / `events.py`)
**Lógica Técnica Prevista:**
1.  **Mapeamentos Invariáveis (Templates Rápidos):** Criar uma classe pura em Python que usa dicionários de templates em substituição de strings nativas padrão (sem precisar chamar a OpenAI para a tradução diária).
    *   *Exemplo de Template:* `"O {actor} aplicou {tokens} de contexto extraídos da regra {rule} no arquivo {file}."`
2.  **O Integrador Dinâmico (Alquimia de Logs):** A função pega os dados duros da EVO-04 (`ai_reasoning_audits`) ou os payloads em tempo real e substitui as variáveis.
3.  **Caminho para "Deep Translation":** Deixar um "hook" ou interface `ISemanticTranslator` pronta na arquitetura. Se, no futuro, o seu Cortex ou a Kimi se plugar oficialmente nesse pipeline, esse simples "template" passará a ser gerado de forma totalmente fluida por um LLM real. Mas, para essa EVO inicial, usaremos deterministic strings supersônicas.

### 3.2. Integração com as Rotas Atuais (`events.py` / WebSocket)
**Alterações Técnicas Previstas:**
1.  Quando a rota `/tables/events/append` ou a rota futura da auditoria receberem o POST do cliente ACE, o JSON não será apenas enfiado no banco. O fluxo será:
    *   A) Salva o cru no Banco Imutável.
    *   **B) Executa a classe do `Semantic Translator` no payload.**
    *   C) Pega o log rico e dispara no canal WebSocket (`/api/ws/...`) para atualizar todos os Dashboards Glass Brain conectados.

---

## 4. Comportamento e Retornos

| Geração de Evento | O Que Entendeu a Máquina | O Que Entendeu o Humano no Painel |
| :--- | :--- | :--- |
| Ping do Túnel caiu. | `{"status": "dead", "source": "CF_TUNNEL"}` | 🔴 **O Túnel Cloudflare (Borda Externa) desabou. Sistema offline.** |
| A extração curou código. | `{"id": "ev2", "file": "login.js", "qty": 4000}` | 🧠 O Agente **PC_LOCAL** blindou o Cursor e salvou incríveis **4.000 tokens** no arquivo `login.js`. |

## 5. Próximo Passo Cingulado (Pontos de Atenção)
Esta evolução transforma o backend em um "narrador" de tudo o que a IA faz. Porém, até este exato ponto, a narrativa vive apenas na memória RAM e flutua nos fios do WebSocket... não há um "palco" bonito para o Arquiteto assistir esse show em tempo real.

Construir esse palco visual definitivo com os botões, semáforos, gráficos vivos e terminal narrativo em uma experiência sci-fi é o que fecha esse ciclo espetacular: a **[EVO-06] O Cérebro de Vidro (Dashboard Unificado: Glass Brain)**.

---
> Aguardando Revisão do Arquiteto. 
> Se o modelo de tradução na Borda Interna (com foco inicial em templates velozes para proteger a latência) for adequado, ordene: **"Aprovado. Descreva a EVO-06"**.
