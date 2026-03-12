from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional
import json

@dataclass
class ToolIntent:
    """
    Evolution Tool Intent: A proposal to use a tool.
    Strictly follows 'Passive-Only' governance.
    """
    tool_name: str
    arguments: Dict[str, Any]
    rationale: str
    risk_level: str  # 'READ_ONLY', 'LOW', 'MEDIUM', 'HIGH', 'DESTRUCTIVE'
    scope_restriction: Optional[str] = None
    
    def to_json(self) -> str:
        return json.dumps(asdict(self), sort_keys=True)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(**data)
