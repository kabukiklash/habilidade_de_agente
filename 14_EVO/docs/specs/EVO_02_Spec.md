# Especificação Funcional: [EVO-02] O Túnel Efêmero (Cloudflare Bridge)

## 1. Objetivo da Evolução
Criar uma ponte de comunicação segura, criptografada (HTTPS) e estritamente efêmera (sob demanda) que exponha a porta `8090` do CMS local para a internet pública, permitindo que Notebooks ou PCs Nômades enviem seus aprendizados para a base central sem a necessidade de uma VPS permanente.

## 2. Princípio Arquitetural Aplicado
**Infraestrutura Efêmera (Ephemeral Infrastructure) e Security by Obscurity.** Em vez de abrirmos portas (`Port Forwarding`) no roteador físico da empresa (o que traz riscos massivos de invasão de rede interna), terceirizamos o risco da borda para a Cloudflare via túneis de proxy reverso assíncrono. O servidor só existe na rede pública enquanto o script `.bat` estiver ativado.

---

## 3. Topologia e Arquivos Afetados

A implementação não afeta o código fonte do Python ou do Node.js. Trata-se puramente de uma operação de plataforma (DevOps) gerenciada por um script utilitário empacotado no repositório.

### 3.1. Arquivos Core (A Serem Criados)

#### `[NEW] root/ops/expor_cms_cloudflared.bat`
Este será o arquivo executável "One-Click" que o Administrador roda no PC Base (Onde o Docker Compose do CMS está rodando).

**Lógica Técnica Prevista dentro do `.bat`:**
1.  **Checagem de Dependência Segura:** Verificar se `cloudflared.exe` existe na pasta `ops/bin/`. Se não existir, o arquivo `.bat` consultará exclusivamente o repositório oficial da Cloudflare no GitHub (via HTTP GET com validação de TLS/SSL) para baixar a versão binária oficial do Windows, mitigando ataques de *Supply Chain*.
2.  **Verificação de Saúde (Sensor):** Antes de abrir o túnel, dispara um ping (`curl`) silencioso para `http://localhost:8090/api/health` para garantir que o CMS está de fato ligado.
3.  **Abertura do Túnel:** Executa o comando secreto: `cloudflared tunnel --url http://localhost:8090`.
4.  **Extração do Sensor:** O cloudflared cospe muitos logs no terminal. O script fará um *parsing* visual (usando regex ou split no PowerShell) para isolar especificamente a linha que contém a URL gerada (ex: `https://palavra-aleatoria-outra.trycloudflare.com`) e pintar de verde na tela para o usuário copiar facilmente.

---

## 4. Comportamento Operacional (A Jornada do Administrador)

| Ação Humana | Resultado Físico na Arquitetura |
| :--- | :--- |
| Duplo Clique em `expor_cms_cloudflared.bat` | O Cloudflare aloca uma URL global em < 3 segundos. O terminal pinta a URL de Verde. A porta local 8090 passa a aceitar pacotes mundiais. |
| Fechar a janela Preta do Terminal (CMD) | O túnel desaba instantaneamente. Qualquer chamada à URL gerada retornará "Host Not Found". O banco de dados volta a ser 100% isolado na intranet. |

## 5. Próximo Passo Cingulado (Pontos de Atenção)
Esta evolução cria a URL mágica rotativa. No entanto, lembremos que a [EVO-01] já ativou a barreira de API Key. Sendo assim, o túnel em si é público, mas tentar usar a URL no navegador ou no Postman sem o Header `X-ACE-API-KEY` resultará em um bloqueio sumário e silencioso feito pelo FastAPI no exato momento que o tráfego do túnel entregar o pacote. 

O próximo desafio é ensinar o Agente Remoto do programador (`ace_server.py`) a perguntar qual é essa URL e qual é a senha (API Key). Isso é o objeto da `[EVO-03]`.

---
> Aguardando Revisão do Arquiteto. 
> Se estiver Aprovada para ir pra código no futuro, diga **"Aprovado. Descreva a EVO-03"**.
