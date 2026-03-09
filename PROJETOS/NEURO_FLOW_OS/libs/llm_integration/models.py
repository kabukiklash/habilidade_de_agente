from dataclasses import dataclass, field
from typing import Dict, Any, Optional

@dataclass
class LLMRequest:
    prompt: str
    model: str = "claude-3-5-sonnet-latest"
    temperature: float = 0.7
    max_tokens: int = 4096
    options: Dict[str, Any] = field(default_factory=dict)
    request_id: Optional[str] = None

@dataclass
class LLMUsage:
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0

@dataclass
class LLMResponse:
    text: str
    usage: LLMUsage
    request_id: str
    model: str
    metadata: Dict[str, Any] = field(default_factory=dict)
