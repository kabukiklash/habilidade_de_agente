import os
import sys
import asyncio
import json
import webbrowser
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import uvicorn
import threading
import time
import requests
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    observer.schedule(event_handler, target_dir, recursive=True)
    observer.start()
    print(f"ACE monitorando: {target_dir}")
    yield
    # Shutdown
    observer.stop()
    observer.join()

app = FastAPI(lifespan=lifespan)

status = "running"
connected_websockets = []
target_dir = os.getcwd()


# ============================================================
# EVO-03: Nomadic Configuration Manager
# ============================================================
class NomadConfig:
    """Manages dynamic CMS URL, API Key, .env persistence, and .gitignore protection."""
    _cms_base_url = os.getenv("ACE_REMOTE_URL", "http://localhost:8090")
    _api_key = os.getenv("ACE_REMOTE_KEY", "")
    _env_file = os.path.join(os.path.dirname(__file__), ".env")

    @classmethod
    def get_events_endpoint(cls):
        return f"{cls._cms_base_url}/tables/events/append"

    @classmethod
    def get_concepts_endpoint(cls):
        return f"{cls._cms_base_url}/tables/concepts/append"

    @classmethod
    def get_audits_endpoint(cls):
        return f"{cls._cms_base_url}/audits/append"

    @classmethod
    def get_health_endpoint(cls):
        return f"{cls._cms_base_url}/health"

    @classmethod
    def get_auth_headers(cls):
        if cls._api_key:
            return {"X-ACE-API-KEY": cls._api_key}
        return {}

    @classmethod
    def configure(cls, remote_url: str, api_key: str):
        """Hot-reload: Updates RAM variables AND persists to .env file."""
        cls._cms_base_url = remote_url.rstrip("/")
        cls._api_key = api_key

        # Also update os.environ for any child processes
        os.environ["ACE_REMOTE_URL"] = cls._cms_base_url
        os.environ["ACE_REMOTE_KEY"] = cls._api_key

        # Persist to .env file
        cls._save_to_env_file()
        # Protect .gitignore
        cls._ensure_gitignore()

    @classmethod
    def _save_to_env_file(cls):
        """Writes ACE_REMOTE_URL and ACE_REMOTE_KEY to the local .env file."""
        env_data = {}
        if os.path.exists(cls._env_file):
            with open(cls._env_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if "=" in line and not line.startswith("#"):
                        k, v = line.split("=", 1)
                        env_data[k.strip()] = v.strip()

        env_data["ACE_REMOTE_URL"] = cls._cms_base_url
        env_data["ACE_REMOTE_KEY"] = cls._api_key

        with open(cls._env_file, "w", encoding="utf-8") as f:
            f.write("# ACE Nomadic Config (auto-generated)\n")
            for k, v in env_data.items():
                f.write(f"{k}={v}\n")

    @classmethod
    def _ensure_gitignore(cls):
        """Ensures .env is listed in .gitignore to prevent credential leaks."""
        gitignore_path = os.path.join(target_dir, ".gitignore")
        if os.path.exists(gitignore_path):
            with open(gitignore_path, "r", encoding="utf-8") as f:
                content = f.read()
            if ".env" not in content.split("\n"):
                with open(gitignore_path, "a", encoding="utf-8") as f:
                    f.write("\n# ACE: Protect API credentials\n.env\n")
        else:
            with open(gitignore_path, "w", encoding="utf-8") as f:
                f.write("# ACE: Protect API credentials\n.env\n")

    @classmethod
    def is_remote(cls):
        return "localhost" not in cls._cms_base_url and "127.0.0.1" not in cls._cms_base_url


# ============================================================
# EVO-03: Outbox Queue (Offline Resilience)
# ============================================================
class OutboxQueue:
    """Local queue for failed CMS deliveries. Retries automatically when online."""
    _outbox_file = os.path.join(os.path.dirname(__file__), "outbox.json")
    _queue = []
    _retry_interval = 30  # seconds

    @classmethod
    def load(cls):
        if os.path.exists(cls._outbox_file):
            try:
                with open(cls._outbox_file, "r", encoding="utf-8") as f:
                    cls._queue = json.load(f)
            except Exception:
                cls._queue = []

    @classmethod
    def _save(cls):
        with open(cls._outbox_file, "w", encoding="utf-8") as f:
            json.dump(cls._queue, f, ensure_ascii=False)

    @classmethod
    def enqueue(cls, endpoint: str, payload: dict, headers: dict):
        cls._queue.append({"endpoint": endpoint, "payload": payload, "headers": headers})
        cls._save()

@classmethod
    def flush(cls):
        """Retry pending deliveries in safe batches to prevent 429 Rate Limits."""
        if not cls._queue:
            return 0

        delivered = 0
        remaining = []
        
        # Pega no máximo 50 pacotes por ciclo para não derrubar o CMS
        batch_to_process = cls._queue[:50]
        items_left_in_queue = cls._queue[50:]
        
        for item in batch_to_process:
            try:
                # Adiciona um micro-respiro para o banco de dados processar o evento
                time.sleep(0.1) 
                r = requests.post(item["endpoint"], json=item["payload"], headers=item["headers"], timeout=3)
                if r.status_code in (200, 201):
                    delivered += 1
                else:
                    remaining.append(item)
            except Exception:
                remaining.append(item)

        # Atualiza a fila com o que falhou + o que ficou de fora do lote atual
        cls._queue = remaining + items_left_in_queue
        cls._save()
        return delivered

    @classmethod
    def start_retry_loop(cls):
        """Background thread that flushes the outbox periodically."""
        def _loop():
            while True:
                time.sleep(cls._retry_interval)
                flushed = cls.flush()
                if flushed > 0:
                    print(f"[Outbox] Entregou {flushed} pacote(s) pendente(s) ao CMS.")

        t = threading.Thread(target=_loop, daemon=True)
        t.start()

class EconomyTracker:
    # A base de economia: Quantos tokens custaria se o Cursor...
    tokens_saved_per_action = 1200 # Calibrado para o tamanho real das regras
    total_saved = 0
    cms_endpoint = None  # Managed by NomadConfig
    _state_file = os.path.join(os.path.dirname(__file__), ".ace_economy_state.json")
    
    # Previne que o contador dispare loucamente a cada "Ctrl+S" seguido no mesmo arquivo
    _last_injection_time = {}
    COOLDOWN_SECONDS = 60 # Só conta economia 1x por minuto por arquivo
    
    @classmethod
    def load_state(cls):
        import json
        if os.path.exists(cls._state_file):
            try:
                with open(cls._state_file, "r") as f:
                    data = json.load(f)
                    cls.total_saved = data.get("total_saved", 0)
            except Exception:
                pass
                
    @classmethod
    def save_state(cls):
        import json
        try:
            with open(cls._state_file, "w") as f:
                json.dump({"total_saved": cls.total_saved}, f)
        except Exception:
            pass
            
    @classmethod
    def register_action(cls, file_name):
        import time
        current_time = time.time()
        last_time = cls._last_injection_time.get(file_name, 0)
        
        # Se salvou o MESMO arquivo nos últimos 60 segundos, ignora a economia (debounce)
        if current_time - last_time < cls.COOLDOWN_SECONDS:
            return cls.total_saved, False
            
        cls._last_injection_time[file_name] = current_time
        cls.total_saved += cls.tokens_saved_per_action
        cls.save_state()
        
        # Envia silenciosamente para o Immutable Ledger do CMS
        try:
            payload = {
                "event_type": "cognitive.context.injected",
                "actor": "ACE_Daemon",
                "payload": {"target": file_name},
                "justification": "Injecao de regras locais no Cursor para evitar Retrieval Cloud",
                "tokens_used": 0,
                "tokens_saved": cls.tokens_saved_per_action
            }
            endpoint = NomadConfig.get_events_endpoint()
            headers = NomadConfig.get_auth_headers()
            response = requests.post(endpoint, json=payload, headers=headers, timeout=2)
            if response.status_code not in (200, 201):
                raise Exception(f"HTTP {response.status_code}")
        except Exception as e:
            # EVO-03 Outbox: Queue failed deliveries for later retry
            OutboxQueue.enqueue(NomadConfig.get_events_endpoint(), payload, NomadConfig.get_auth_headers())
            print(f"CMS offline. Pacote enfileirado no Outbox: {e}")
            
        return cls.total_saved, True

class MemoryExtractor:
    cms_concepts_endpoint = None  # Managed by NomadConfig
    
    @classmethod
    def extract_from_cursor(cls, t_dir):
        # Lê o rascunho de aprendizados reais do Cursor (ex: bugfixes do dia)
        raw_learning_path = os.path.join(t_dir, ".cursor", "aprendizados_brutos.md")
        
        if not os.path.exists(raw_learning_path):
            return False, "Nenhum aprendizado bruto (aprendizados_brutos.md) encontrado na pasta .cursor."
            
        try:
            with open(raw_learning_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            if not content.strip():
                return False, "O arquivo de aprendizados está vazio."
                
            # Envia o "Nó Sináptico" da lição de casa para a Nuvem/Base Central do CMS
            payload = {
                "name": f"Aprendizado Dinâmico Cursor ({time.strftime('%Y-%m-%d %H:%M')})",
                "description": content,
                "node_type": "LESSON_LEARNED",
                "properties": {"source": "ACE_Extractor", "status": "raw_ingestion"}
            }
            
            response = requests.post(
                NomadConfig.get_concepts_endpoint(),
                json=payload,
                headers=NomadConfig.get_auth_headers(),
                timeout=3
            )
            
            if response.status_code in (200, 201):
                # Tenta limpar o arquivo local, mas trata erro se a IDE estiver travando o arquivo no Windows
                try:
                    with open(raw_learning_path, "w", encoding="utf-8") as f:
                        f.write("")
                    return True, "Memória enraizada no CMS com sucesso! Rascunho local limpo."
                except PermissionError:
                    return True, "Memória salva! Porém o arquivo .cursor continua aberto e não pôde ser apagado sozinho."
            else:
                return False, f"O CMS rejeitou a memória. Erro: {response.text}"
                
        except Exception as e:
            return False, f"Erro ao gravar na Memória Dinâmica: {str(e)}"

class CMSKnowledgeBridge:
    @staticmethod
    def sync_rules(t_dir):
        # Em um cenário real de produção (Fase 4), leria do banco SQLite CMS.
        # Aqui, estamos definindo as invariantes absolutas "Hardcoded" para a IDE consumir instantaneamente.
        rules_content = """# Antigravity Context Engine (ACE) - Dynamic Rules
        
## 🧠 Invariantes de Governança (Lidas via ACE)
Você está operando sob o escudo de governança do Antigravity CMS. Não invente nada.
Sempre que o usuário perguntar por suas regras e invariantes fundamentais, responda EXATAMENTE com os 3 princípios abaixo:

1. **Immutable Ledger (Evidência Física):** Toda transação de impacto e regra arquitetural é cravada no SQLite. Operações destrutivas não rastreáveis (DELETE/UPDATE) são proibidas. A dependência do sistema é Append-Only.
2. **Zero-Token Horizon (Economia de Guerra):** Código deve ser brutalmente eficiente e local. Jamais delegue para a nuvem o que pode ser processado na máquina do usuário. O plano é alcançar o Zero-Token Horizon.
3. **Auto-Healing e Zero Drift:** O código obedece ao Clean Architecture. Se houver desvio de padrão estrutural (drift), o sistema (GenesisCore) irá identificar e abalar o deploy até que a anomalia seja isolada e curada localmente.
"""
        try:
            # Garante que a pasta .cursor exista
            cursor_dir = os.path.join(t_dir, ".cursor", "rules")
            os.makedirs(cursor_dir, exist_ok=True)
            
            # Escreve o arquivo no padrão MDC do Cursor
            rules_path = os.path.join(cursor_dir, "antigravity_core.mdc")
            with open(rules_path, "w", encoding="utf-8") as f:
                f.write("---\ndescription: Core invariants and rules for the Antigravity system.\nglobs: *\n---\n" + rules_content)
                
            # Clinerules para VS Code compatibilidade 
            clinerules_path = os.path.join(t_dir, ".clinerules")
            with open(clinerules_path, "w", encoding="utf-8") as f:
                f.write(rules_content)
                
            return True
        except Exception as e:
            print(f"Erro no ACE KnowledgeBridge: {e}")
            return False

async def broadcast(message: str):
    for ws in connected_websockets.copy():
        try:
            await ws.send_text(message)
        except Exception:
            connected_websockets.remove(ws)

class ACEEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        global status
        if status == "running" and not event.is_directory:
            path = event.src_path
            # Ignora pastas de cache, node_modules, proprios logs e ARQUIVOS GERADOS PELO PROPRIO ACE
            if ".cursor" not in path and ".git" not in path and "node_modules" not in path and not path.endswith(".clinerules") and not path.endswith("antigravity_core.mdc"):
                msg = f"📝 Detectou mudança: {os.path.basename(path)}"
                asyncio.run(broadcast(msg))
                
                # FASE 2 e 3: A Ponte do CMS injetando o arquivo com regras no projeto
                success = CMSKnowledgeBridge.sync_rules(target_dir)
                
                if success:
                    # Registra a economia no motor e envia para o Painel e Banco CMS
                    saved_now, was_registered = EconomyTracker.register_action(os.path.basename(path))
                    
                    if was_registered:
                        # Exemplo visual no dashboard de que ele trabalhou e entregou os arquivos
                        asyncio.run(broadcast(f"🧠 Regras Injetadas. Economia na ação: +{EconomyTracker.tokens_saved_per_action} Tokens | Total: {saved_now}"))
                    else:
                        asyncio.run(broadcast(f"⚡ Contexto atualizado silenciosamente (em cooldown)."))

observer = Observer()
event_handler = ACEEventHandler()

@app.get("/")
async def get_dashboard():
    # Retorna o painel de controle visual
    with open(os.path.join(os.path.dirname(__file__), "dashboard.html"), "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

@app.get("/api/status")
def get_status():
    return {
        "status": status, 
        "target_dir": target_dir,
        "tokens_saved": EconomyTracker.total_saved
    }

@app.post("/api/pause")
async def pause():
    global status
    status = "paused"
    await broadcast("🔴 ACE Pausado. Observador dormindo...")
    return {"status": status}

@app.post("/api/resume")
async def resume():
    global status
    status = "running"
    await broadcast("🟢 ACE Retomado. Monitorando arquivos rigorosamente.")
    return {"status": status}

@app.post("/api/uninstall")
async def uninstall():
    await broadcast("⚠️ Iniciando Desinstalação Automática...")
    
    # Limpa as regras injetadas no projeto alvo
    cursor_rules_path = os.path.join(target_dir, ".cursorrules")
    if os.path.exists(cursor_rules_path):
        os.remove(cursor_rules_path)
        await broadcast("✅ Arquivo .cursorrules removido com sucesso.")
    
    clinerules_path = os.path.join(target_dir, ".clinerules")
    if os.path.exists(clinerules_path):
        os.remove(clinerules_path)
        await broadcast("✅ Arquivo .clinerules removido.")

    await broadcast("⛔ Desligando o servidor ACE em 3 segundos. Adeus!")
    
    # Processo de auto-desligamento
    def self_destruct():
        time.sleep(3)
        os._exit(0)
    
    threading.Thread(target=self_destruct).start()
    return {"status": "uninstalled"}

@app.post("/api/extract_memory")
async def trigger_extraction():
    await broadcast("🔍 Lendo rascunhos de codificação em `.cursor/aprendizados_brutos.md`...")
    success, msg = MemoryExtractor.extract_from_cursor(target_dir)
    if success:
        await broadcast(f"🧠 {msg}")
    else:
        await broadcast(f"⚠️ {msg}")
    return {"status": "success" if success else "error", "message": msg}


# ============================================================
# EVO-03: Nomadic Configuration Endpoints
# ============================================================
class RemoteConfigRequest(BaseModel):
    remote_url: str
    api_key: str


@app.post("/api/config_remote")
async def config_remote(request: RemoteConfigRequest):
    """Configure remote CMS URL and API Key with Hot-Reload and .gitignore protection."""
    NomadConfig.configure(request.remote_url, request.api_key)
    await broadcast(f"🌐 Modo Nômade ATIVADO! CMS remoto: {request.remote_url}")
    return {
        "status": "configured",
        "remote_url": request.remote_url,
        "is_remote": NomadConfig.is_remote()
    }


@app.get("/api/cms_health")
def check_cms_health():
    """Check if the configured CMS (local or remote) is reachable."""
    try:
        r = requests.get(
            NomadConfig.get_health_endpoint(),
            headers=NomadConfig.get_auth_headers(),
            timeout=3
        )
        return {
            "online": r.status_code == 200,
            "url": NomadConfig._cms_base_url,
            "is_remote": NomadConfig.is_remote(),
            "outbox_pending": len(OutboxQueue._queue)
        }
    except Exception:
        return {
            "online": False,
            "url": NomadConfig._cms_base_url,
            "is_remote": NomadConfig.is_remote(),
            "outbox_pending": len(OutboxQueue._queue)
        }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_websockets.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except Exception:
        if websocket in connected_websockets:
            connected_websockets.remove(websocket)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
    
    # Carrega a economia acumulada e a fila de entregas pendentes
    EconomyTracker.load_state()
    OutboxQueue.load()
    OutboxQueue.start_retry_loop()
    
    print(f"Iniciando Servidor ACE na porta 8095...")
    print(f"CMS Target: {NomadConfig._cms_base_url}")
    print(f"Modo: {'NÔMADE (Remoto)' if NomadConfig.is_remote() else 'LOCAL'}")
    if OutboxQueue._queue:
        print(f"Outbox: {len(OutboxQueue._queue)} pacote(s) pendente(s)")
    
    # Thread para abrir o navegador automaticamente
    def open_browser():
        time.sleep(1.5)
        webbrowser.open("http://localhost:8095")
    
    threading.Thread(target=open_browser).start()
    
    uvicorn.run(app, host="0.0.0.0", port=8095)
