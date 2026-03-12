from typing import Dict, Any
from .logger import logger

class ROIEngine:
    """
    Calculadora de Retorno sobre Investimento (ROI) e Economia de Tokens.
    """
    
    def __init__(self):
        # Preços por 1k tokens (Estimados - Fevereiro 2026)
        self.prices = {
            "kimi-k2-turbo-preview": {"input": 0.005, "output": 0.015},
            "o3-mini": {"input": 0.01, "output": 0.03},
            "claude-3-5-sonnet": {"input": 0.003, "output": 0.015},
            "default": {"input": 0.01, "output": 0.03}
        }

    def calculate_savings(self, model_name: str, raw_tokens: int, curated_tokens: int) -> Dict[str, Any]:
        """
        Calcula a economia em tokens e em USD.
        """
        saved_tokens = max(0, raw_tokens - curated_tokens)
        
        price_info = self.prices.get(model_name, self.prices["default"])
        usd_saved = (saved_tokens / 1000) * price_info["input"]
        
        return {
            "tokens_saved": saved_tokens,
            "usd_saved": round(usd_saved, 6),
            "efficiency_gain": round((saved_tokens / max(1, raw_tokens)) * 100, 2)
        }

# Global Instance
roi_engine = ROIEngine()
