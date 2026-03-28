# Especificação Funcional: [EVO-03] Cliente ACE Nômade (Fallback Híbrido)

## 1. Objetivo da Evolução
Dotar o Antigravity Context Engine (ACE) — o robô que roda na máquina local do programador junto com o Cursor — da inteligência necessária para detectar proativamente se o servidor central de memórias (CMS) está disponível localmente. Caso não esteja (ex: quando o dev está trabalhando de um notebook em outra rede), o ACE deve permitir a inserção manual de uma URL da nuvem (gerada na EVO-02) e a respectiva Chave de API de segurança (criada na EVO-01), alterando seu fluxo de dados *on-the-fly* sem necessidade de reiniciar o sistema local.

## 2. Princípio Arquitetural Aplicado
**Resiliência Híbrida Inteligente (Smart Hybrid Fallback) e Injeção Dinâmica de Configuração.** O cliente local nunca deve assumir que a infraestrutura central é permanente. Ele deve ter mecanismos de *fallback* (plano B) graciosos, evitando gargalos ou crashes no loop de injeção de prompt da IDE. O acoplamento com o backend passa a ser solto e configurável em tempo de execução.

---

## 3. Topologia e Arquivos Afetados

Esta evolução é dividida em duas camadas do cliente ACE: O Backend Local (Python) responsável pelas requisições, e a Interface de Controle (HTML/JS) com a qual o dev interage.

### 3.1. Arquivos Backend (A Serem Modificados)

#### `ace-installer-kit/ace_server.py`
**Alterações Técnicas Previstas:**
1.  **Variáveis de Estado Dinâmico:** As variáveis estáticas `cms_endpoint` (atualmente `http://localhost:8090/...`) nas classes `EconomyTracker` e `MemoryExtractor` deixarão de ser *hardcoded*. Elas passarão a ser alimentadas por um estado central gerenciado pelo servidor.
2.  **Novo Endpoint de Configuração (`/api/config_remote`):** Criar uma rota no FastAPI local (`8095`) que receba via POST um payload com a URL e Chave. **CRÍTICO:** Essa rota deverá gravar esses dados no arquivo `.env` local do Cliente ACE (ex: `ACE_REMOTE_URL` e `ACE_REMOTE_KEY`), garantindo que o agente recupere a configuração mesmo se o computador for reiniciado.
3.  **Hot-Reload de Variáveis (Sincronia RAM-Disco):** O endpoint `/api/config_remote` **não pode** apenas salvar o `.env`. Ele deve forçar a alteração das propriedades estáticas diretamente nas instâncias vivas em memória (`EconomyTracker.cms_endpoint = nova_url` e `MemoryExtractor.cms_concepts_endpoint = nova_url + "/tables/concepts/append"`), pois o Python carrega variáveis de ambiente apenas no boot.
4.  **Proteção de Fogo Amigo (.gitignore):** Imediatamente após injetar as credenciais no `.env` do cliente remoto, o script deverá obrigatoriamente abrir o arquivo `.gitignore` do projeto atual e verificar se a entrada `.env` já consta lá. Caso não exista, o script irá adicioná-la silenciosamente, evitando vazamentos acidentais da Chave da Empresa em repositórios públicos na nuvem.
5.  **Fila Local Offline (Padrão Outbox):** Se o envio para o CMS (local ou remoto) falhar por Timeout, conexão recusada ou qualquer erro de rede, o ACE **não descartará** os pacotes. Ele gravará os payloads pendentes num arquivo local `outbox.json`. Um loop periódico (a cada 30 segundos) tentará reenviar os pacotes acumulados assim que o Uplink ficar verde. Isso garante zero perda de dados em cenários Offline prolongados (ex: 8 horas num voo sem internet).
6.  **Injeção do Header de Segurança (EVO-01 Conectada):** Toda função na classe `EconomyTracker` e `MemoryExtractor` que usa `requests.post` será atualizada para checar se uma Chave de API foi fornecida. Se sim, o parâmetro `headers={"X-ACE-API-KEY": api_key}` será obrigatoriamente anexado à requisição. Caso contrário (tráfego puramente local antigo), tentará sem header.

### 3.2. Arquivos Frontend (A Serem Modificados)

#### `ace-installer-kit/dashboard.html`
**Alterações Técnicas Previstas:**
1.  **Lógica Visual de Verificação (Healthcheck em Loop):** O JS fará um `fetch` periódico assíncrono para tentar alcançar o `localhost:8090/api/health`.
2.  **Padrão Nômade de Interface (Card de Fallback):**
    *   **Cenário Local:** Se o CMS responder `200 OK` localmente, o painel mantém a aparência normal e pinta um farol de verde: `CMS Local: Ativo`.
    *   **Cenário Offline/Nômade:** Se a requisição local falhar (timeout ou conexão recusada), a interface revelará suavemente (via CSS) um "Card Amarelo de Alerta".
3.  **Componentes do "Card Nômade":**
    *   Mensagem: *"CMS Local Inacessível. Você está em modo Nômade?"*
    *   Campo Input 1: `URL do Túnel (Cloudflare)`
    *   Campo Input 2: `Chave de Autenticação (API Key)`
    *   Botão: `Configurar Relink Remoto`
4.  **Ação de Relink:** Ao clicar no botão, o JS fará o POST para a rota `/api/config_remote` (definida no 3.1). Ao receber sucesso, o painel volta ao normal, mas o farol muda para azul/cyan: `CMS Remoto: Ativo via Túnel`.

---

## 4. Comportamento e Retornos

| Condição Ambiental | Reação Visível do Cliente ACE | Reação do Motor Interno (`ace_server.py`) |
| :--- | :--- | :--- |
| **Computador QG (Online)** | Farol Verde. Card oculto. | Operação normal via `localhost`. Requisições diretas sem header obrigatório (ou com header default se configurado). |
| **Notebook Fora de Casa** | Revela Card Amarelo pedindo URL e Chave. | ACE entra em modo passivo em relação ao envio de dados, falhando silenciosamente no envio de métricas, **mas continuará injetando o contexto no Cursor normalmente (Função Primária preservada)**. |
| **Após Preencher Setup Nômade** | Farol Azul/Cyan. Card oculto. Novo log gerado confirmando uplink. | Atualiza endpoints de `localhost` para a URL do Cloudflare. Adiciona o Header nas requisições do pacote `requests`. Operação totalmente normalizada via internet pública. |

## 5. Próximo Passo Cingulado (Pontos de Atenção)
Com a EVO-03 concluída, o seu Notebook na rua já terá a capacidade técnica de se conectar ao CMS do seu computador em casa, contanto que o túnel da EVO-02 esteja levantado e protegido pela senha da EVO-01.

O ciclo sistêmico estará fechado, mas ainda nos falta guardar os raciocínios valiosos que agora vão viajar do Notebook até a Base. Para isso, o banco de dados precisará da estrutura de cofre final: o Livro Caixa da Inteligência, a ser projetado na `[EVO-04]`.

---
> Aguardando Revisão do Arquiteto. 
> Se estiver Aprovada a especificação híbrida e o comportamento local-first, ou se houver objeções ao Card Visual, responda. Para ir adiante diga **"Aprovado. Descreva a EVO-04"**.
