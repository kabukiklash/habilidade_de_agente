import os
import httpx
import json
import logging
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

logger = logging.getLogger("ClaudeClient")

class ClaudeClient:
    """
    Antigravity Claude Client.
    Supports Anthropic Messages API with async httpx.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        # Load environment specifically for Anthropic if .env.anthropic exists
        env_path = os.path.join(os.getcwd(), ".env.anthropic")
        if os.path.exists(env_path):
            load_dotenv(env_path)
        elif os.path.exists(os.path.join(os.getcwd(), ".env")):
             load_dotenv()
            
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.api_url = "https://api.anthropic.com/v1/messages"
        
        if not self.api_key:
            # We don't crash here, but warning if used without key
            logger.warning("ANTHROPIC_API_KEY not found in environment or .env.anthropic")

    async def chat_thinking(self, prompt: str, system_msg: str = "You are the Final Auditor and Supreme Judge of the AI Council.", model: str = "claude-3-5-sonnet-20241022", return_usage: bool = False) -> Any:
        """
        Claude reasoning/auditing mode.
        """
        if not self.api_key:
             return f"ERROR: ANTHROPIC_API_KEY missing. Claude cannot deliberate."

        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        payload = {
            "model": model,
            "max_tokens": 4096,
            "system": system_msg,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        
        async with httpx.AsyncClient(timeout=90.0) as client:
            try:
                response = await client.post(self.api_url, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
                
                content = data["content"][0]["text"]
                usage = {
                    "prompt_tokens": data["usage"]["input_tokens"],
                    "completion_tokens": data["usage"]["output_tokens"],
                    "total_tokens": data["usage"]["input_tokens"] + data["usage"]["output_tokens"]
                }
                
                if return_usage:
                    return content, usage
                return content
            except Exception as e:
                logger.error(f"Claude API Error: {e}")
                err_msg = f"ERROR: Claude deliberation failed. {e}"
                if return_usage:
                    return err_msg, {"total_tokens": 0}
                return err_msg

    async def chat_instant(self, prompt: str) -> str:
        """Fast response mode with Haiku."""
        return await self.chat_thinking(prompt, model="claude-3-haiku-20240307")

# Global singleton
claude_client = ClaudeClient()
