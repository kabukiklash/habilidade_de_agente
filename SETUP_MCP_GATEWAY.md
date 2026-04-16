# 🚀 SETUP MCP Gateway - Instruções de Implementação

**Data:** 01 de abril 2026
**Objetivo:** Executar a API Gateway e conectar o MCP Server Node.js

---

## ✅ PASSO 1: Rodar a API Gateway (Terminal 1)

**NOTA:** AfixControl está em localhost:8050, então vamos rodar API em **8051**

### Via Docker (Recomendado):

```powershell
cd C:\Users\RobsonSilva-AfixGraf\Habilidade_de_agente\WORKSPACE\PROJETOS\AfixcontrolAfixgraf

docker run -it --rm `
  -p 8051:8000 `
  -v "C:\Users\RobsonSilva-AfixGraf\Habilidade_de_agente\WORKSPACE\PROJETOS\AfixcontrolAfixgraf:/app" `
  -w /app `
  -e AFIXCONTROL_DB_HOST=afixcontrolafixgraf-db-1 `
  -e AFIXCONTROL_DB_PORT=3306 `
  -e AFIXCONTROL_DB_USER=root `
  -e AFIXCONTROL_DB_PASSWORD=admin `
  -e AFIXCONTROL_DB_NAME=afixcontrol `
  php:8.2-cli php -S 0.0.0.0:8000

# Você verá:
# [Wed Apr 01 10:50:00 2026] PHP 8.2.0 Development Server running at http://0.0.0.0:8000
```

### Windows CMD:

```cmd
cd C:\Users\RobsonSilva-AfixGraf\Habilidade_de_agente\WORKSPACE\PROJETOS\AfixcontrolAfixgraf

set AFIXCONTROL_DB_HOST=afixcontrolafixgraf-db-1
set AFIXCONTROL_DB_PORT=3306
set AFIXCONTROL_DB_USER=root
set AFIXCONTROL_DB_PASSWORD=admin
set AFIXCONTROL_DB_NAME=afixcontrol

php -S localhost:8050
```

---

## ✅ PASSO 2: Testar a API (Terminal 2)

```bash
# Teste 1: Health Check
curl http://localhost:8051/api/mcp-gateway.php

# Esperado: JSON com endpoints disponíveis

# Teste 2: Validar Banco
curl "http://localhost:8051/api/mcp-gateway.php?action=validate_database"

# Esperado: Status SUCCESS ou WARNING com dados do banco

# Teste 3: Validar Encoding
curl "http://localhost:8051/api/mcp-gateway.php?action=validate_encoding"

# Esperado: Status com lista de arquivos e encoding

# Teste 4: Validar Git
curl "http://localhost:8051/api/mcp-gateway.php?action=validate_git"

# Esperado: Branch atual, último commit, tags

# Teste 5: Executar Testes
curl "http://localhost:8051/api/mcp-gateway.php?action=execute_tests"

# Esperado: Resultados dos testes PHP
```

**Se tudo funcionar, você verá JSON estruturado com `"status": "SUCCESS"` ✅**

---

## ✅ PASSO 3: Rodar o MCP Server Node.js (Terminal 3)

```bash
cd C:\Users\RobsonSilva-AfixGraf\Habilidade_de_agente\afixcontrol-mcp-server

# Definir variáveis (mesmas da API)
set AFIXCONTROL_DB_HOST=afixcontrolafixgraf-db-1
set AFIXCONTROL_DB_PORT=3306
set AFIXCONTROL_DB_USER=root
set AFIXCONTROL_DB_PASSWORD=admin
set AFIXCONTROL_DB_NAME=afixcontrol

# Rodar servidor com AUTO_TEST
set AUTO_TEST=true
node dist/server.js

# Esperado: Conecta à API e mostra status das 4 tools
```

---

## 📊 Arquitetura de Funcionamento

```
┌─────────────────────────────────┐
│   MCP Server Node.js            │
│   (afixcontrol-mcp-server/)     │
└──────────────┬──────────────────┘
               │ HTTP GET
               ▼
┌─────────────────────────────────┐
│   API Gateway PHP               │
│   (api/mcp-gateway.php)         │
│   localhost:8050                │
└──────────────┬──────────────────┘
               │ PDO/Shell/FS
               ▼
┌──────────────────────────────────────────┐
│   Recursos Locais                        │
│   - MySQL (afixcontrolafixgraf-db-1)     │
│   - File System (projetos/)              │
│   - Git (repositórios)                   │
│   - PHP (testes)                         │
└──────────────────────────────────────────┘
```

---

## 🧪 Próximo Passo: Registrar no .mcp.json

Depois que ambos funcionarem, vou registrar o MCP Server em:
```
C:\Users\RobsonSilva-AfixGraf\.claude\projects\...\Habilidade_de_agente\.mcp.json
```

E então poderei usar direto nos meus tools! ✅

---

## 🚨 Troubleshooting

### API não conecta ao banco:
```
❌ "ENOTFOUND afixcontrolafixgraf-db-1"

Solução: Testar com localhost ou IP do container:
curl "http://localhost:8050/api/mcp-gateway.php?action=validate_database&host=localhost"
```

### PHP não está no PATH:
```
❌ "'php' não é reconhecido"

Solução: Usar caminho completo:
C:\xampp\php\php.exe -S localhost:8050
```

### Porta 8050 em uso:
```
❌ "Address already in use"

Solução: Usar outra porta:
php -S localhost:8051
```

---

## ✅ Checklist de Conclusão

- [ ] API Gateway rodando em localhost:8050
- [ ] Teste de health check funcionando
- [ ] validate_database retornando dados
- [ ] validate_encoding retornando dados
- [ ] validate_git retornando dados
- [ ] MCP Server Node.js rodando
- [ ] MCP Server conectando à API com sucesso
- [ ] Pronto para registrar em .mcp.json

---

**Quando todos os testes passarem, me avisa!** 🚀
