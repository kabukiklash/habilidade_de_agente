import time
import hashlib
import json
import os
from typing import Dict, Any, List, Optional

class LoopGuardMaster:
    """
    Motor de Proteção do ACE (TEC 14).
    Implementa 4 camadas de governança contra loops, redundâncias e burst.
    """
    
    def __init__(self):
        # Configurações de Watcher Guard
        self.ignored_patterns = [
            ".cursorrules", 
            ".clinerules", 
            "antigravity_core.mdc",
            ".ace_economy_state.json", 
            "outbox.json",
            ".agent/",
            ".git/",
            "node_modules/",
            "__pycache__"
        ]
        
        # Estado de Rate Limit
        self.action_history: List[float] = []
        self.MAX_ACTIONS_PER_MINUTE = 5
        
        # Estado de Semantic Dedup (Temporal + Structural Hash)
        self._recent_hashes: Dict[str, float] = {}
        self.DEDUP_WINDOW_SECONDS = 300 # 5 minutos para o mesmo insight
        
    def should_process_event(self, file_path: str, origin: str = "system") -> bool:
        """
        4.1 & 4.2: Source Guard + Watcher Guard
        Verifica se o evento deve ser processado.
        """
        # Ignora arquivos do próprio ecossistema ou gerados pelo ACE
        base_name = os.path.basename(file_path)
        
        if any(pattern in file_path for pattern in self.ignored_patterns):
            return False
            
        if origin == "ace":
            # ACE não pode processar eventos gerados por ele mesmo (Recursão Preventiva)
            return False
            
        return True

    def check_rate_limit(self) -> bool:
        """
        4.4: Rate Limit Guard
        Retorna True se estiver dentro do limite, False se exceder.
        """
        now = time.time()
        # Limpa histórico antigo (> 60s)
        self.action_history = [t for t in self.action_history if now - t < 60]
        
        if len(self.action_history) >= self.MAX_ACTIONS_PER_MINUTE:
            return False
            
        return True

    def register_action(self):
        self.action_history.append(time.time())

    def is_semantic_duplicate(self, content: str) -> bool:
        """
        4.3: Semantic Dedup Guard (MD5 Hash + Window)
        """
        if not content:
            return False
            
        content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
        now = time.time()
        
        last_seen = self._recent_hashes.get(content_hash, 0)
        
        if now - last_seen < self.DEDUP_WINDOW_SECONDS:
            return True
            
        # Atualiza o rastro
        self._recent_hashes[content_hash] = now
        # Limpeza periódica (opcional, para não crescer infinitamente)
        if len(self._recent_hashes) > 1000:
            self._recent_hashes = {k: v for k, v in self._recent_hashes.items() if now - v < self.DEDUP_WINDOW_SECONDS}
            
        return False

loop_guard = LoopGuardMaster()
