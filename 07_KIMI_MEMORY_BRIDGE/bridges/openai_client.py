import os
import httpx
import json
import logging
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

logger = logging.getLogger("OpenAIClient")

class OpenAIClient:
    """
    Evolution OpenAI Client.
    Supports chat completions and deep reasoning models (o1/o3-mini).
    """
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        # Load environment specifically for OpenAI if .env.openai exists
        env_path = os.path.join(os.getcwd(), ".env.openai")
        if os.path.exists(env_path):
            load_dotenv(env_path)
            
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        
        if not self.api_key:
            # Fallback Logger logic for standalone execution
            try:
                from .logger import logger
            except ImportError:
                class DummyLogger:
                    def info(self, m): print(f"[INFO] {m}")
                    def error(self, m): print(f"[ERROR] {m}")
                    def warning(self, m): print(f"[WARN] {m}")
                logger = DummyLogger()
            logger.warning("[WARN] OPENAI_API_KEY nao configurada. Chamadas ao OpenAI falharao, mas a infraestrutura basica foi carregada.")

    async def chat_thinking(self, prompt: str, system_msg: str = "You are a helpful assistant.", model: str = "o3-mini", return_usage: bool = False) -> str:
        """
        Deep thinking mode using OpenAI models.
        """
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # o1/o3-mini specific handling if needed, but standard chat completion usually works
        payload = {
            "model": model,
            "messages": [
                {"role": "developer", "content": system_msg} if model.startswith("o") else {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt}
            ]
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            if return_usage:
                return content, data.get("usage", {})
            return content

    async def chat_instant(self, prompt: str, model: str = "gpt-4o-mini") -> str:
        """
        Fast response mode.
        """
        return await self.chat_thinking(prompt, system_msg="You are a precise technical analyst.", model=model)

# Global singleton
openai_client = OpenAIClient()
