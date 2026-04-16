import time
from typing import Dict, List, Optional
import os
import sys

# Sovereign Path Orchestration for Circuit Breaker
base_dir = r"c:\Users\RobsonSilva-AfixGraf\Habilidade_de_agente"
tech_cb_path = os.path.join(base_dir, "03_CIRCUIT_BREAKER_V3", "core")
if tech_cb_path not in sys.path:
    sys.path.insert(0, tech_cb_path)

try:
    from circuit_breaker_master import circuit_breaker
except ImportError:
    circuit_breaker = None

class LoopGuard:
    """
    Governor V4: Loop Guard (Recursive Protection).
    Monitors correlation_ids to detect and break infinite multi-agent loops.
    """
    def __init__(self, max_depth: int = 5, time_window_sec: float = 1.0):
        self.max_depth = max_depth
        self.time_window_sec = time_window_sec
        # Maps correlation_id -> List of timestamps
        self.history: Dict[str, List[float]] = {}
        
    def check_and_register(self, correlation_id: Optional[str]) -> bool:
        """
        Registers a call for the given correlation_id.
        Returns False if a recursive loop is detected (Kill-Switch activated), True otherwise.
        """
        if not correlation_id:
            return True
            
        now = time.time()
        
        if correlation_id not in self.history:
            self.history[correlation_id] = []
            
        # Clean up old timestamps outside the window
        self.history[correlation_id] = [
            ts for ts in self.history[correlation_id] 
            if now - ts <= self.time_window_sec
        ]
        
        # Register current call
        self.history[correlation_id].append(now)
        
        # Check depth
        if len(self.history[correlation_id]) > self.max_depth:
            # KILL-SWITCH: Trigger Circuit Breaker
            print(f"🚨 [Loop Guard] RECURSIVE LOOP DETECTED for ID {correlation_id}! ({len(self.history[correlation_id])} calls in {self.time_window_sec}s)")
            if circuit_breaker:
                circuit_breaker._open_breaker(f"Loop Guard Triggered: Recursive depth > {self.max_depth} for {correlation_id}")
            
            # Clean history to allow recovery after breaker cools down
            self.history[correlation_id] = []
            return False
            
        return True

# Global Singleton
loop_guard = LoopGuard()

if __name__ == "__main__":
    import asyncio
    
    async def run_tests():
        # Test Loop Guard
        print("[*] Testing Loop Guard...")
        guard = LoopGuard()
        
        # Simulate valid calls
        assert guard.check_and_register("req-123") == True
        time.sleep(0.1)
        assert guard.check_and_register("req-123") == True
        
        # Simulate recursive loop in < 1s
        for _ in range(5):
            guard.check_and_register("loop-999")
        
        # The 6th call should trigger the kill-switch
        is_safe = guard.check_and_register("loop-999")
        print(f"[+] 6th call safety check: {is_safe}")
        assert is_safe == False
        print("✅ Loop Guard test passed!")

    asyncio.run(run_tests())
