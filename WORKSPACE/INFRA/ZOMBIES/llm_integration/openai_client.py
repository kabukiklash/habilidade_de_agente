import os
import httpx
import json
import logging
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

logger = logging.getLogger("OpenAIClient")

class OpenAIClient:
    """
    Antigravity OpenAI Client.
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
            raise ValueError("OPENAI_API_KEY not found. Please provide it or set it in .env.openai")

    async def chat_thinking(self, prompt: str, system_msg: str = "You are a helpful assistant.", model: str = "o3-mini") -> str:
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
            try:
                response = await client.post(url, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
            except Exception as e:
                logger.error(f"OpenAI API Error: {e}")
                return f"ERROR: OpenAI deliberation failed. {e}"

    async def chat_instant(self, prompt: str, model: str = "gpt-4o-mini") -> str:
        """
        Fast response mode.
        """
        return await self.chat_thinking(prompt, system_msg="You are a precise technical analyst.", model=model)

# Global singleton
openai_client = OpenAIClient()
