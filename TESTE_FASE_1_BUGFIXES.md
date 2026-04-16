# 🧪 PLANO DE TESTES - FASE 1: BUG FIXES ESSENCIAIS
**Data**: 2026-04-01
**Branch Testada**: `Evolucao_ISO` (após FASE 1)
**Commits Testados**: fa561e6, c5d8bb6, 822af4d

---

## 📋 SUMÁRIO DOS TESTES

Total de Testes: **18 casos**
- Teste 1-6: Sincronização RD Station
- Teste 7-12: Fluxo OTK
- Teste 13-18: CNPJ/CPF Validação

---

## 🔴 BLOCO 1: SINCRONIZAÇÃO RD STATION (fa561e6)
**Objetivo**: Validar que representante é sincronizado corretamente com RD Station

### TESTE 1.1: Criar proposta e sincronizar representante
```
PASSO 1: Acessar "Minhas Propostas"
PASSO 2: Criar nova proposta (clicar em + verde)
PASSO 3: Preencher dados básicos:
  - Cliente: MASTERCARD BRASIL LTDA
  - Produto: Qualquer um
  - Representante: "João Silva" (ou qualquer representante)
  - Valor: R$ 1.000,00

PASSO 4: Salvar proposta

VALIDAÇÃO ESPERADA:
  ✅ Proposta criada com sucesso
  ✅ Representante salvo corretamente
  ✅ Nenhum erro de banco de dados

VERIFICAR NO BANCO:
  SELECT proposta_representante FROM propostas WHERE proposta_id = LAST_ID;
  → Deve retornar o ID do representante correto
```

---

### TESTE 1.2: Sincronizar propostas com RD Station
```
PASSO 1: Em "Minhas Propostas", selecionar uma proposta
PASSO 2: Clicar no menu (três pontos) → "Sincronizar com RD"
PASSO 3: Aguardar resposta da API

VALIDAÇÃO ESPERADA:
  ✅ RD Station retorna sucesso (status 200)
  ✅ Representante aparece em RD Station
  ✅ Sem erro "Representante não sincronizado"

SE FALHAR:
  📋 Verificar logs: tail -f ../logs/error.log
  📋 Verificar RD Station API credentials em requires/connection.php
```

---

### TESTE 1.3: Atualizar representante e re-sincronizar
```
PASSO 1: Abrir proposta criada em TESTE 1.1
PASSO 2: Clicar em "Editar"
PASSO 3: Mudar representante para outro (ex: "Maria Santos")
PASSO 4: Salvar
PASSO 5: Sincronizar com RD novamente

VALIDAÇÃO ESPERADA:
  ✅ Representante atualizado no banco
  ✅ RD Station recebe representante novo
  ✅ Histórico de propostas mostra atualização
```

---

### TESTE 1.4: Criar proposta SEM representante (edge case)
```
PASSO 1: Criar nova proposta
PASSO 2: NÃO selecionar representante (deixar vazio)
PASSO 3: Tentar salvar

VALIDAÇÃO ESPERADA:
  ❌ Sistema deve avisar: "Representante obrigatório"
  ✅ Proposta não é salva

OU (se representante for opcional):
  ✅ Proposta salva sem representante
  ✅ Sincronização com RD trata null corretamente
```

---

### TESTE 1.5: Verificar classe Propostas sincronização
```
ARQUIVO: classes/propostas.php
LINHA: ~250-300 (pós-atualização)

VERIFICAR:
  ✅ Método sincronizarComRD() existe
  ✅ Recebe $representante_id como parâmetro
  ✅ Envia para $_rdstation->sincronizar()
  ✅ Log registra sincronização (error_log)
```

---

### TESTE 1.6: Regressão - Criar proposta sem sincronização
```
PASSO 1: Criar proposta
PASSO 2: NÃO sincronizar com RD
PASSO 3: Fechar proposta

VALIDAÇÃO ESPERADA:
  ✅ Proposta funciona normalmente
  ✅ Nenhum erro de sincronização automática
  ✅ Sistema permite criar proposta local sem RD
```

---

## 🟡 BLOCO 2: FLUXO OTK (c5d8bb6)
**Objetivo**: Validar que cadastro de cliente OTK funciona sem duplicatas

### TESTE 2.1: Criar cliente novo com OTK
```
PASSO 1: Ir para "Clientes" → "+ Novo Cliente"
PASSO 2: Preencher dados:
  - Razão Social: "EMPRESA TESTE OTK LTDA"
  - CNPJ: "12.345.678/0001-99"
  - Email: "contato@empresatestek.com.br"

PASSO 3: Clicar "Buscar no OTK"

VALIDAÇÃO ESPERADA:
  ✅ Sistema conecta em OTK API
  ✅ Retorna dados do cliente de OTK
  ✅ Preenche campos automaticamente
  ✅ Nenhum erro de timeout/conexão
```

