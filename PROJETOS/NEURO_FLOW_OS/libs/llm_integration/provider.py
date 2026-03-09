from abc import ABC, abstractmethod
from .models import LLMRequest, LLMResponse

class LLMProvider(ABC):
    """
    Base class for all LLM providers.
    Ensures a consistent interface and passive-only policy.
    """
    
    @abstractmethod
    def generate(self, request: LLMRequest) -> LLMResponse:
        """
        Generates a response from the LLM based on the request.
        Must handle retries, timeouts, and error sanitization internally.
        """
        pass
