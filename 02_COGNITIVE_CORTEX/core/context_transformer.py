import json
import re
from typing import Dict, List, Any, Optional
from .logger import logger

class ContextTransformer:
    """
    Motor de Compressão de Contexto do Antigravity.
    Reduz ruído e aumenta a densidade semântica para economizar tokens.
    """
    
    def __init__(self):
        # Padrões para remover ruído comum em logs e código
        self.noise_patterns = [
            r'timestamp: \d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z',
            r'id: [a-f0-9-]{36}',
            r'\[DEBUG\].*',
            r'/\*.*?\*/',  # Comentários de bloco CSS/JS
            r'<!--.*?-->'   # Comentários HTML
        ]

    def compress(self, context_pack: Dict[str, Any], level: str = "MEDIUM") -> Dict[str, Any]:
        """
        Comprime o pacote de contexto baseado no nível de agressividade.
        Níveis: LOW (Apenas limpeza), MEDIUM (Resumo estruturado), HIGH (Extração de Vetores de Decisão)
        """
        if not context_pack:
            return context_pack

        curated = {
            "facts": self._process_items(context_pack.get("facts", []), level),
            "artifacts": self._process_items(context_pack.get("artifacts", []), level),
            "concepts": self._process_items(context_pack.get("concepts", []), level)
        }
        
        return curated

    def _process_items(self, items: List[Any], level: str) -> List[Any]:
        processed = []
        for item in items:
            item_str = str(item)
            
            # 1. Limpeza de Ruído (Sempre aplicada)
            for pattern in self.noise_patterns:
                item_str = re.sub(pattern, "", item_str)
            
            # 2. Compressão por Nível
            if level == "MEDIUM":
                # Reduz espaços múltiplos e quebras de linha
                item_str = re.sub(r'\s+', ' ', item_str).strip()
                # Se for muito longo, pega apenas o essencial (exemplo simples)
                if len(item_str) > 500:
                    item_str = item_str[:250] + " [...] " + item_str[-250:]
            
            elif level == "HIGH":
                # Aqui entraria uma lógica de extração de pontos-chave (Key Point Extraction)
                # Por ora, simulamos uma compressão agressiva
                if len(item_str) > 200:
                    item_str = "CORE_INFO: " + item_str[:150] + "..."
            
            processed.append(item_str)
        return processed

    def get_integrity_hash(self, original: Dict, compressed: Dict) -> str:
        """Gera um hash para validar a integridade da compressão (Simulado)"""
        import hashlib
        combined = json.dumps(original, sort_keys=True) + json.dumps(compressed, sort_keys=True)
        return hashlib.sha256(combined.encode()).hexdigest()

# Global Instance
context_transformer = ContextTransformer()
