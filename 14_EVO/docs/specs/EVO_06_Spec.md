# Especificação Funcional: [EVO-06] O Cérebro de Vidro (Dashboard Unificado: Glass Brain)

## 1. Objetivo da Evolução
Transformar o atual `dashboard/index.html` estático do CMS em um Centro de Comando Vivo e de Nível Enterprise (Control Plane). O objetivo é provar para o Arquiteto e para os clientes da infraestrutura que o sistema é hiper-transparente, materializando graficamente as engrenagens ocultas: os sensores de saúde da rede (Online/Offline) e o raciocínio semântico traduzido vindo do ACE, tudo em tempo real.

## 2. Princípio Arquitetural Aplicado
**Observability-Driven Design (Interface Baseada em Sensores).** A interface com o usuário (UI) não é uma janela de inputs morta; ela é o reflexo exato do estado de saúde global da infraestrutura. A integração baseada em Eventos Reativos (WebSockets) garante tela fluida sem "Refresh", essencial em plataformas de monitoramento de Segurança ou Data Centers.

---

## 3. Topologia e Arquivos Afetados

A modificação ocorre inteiramente na camada Frontend (Single Page Application hospedada pelo FastAPI) e na forma como o Python serve dados assíncronos.

### 3.1. Arquivos Core (A Serem Modificados)

#### `cognitive-memory-service/dashboard/index.html` (e estilos relacionados)
**Alterações Visuais e ODD Previstas:**
1.  **Grid de Sensores (Semáforos):** Substituir indicadores amadores de texto por um Cluster de Sensores reais no topo da tela. 
    *   Sensor 1: `Túnel Cloudflare` (Verde: Uplink Ativo / Vermelho: Fechado).
    *   Sensor 2: `Armazenamento Imutável` (Verde: SQLite Travado / Vermelho: Vulnerável).
    *   Sensor 3: `Uplink ACE Nômade` (Monitoramento de PC Remoto).
2.  **Modo "Glass Brain" (Teatro de Operações Visual):**
    *   Representação gráfica dos nós: Ícone do *ACE* à esquerda, Ícone do *CMS* à direita.
    *   **Animação WebSocket:** Quando um pacote cruza a EVO-05 no backend, a UI desenha um envelope de luz (CSS Animation) viajando do ACE para o CMS. Se bloqueado pela segurança (EVO-01), o envelope queima em vermelho.
3.  **Terminal Semântico Anti-XSS:** Uma caixa central, no visual de "Hacker/DevSecOps", que escuta o WebSocket e injeta o texto gerado na EVO-05 de cima para baixo. **CRÍTICO:** O script deverá usar exclusivamente métodos seguros de inserção no DOM (ex: `document.createElement` e `.textContent`), banindo o uso de `innerHTML` para blindar a interface contra ataques de injeção *Cross-Site Scripting* (XSS) originados de mensagens manipuladas.
4.  **Integração do Input Nômade:** Formulário na interface para "Levantar Âncora" (Configurar o acesso Cloudflare para outros dispositivos da rede, caso aplicável).

### 3.2. Arquivos Backend (Apoio ao Dashboard)

#### `cognitive-memory-service/app/main.py` e `events.py`
**Alterações Técnicas Previstas:**
1.  **Gerenciador de Conexões WebSocket:** Aprimorar o `WebSocketManager` atual do FastApi. Ele vai retransmitir a tradução da EVO-05 simultaneamente para as instâncias de tela aberta.
2.  **API de Sensores de Borda (`/api/sensors_health`):** Rota que a UI consulta em background a cada 5 segundos para descobrir se o `.bat` do Cloudflare caiu, pintando os Semáforos no frontend imediatamente.

---

## 4. Comportamento e Retornos

| Evento Físico no Quarto/Server | Reação Instantânea na TELA (Dashboard) |
| :--- | :--- |
| Administrador fecha o CMD do Cloudflare (Túnel Derrubado) | Dashboard dá um "bip" visual. Semáforo `Túnel Cloudflare` muda para vermelho: "Offline". |
| Notebook na Rua envia um novo aprendizado (`[EVO-03]`) | Envelope de luz amarela pisca na tela viajando da esquerda para a direita; O Terminal Semântico imprime o resultado em inglês/português legível; O contador de *Total Tokens Saved* gira como um hodômetro de carro. |

## 5. Próximo Passo Cingulado (Pontos de Atenção)
Esta evolução sela o épico de maneira gloriosa. Nós passaremos de um script estático para uma verdadeira **Plataforma Nômade Antigravity**. Ao concluir a EVO-06, teremos o ciclo completo: A Borda Trancada (EVO-01), o Túnel (EVO-02), o Cliente Híbrido (EVO-03), a Base Imutável (EVO-04), a Tradução Semântica (EVO-05) e a Tela Espacial (EVO-06).

A partir do seu "OK", deixamos o plano conceitual e partimos direto para o Código! Qual será a nossa primeira ação? Implementaremos tudo sequencialmente desde a [EVO-01], ou você tem alguma ordem preferida?

---
> Aguardando Revisão e Ordem de Produção do Arquiteto. 
> Se estiver Aprovada esta última EVO, me dê o comando de largada para a **Fase 3 & 4 (Evo 04 e Evo 01 - Dados e Segurança)** conforme o nosso `task.md`. Você pode dizer: **"Todas Aprovadas. Inicie a codificação da EVO-04!"**
