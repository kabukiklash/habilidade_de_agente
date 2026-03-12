from typing import List, Dict, Any, Tuple
from intent_schema import ToolIntent

class PolicyEngine:
    """
    Antigravity Policy Engine: The Guardian of Non-Agency.
    Enforces WORM-like safety on tool execution intents.
    """
    def __init__(self):
        self.allowlist = [
            "read_file", "list_dir", "grep_search", 
            "view_file", "view_file_outline", "view_code_item"
        ]
        self.restricted_paths = [
            "C:/Windows", "C:/Users/RobsonSilva-AfixGraf/AppData", ".env"
        ]
        self.risk_threshold = "MEDIUM" # Block anything higher automatically

    def validate_intent(self, intent: ToolIntent) -> Tuple[bool, str]:
        """
        Validates if a tool intent is safe for proposal.
        """
        # 1. Check Allowlist
        if intent.tool_name not in self.allowlist:
            return False, f"TOOL_NOT_ALLOWED: {intent.tool_name} is not in the audit allowlist."

        # 2. Check Path Restrictions (if applicable)
        if "path" in intent.arguments:
            path = intent.arguments["path"].replace("\\", "/")
            for restricted in self.restricted_paths:
                if restricted in path:
                    return False, f"SCOPE_VIOLATION: Access to {restricted} is prohibited."

        # 3. Check Risk Level
        risk_order = ["READ_ONLY", "LOW", "MEDIUM", "HIGH", "DESTRUCTIVE"]
        try:
            current_risk_idx = risk_order.index(intent.risk_level)
            threshold_idx = risk_order.index(self.risk_threshold)
            
            if current_risk_idx > threshold_idx:
                return False, f"RISC_TOO_HIGH: {intent.risk_level} exceeds threshold {self.risk_threshold}."
        except ValueError:
            return False, f"INVALID_RISK_LEVEL: {intent.risk_level}"

        return True, "INTENT_VALIDATED: Safe for audit proposal."

if __name__ == "__main__":
    # Test Policy Engine
    engine = PolicyEngine()
    
    # Safe Intent
    safe_intent = ToolIntent(
        tool_name="read_file",
        arguments={"path": "C:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente/README.md"},
        rationale="Verificar documentação.",
        risk_level="READ_ONLY"
    )
    
    # Risky Intent
    risky_intent = ToolIntent(
        tool_name="delete_file",
        arguments={"path": "C:/Important/Data.db"},
        rationale="Limpeza de disco.",
        risk_level="DESTRUCTIVE"
    )
    
    print(f"Safe Test: {engine.validate_intent(safe_intent)}")
    print(f"Risky Test: {engine.validate_intent(risky_intent)}")
