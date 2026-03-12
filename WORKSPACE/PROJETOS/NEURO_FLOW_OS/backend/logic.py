import math
from datetime import datetime
from typing import List, Dict, Any
from .models import NeuralTask, BrainState

class FocusScorer:
    @staticmethod
    def calculate(brain_state: BrainState) -> float:
        """
        Formula: focus = 0.6 * sigmoid(hrv - 30) + 0.3 * sigmoid(alpha_power - 1.2)
        Simplified for simulation.
        """
        def sigmoid(x):
            return 1 / (1 + math.exp(-x))
            
        hrv_factor = sigmoid(brain_state.hrv - 30)
        alpha_factor = sigmoid(brain_state.alpha_power - 1.2)
        
        # Base dopamine influencer (simulated)
        dopamine_factor = min(brain_state.dopamine_level / 10, 1.0)
        
        score = (0.5 * hrv_factor) + (0.3 * alpha_factor) + (0.2 * dopamine_factor)
        return round(score, 2)

class PriorityMatrix:
    @staticmethod
    def reorder(tasks: List[NeuralTask]) -> List[NeuralTask]:
        """
        Formula: (Impact * CognitiveWeight) / Inércia
        """
        now = datetime.utcnow()
        for task in tasks:
            # Impact is simulated from metadata or cognitive weight for now
            impact = task.metadata.get("impact", 5)
            
            # Inertia: time since creation in hours (min 1h to avoid div zero)
            inertia = max((now - task.created_at).total_seconds() / 3600, 1.0)
            
            # Base priority
            base_priority = (impact * task.cognitive_weight) / inertia
            
            # Apply focus score as a boost if high
            task.priority = round(base_priority * (1 + task.focus_score), 2)
            
        return sorted(tasks, key=lambda x: x.priority, reverse=True)
