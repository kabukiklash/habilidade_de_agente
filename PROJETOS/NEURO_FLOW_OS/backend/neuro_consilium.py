import sys
import os
from typing import List, Dict, Any

# Add libs to path for self-contained execution
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "libs")))

from llm_integration import consilium
from .models import NeuralTask

class NeuroConsilium:
    """
    Sovereign wrapper for Neuro-Flow OS deliberations.
    Uses the Council to validate task priority and cognitive weight.
    """
    
    @staticmethod
    async def deliberate_task(task: NeuralTask) -> Dict[str, Any]:
        prompt = f"""
        Tarefa: {task.title}
        Peso Cognitivo: {task.cognitive_weight}
        Prioridade Calculada: {task.priority}
        
        Veredito do Concílio: Validar se esta tarefa é adequada para o estado neural e business impact.
        """
        
        # In a real scenario, we gather evidence from the ledger
        evidence_files = [] 
        
        try:
            result = await consilium.deliberate(prompt, evidence_files)
            return result
        except Exception as e:
            return {"error": str(e), "verdict": "Offline Deliberation mode active."}

# Global singleton
neuro_consilium = NeuroConsilium()
