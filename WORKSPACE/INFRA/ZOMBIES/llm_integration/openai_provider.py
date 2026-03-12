from typing import Dict, Any, Optional
import asyncio
from .provider import LLMProvider
from .models import LLMRequest, LLMResponse, LLMUsage
from .openai_client import openai_client

class OpenAIProvider(LLMProvider):
    """
    OpenAI Provider for Antigravity.
    Follows the Zero-Trust and Passive-Only policy.
    """
    
    def __init__(self, model: str = "gpt-4o"):
        self.model = model
        self.client = openai_client

    def generate(self, request: LLMRequest) -> LLMResponse:
        """
        Synchronous wrapper for generate.
        """
        return asyncio.run(self.generate_async(request))

    async def generate_async(self, request: LLMRequest) -> LLMResponse:
        """
        Asynchronous generation.
        """
        # Passive-Only: The provider only analyzes, never executes.
        # This is enforced by the prompt context in higher layers.
        
        system_msg = "You are a specialized Antigravity Council Member. Provide logical, evidenced-based reasoning."
        
        try:
            response_text = await self.client.chat_thinking(
                prompt=request.prompt,
                system_msg=system_msg,
                model=self.model
            )
            
            # OpenAI costs vary, for now we return a generic usage or estimate
            # (In a real scenario, we'd parse this from the API response)
            usage = LLMUsage(prompt_tokens=0, completion_tokens=0, total_tokens=0)
            
            return LLMResponse(
                text=response_text,
                model=self.model,
                usage=usage,
                provider="openai"
            )
        except Exception as e:
            return LLMResponse(
                text=f"OpenAI Provider Error: {e}",
                model=self.model,
                usage=LLMUsage(0, 0, 0),
                provider="openai"
            )

# Convenience instance
openai_provider = OpenAIProvider()
