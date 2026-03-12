# Antigravity Context Engine (ACE) - Standalone Kit

O ACE é um serviço local e leve responsável por monitorar o seu ambiente de desenvolvimento e atuar como uma governança cognitiva, injetando inteligência do seu CMS diretamente em IDEs como Cursor e VS Code.

## Estrutura do Pacote
- `ace_server.py`: O coração da aplicação (API + Monitor de Arquivos Wachdog + Servidor WebSocket).
- `dashboard.html`: Uma UI moderna para visualizar o fluxo de eventos e pausar/reiniciar o vigilante.
- `requirements.txt`: Dependências simples (FastAPI, Uvicorn, Websockets, Watchdog).
- `install.bat`: Script rápido para instalação no Windows.

## 🚀 Como instalar em qualquer máquina?

1. Descompacte ou clone esta pasta `ace-installer-kit` na máquina desejada.
2. Dê um duplo clique no arquivo `install.bat`. Ele vai baixar as dependências (`fastapi`, `uvicorn`, `watchdog`).
3. (Alternativa) Via terminal:
   ```powershell
   pip install -r requirements.txt
   ```

## 🎮 Como Usar

Para ligar o "Cérebro" para o projeto atual, abra o terminal na pasta do seu projeto de código fonte e execute:

```powershell
python "C:\Caminho\Ate\O\ace-installer-kit\ace_server.py" .
```
*(O `.` no final significa "monitore o diretório atual").*

O que vai acontecer em seguida?
1. O Painel de Controle abrirá automaticamente em seu navegador: **http://localhost:8095**
2. Ele começará a ouvir os salvamentos do seu Cursor/VS Code.
3. Você pode usar os botões **Pausar** ou **Iniciar** no navegador para poupar processos sem fechar o terminal.

## 🗑️ Como Desinstalar / Remover o Monitoramento

Caso você não queira mais que o Cursor/VS Code conecte seu projeto ao ACE, basta ir no Painel de Controle no navegador (http://localhost:8095) e clicar no botão **"Desinstalar ACE da Máquina"**.

Ele automaticamente:
- Exclui os arquivos intrusivos criados no seu repositório (ex: `.cursorrules`, `.clinerules`).
- Desliga a API e finaliza o processo da memória.