---

### TESTE 2.2: Criar duplicata (mesmo CNPJ) - sem duplicatas
```
PASSO 1: Criar cliente com CNPJ "12.345.678/0001-99" (do TESTE 2.1)
PASSO 2: Tentar criar OUTRO cliente com mesmo CNPJ
PASSO 3: Submeter formulário

VALIDAÇÃO ESPERADA:
  ❌ Sistema avisa: "Cliente com esse CNPJ já existe"
  ✅ Duplicata não é criada
  ✅ Oferece opção de usar cliente existente
```

---

### TESTE 2.3: Fluxo OTK completo (cadastro + proposta)
```
PASSO 1: Criar cliente OTK (TESTE 2.1)
PASSO 2: Ir para "Minhas Propostas"
PASSO 3: Criar nova proposta com esse cliente
PASSO 4: Salvar proposta

VALIDAÇÃO ESPERADA:
  ✅ Cliente aparece no dropdown de clientes
  ✅ Proposta salva com cliente OTK
  ✅ Dados do cliente carregam corretamente
  ✅ Sem erro "Cliente não encontrado"
```

---

### TESTE 2.4: UX ao salvar cliente
```
PASSO 1: Preencher formulário de cliente
PASSO 2: Clicar "Salvar"

VALIDAÇÃO ESPERADA:
  ✅ Botão fica desativado durante envio
  ✅ Mostra "Salvando..." ou spinner
  ✅ Após 2-3 segundos, retorna à lista
  ✅ Novo cliente aparece na lista
  ✅ Nenhum erro de validação oculto
```

---

### TESTE 2.5: Listagem sem duplicatas
```
PASSO 1: Ir para "Clientes"
PASSO 2: Filtrar por nome "EMPRESA TESTE OTK"

VALIDAÇÃO ESPERADA:
  ✅ Aparece apenas 1 resultado
  ✅ Sem duplicatas de cliente
  ✅ Listagem mostra código OTK correto
```

---

### TESTE 2.6: Regressão - Clientes antigos funcionam
```
PASSO 1: Abrir cliente criado ANTES de FASE 1
PASSO 2: Criar proposta com esse cliente

VALIDAÇÃO ESPERADA:
  ✅ Clientes antigos funcionam normalmente
  ✅ Sem erro de compatibilidade
  ✅ OTK sync funciona para clientes novos e antigos
```

---

## 🔵 BLOCO 3: VALIDAÇÃO CNPJ/CPF (822af4d)
**Objetivo**: Validar que CNPJ/CPF são validados e normalizados corretamente

### TESTE 3.1: Validar CNPJ correto
```
PASSO 1: Ir para "Clientes" → "+ Novo Cliente"
PASSO 2: Campo "CNPJ": digitar "12.345.678/0001-99"
PASSO 3: Clicar fora do campo (para validar)

VALIDAÇÃO ESPERADA:
  ✅ CNPJ é validado (dígito verificador correto)
  ✅ Campo fica verde ✓
  ✅ Nenhuma mensagem de erro
```

---

### TESTE 3.2: Validar CNPJ incorreto
```
PASSO 1: Campo "CNPJ": digitar "11.111.111/1111-11" (inválido)
PASSO 2: Clicar fora do campo

VALIDAÇÃO ESPERADA:
  ❌ Campo fica vermelho ✗
  ❌ Mensagem: "CNPJ inválido"
  ✅ Formulário não permite salvar
```

---

### TESTE 3.3: CNPJ com máscara automática
```
PASSO 1: Campo "CNPJ": digitar sem máscara "12345678000199"
PASSO 2: Aguardar auto-formatação

VALIDAÇÃO ESPERADA:
  ✅ Sistema formata automaticamente para "12.345.678/0001-99"
  ✅ Validação funciona na máscara
```

---

### TESTE 3.4: Validar CPF correto
```
PASSO 1: Se cliente é PF (Pessoa Física)
PASSO 2: Campo "CPF": digitar "123.456.789-10" (exemplo válido)
PASSO 3: Clicar fora

VALIDAÇÃO ESPERADA:
  ✅ CPF é validado
  ✅ Campo fica verde ✓
  ✅ Nenhum erro
```

---

### TESTE 3.5: Normalização de documento
```
PASSO 1: Digitar CNPJ com espaços/caracteres extras "12  345 678 / 0001 - 99"
PASSO 2: Salvar cliente

VALIDAÇÃO ESPERADA:
  ✅ Sistema normaliza para "12345678000199" (sem máscara no banco)
  ✅ Banco armazena versão limpa
  ✅ Exibição mostra com máscara "12.345.678/0001-99"
```

