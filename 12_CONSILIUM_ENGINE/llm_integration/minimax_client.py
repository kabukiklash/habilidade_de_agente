import os
import httpx
import logging
from typing import Optional
from dotenv import load_dotenv

logger = logging.getLogger("MinimaxClient")

class MinimaxClient:
    """
    Antigravity Minimax Client.
    Supports chat completions using the official API (api.minimax.chat).
    """
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        env_path = os.path.join(os.getcwd(), ".env")
        if os.path.exists(env_path):
            load_dotenv(env_path)
            
        self.api_key = api_key or os.getenv("MINIMAX_API_KEY")
        self.base_url = base_url or os.getenv("MINIMAX_BASE_URL", "https://api.minimax.chat/v1")
        
        if not self.api_key:
            logger.warning("MINIMAX_API_KEY not found. Please provide it or set it in sua raiz .env")

    async def chat_thinking(self, prompt: str, system_msg: str = "You are a Research Strategist.", model: str = "abab6.5s-chat") -> str:
        """
        Deep thinking mode using Minimax.
        """
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.5
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(url, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
            except Exception as e:
                logger.error(f"Minimax API Error: {e}")
                return f"ERROR: Minimax deliberation failed. {e}"

# Global singleton
minimax_client = MinimaxClient()
