# Configuração de Inteligência Local (Local Brain)

Objetivo: Integrar modelos de IA locais via LM Studio e Cloudflared para economizar tokens em tarefas específicas.

## Checklist

### Fase 1: Seleção de Modelos <!-- id: 0 -->
- [x] Definir modelo para Código (Code Beast) <!-- id: 1 -->
- [x] Definir modelo para Raciocínio/Planejamento (Logic Beast) <!-- id: 2 -->
- [x] Definir modelo para Chat/Roleplay (Creative Beast) - *Opcional* <!-- id: 3 -->

### Fase 2: Implementação da Skill <!-- id: 4 -->
- [x] Criar Skill `local-brain` para conectar ao LM Studio <!-- id: 5 -->
- [x] Configurar parâmetros de temperatura e contexto para cada "persona" local <!-- id: 6 -->

### Fase 3: Conexão e Teste <!-- id: 7 -->
- [x] Instruir usuário sobre tunelamento (Cloudflared) <!-- id: 8 -->
- [x] Testar conexão com `local-brain` <!-- id: 9 -->
