# Especificação Funcional: [EVO-01] Barreira Zero-Trust (Middleware de Autenticação)

## 1. Objetivo da Evolução
Impedir absolutamente que qualquer entidade externa, seja através da Internet (túnel Cloudflare) ou da rede local, injete, leia ou manipule dados no Sistema de Memória Cognitiva (CMS) sem possuir uma credencial autorizada. 

## 2. Princípio Arquitetural Aplicado
**Zero-Trust Network Access (ZTNA).** O CMS deve sempre operar sob a premissa de que a rede em que ele se encontra (mesmo localhost) é hostil. Nenhuma requisição é confiável até que a identidade do remetente (o ACE Client) seja validada matematicamente.

---

## 3. Topologia e Arquivos Afetados

A implementação ocorrerá estritamente na Camada da API do CMS (Gateway de Entrada), não afetando a regra de negócios (Rotas) nem a persistência (Banco de Dados).

### 3.1. Arquivos Core (A Serem Modificados)

#### `cognitive-memory-service/app/main.py`
Este é o ponto focal. Substituiremos o fluxo aberto do FastAPI por um funil de autenticação.

**Alterações Técnicas Previstas:**
1.  **Importação de Segurança:** Adicionar bibliotecas nativas de segurança do FastAPI (`fastapi.security`, `HTTPBearer` ou `APIKeyHeader`).
2.  **Definição da Chave Mestra:** Carregar uma variável de ambiente `ACE_SECRET_KEY`. Se ela não existir no `.env`, o sistema irá travar (fail-fast) ao subir.
3.  **Implementação do Middleware / Dependência REST:** Criar uma função injetável `verify_api_key` que intercepta toda requisição REST.
4.  **Implementação de Segurança WebSocket (Handshake Criptografado):** O WebSocket deve nascer anônimo (sem chave na URL, pois provedores de rede e a Cloudflare gravam URLs em logs de texto plano). A conexão inicia sem autenticação; o CMS concede 3 segundos de tolerância. O Frontend envia um pacote JSON opaco (`{"auth": "sua-chave"}`) por dentro do túnel TLS. Se a chave for inválida ou o prazo esgotar, o backend encerra a conexão (`close(4001)`).
5.  **Defesa Anti-DoS (Rate Limiter de Borda):** O Middleware passará a contar as tentativas de falha (`401/403`). Se um IP exceder o limite (ex: 10 erros por minuto), ele será bloqueado em nível de memória RAM, evitando sobrecarga de CPU na averiguação excessiva de strings.
6.  **Associação Global às Rotas:** Proteger a inclusão dos *routers* (`app.include_router(events.router, dependencies=[Depends(verify_api_key)])`). E proteger rotas que servem HTML (Dashboard) com Basic Auth ou regra similar se acessadas via IP externo.

### 3.2. Arquivos de Configuração

#### `cognitive-memory-service/.env` (e arquivos derivados como `docker-compose.yml`)
1.  Adição da variável `ACE_SECRET_KEY=sua-chave-secreta-gigante-aqui`.

---

## 4. Comportamento e Retornos (HTTP Contracts)

| Ação Invasora | Comportamento do Sistema |
| :--- | :--- |
| Envio de Carga **Sem** o Header `X-ACE-API-KEY` | A carga não chega à rota. Retorno HTTP imediato: `401 Unauthorized`. |
| Envio com Header, mas Chave Errada | Retorno HTTP imediato: `403 Forbidden`. |
| Envio via GET para ler logs sem Header | Retorno HTTP imediato: `401 Unauthorized`. |
| Bater na Rota Base (`/`) ou Ping de Saúde | Retorno HTTP imediato: `200 OK`. Rota permanecerá **aberta/pública** (Decisão do Arquiteto) para permitir que monitores de uptime (ex: Cloudflare) confirmem que o serviço está no ar sem precisarem de chaves. |

## 5. Próximo Passo Cingulado (Pontos de Atenção)
Esta evolução quebrará imediatamente todos os clientes ACE que estão rodando nas máquinas hoje (já que o painel HTML atual e o `ace_server.py` não sabem ainda da existência dessa senha). Isso é arquiteturalmente correto (fail-safe). O reparo nos clientes será o objeto da `[EVO-03]`.

---
> Aguardando Revisão do Arquiteto (Você). 
> Se houver algo a adicionar ou a mudar na especificação (ex: decisão sobre o Healthcheck), me informe. Se estiver Aprovada para ir pra código no futuro, diga **"Aprovado. Descreva a EVO-02"**.
