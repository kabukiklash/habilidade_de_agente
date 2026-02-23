# Antigravity Evolution v2.0 - Replication Guide

Este guia descreve como replicar a evolução "Clawd-Inspired" em outra instância do Antigravity.

## 📦 Conteúdo do Pacote

A pasta `Habilidade_de_agente` agora é um "Portable Agent Core". Ela contém:

1.  **Novas Skills**:
    *   `local-brain`: Integração com LLMs locais.
    *   `knowledge-vault`: Sistema de memória persistente.
    *   `sandbox-executor`: Execução segura via Docker (Restrito).
    *   `canvas`: Dashboard visual.
    *   `remote-bridge`: (Desabilitado/Inativo).

2.  **Novos Agentes**:
    *   `historian`: Gerente de memória.

3.  **Histórico & Manual**:
    - `ANTIGRAVITY_MANUAL.md`: O guia mestre do sistema (v2.5).
    - `ANTIGRAVITY_EVOLUTION.md`: O plano de longo prazo.
    - Consulte `.agent/docs/evolution_v2/` para detalhes técnicos.

## 🚀 Como instalar em outra máquina

1.  **Copie a Pasta**:
    Copie todo o conteúdo de `Habilidade_de_agente` para o diretório de trabalho do novo agente.

2.  **Instale Dependências (Opcional)**:
    *   **Docker Desktop**: Necessário para a skill `sandbox-executor`.
    *   **LM Studio**: Necessário para a skill `local-brain`.
    *   **Cloudflared**: Necessário para tunelamento do `local-brain`.

3.  **Verifique a Instalação**:
    No novo ambiente, peça para o Antigravity:
    > "Execute o workflow /evolve para reconhecer suas novas habilidades."

4.  **Teste de Fogo**:
    *   Rode `/canvas` para ver se o dashboard abre.
    *   Rode `/status` (se disponível) ou pergunte "Quem é você?" para ver se ele reconhece as novas personas.

## ⚠️ Notas de Segurança

*   O **Remote Bridge** vai copiando como `.DISABLED`. Mantenha assim a menos que você configure chaves SSH seguras no novo host.
*   O **Sandbox** vai exigir autorização explicita. Isso é *by design*.
*   O **Knowledge Vault** (`.agent/memory/index.json`) contém caminhos absolutos desta máquina (`C:\Users\RobsonSilva-AfixGraf...`). **Lembre-se de pedir para o novo agente "Resetar a memória" ou "Atualizar os caminhos"** ao chegar na casa nova.