---

### TESTE 3.6: Classe CnpjCpfNormalizer
```
ARQUIVO: classes/CnpjCpfNormalizer.php
VERIFICAR:
  ✅ Método normalizar() remove máscara
  ✅ Método validarCNPJ() valida dígito verificador
  ✅ Método validarCPF() valida dígito verificador
  ✅ Sem erros de sintaxe PHP
```

---

## 📊 MATRIZ DE VALIDAÇÃO

### Resultado de Cada Bloco:

| Bloco | Testes | Status | Observações |
|-------|--------|--------|-------------|
| **1: RD Station** | 1.1-1.6 | ⏳ | Validar sincronização |
| **2: OTK** | 2.1-2.6 | ⏳ | Validar cadastro e duplicatas |
| **3: CNPJ/CPF** | 3.1-3.6 | ⏳ | Validar validação e normalização |

---

## ✅ CRITÉRIO DE ACEITAÇÃO

**FASE 1 passa se:**
- [ ] Bloco 1: 6/6 testes passam (RD Station)
- [ ] Bloco 2: 6/6 testes passam (OTK)
- [ ] Bloco 3: 6/6 testes passam (CNPJ/CPF)
- [ ] Nenhum erro crítico (PHP errors, warnings)
- [ ] Nenhuma regressão em funcionalidades existentes

**FASE 1 falha se:**
- ❌ Qualquer teste retorna resultado inesperado
- ❌ Aparecem PHP errors/warnings
- ❌ Sistema quebra ou fica lento
- ❌ Banco de dados tem inconsistências

---

## 🔧 FERRAMENTAS DE TESTE

### Verificar Logs em Tempo Real:
```bash
# Terminal 1: Logs de erro PHP
tail -f ../logs/error.log

# Terminal 2: Logs de sucesso/debug
tail -f ../logs/debug.log
```

### Verificar Banco de Dados:
```sql
-- Ver clientes criados em testes
SELECT cliente_id, cliente_nome, cliente_cnpj, cliente_representante FROM clientes
ORDER BY cliente_id DESC LIMIT 10;

-- Ver propostas criadas
SELECT proposta_id, proposta_cliente, proposta_representante FROM propostas
ORDER BY proposta_id DESC LIMIT 5;

-- Ver logs de sincronização (se existir)
SELECT * FROM logs WHERE log_tipo = 'RD_SINCRONIZACAO'
ORDER BY log_data DESC LIMIT 10;
```

### Verificar API RD Station:
```bash
# Fazer requisição manualmente para testar RD Station
curl -X GET "https://api.rdstation.com/clientes?token=YOUR_TOKEN" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 📝 PROTOCOLO DE TESTE

### Para cada teste, registre:
1. **Data/Hora**: Quando foi executado
2. **Executor**: Quem fez o teste
3. **Resultado**: ✅ Passou / ❌ Falhou
4. **Observações**: Qualquer detalhe importante
5. **Screenshot**: Se falhou, tirar screenshot do erro

---

## 🎯 PRÓXIMOS PASSOS

**Após executar todos os testes:**

Se **TODOS PASSAM** ✅:
→ Proceder para FASE 2 (Cálculos Críticos)

Se **ALGUM FALHA** ❌:
→ Reportar qual teste falhou
→ Mostrar erro/screenshot
→ Vamos debugar antes de prosseguir

---

## 📋 CHECKLIST DE EXECUÇÃO

```
ANTES DE COMEÇAR:
☐ Fazer backup do banco de dados
☐ Ter acesso à branch Evolucao_ISO
☐ Sistema rodando em localhost
☐ RD Station API acessível (ou mock disponível)
☐ OTK Web API acessível (ou mock disponível)

DURANTE OS TESTES:
☐ Executar testes na ordem (1.1 → 1.6 → 2.1 → ... → 3.6)
☐ Registrar resultado de cada teste
☐ Se falhar, não pular - investigar
☐ Tomar screenshots de erros

APÓS OS TESTES:
☐ Revisar todos os resultados
☐ Documentar qualquer issue encontrada
☐ Confirmar se procede para FASE 2 ou não
```

---

## 🚀 VOCÊ ESTÁ PRONTO?

Execute os testes e me reporte os resultados!

Formato de resposta sugerido:
```
✅ TESTE 1.1: PASSOU
✅ TESTE 1.2: PASSOU
❌ TESTE 2.1: FALHOU - [descrever erro]
✅ TESTE 2.2: PASSOU
...
CONCLUSÃO: [X]/18 testes passaram
```

**Começamos?**

