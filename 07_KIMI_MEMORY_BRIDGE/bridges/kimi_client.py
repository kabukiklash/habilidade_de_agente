"""
Kimi Client: Integration with Moonshot AI (Kimi-k2.5)
Specialized client for Agent Swarm and Thinking Mode capabilities.
"""
import httpx
import json
import os
from typing import Optional, List, Dict, Any, Union
from dotenv import load_dotenv

# Load environment variables
load_dotenv(".env.moonshot")

class KimiClient:
    """
    Client for Moonshot AI (Kimi) API.
    Compatible with OpenAI format but tuned for Kimi-specific features.
    """
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.moonshot.ai/v1"):
        self.api_key = api_key or os.getenv("MOONSHOT_API_KEY")
        self.base_url = base_url
        if not self.api_key:
            # Fallback Logger logic
            try:
                from .logger import logger
            except ImportError:
                class DummyLogger:
                    def info(self, m): print(f"[INFO] {m}")
                    def error(self, m): print(f"[ERROR] {m}")
                    def warning(self, m): print(f"[WARN] {m}")
                logger = DummyLogger()
            logger.warning("⚠️ MOONSHOT_API_KEY não configurada. Chamadas ao Kimi falharão, mas a infraestrutura básica foi carregada.")

    async def _request(self, method: str, endpoint: str, json_data: Optional[Dict] = None) -> Dict[str, Any]:
        """Generic requester for Moonshot API."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.request(
                method, 
                f"{self.base_url}/{endpoint}", 
                headers=headers, 
                json=json_data
            )
            if response.status_code != 200:
                try:
                    error_detail = response.json()
                except:
                    error_detail = response.text
                raise Exception(f"Moonshot API Error ({response.status_code}): {json.dumps(error_detail)}")
            return response.json()

    async def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        model: str = "kimi-latest",
        temperature: float = 0.3,
        max_tokens: int = 4096,
        stream: bool = False,
        use_thinking: bool = False
    ) -> Dict[str, Any]:
        """
        Generic chat completion.
        If use_thinking is True, it will attempt to use specialized thinking models if supported.
        """
        if use_thinking:
            # Fallback to thinking-ready model if available
            target_model = "kimi-k2-thinking" if model == "kimi-latest" else model
        else:
            target_model = model

        payload = {
            "model": target_model,
            "messages": messages,
            "temperature": 1.0 if "kimi-k" in target_model else temperature,
            "max_tokens": max_tokens,
            "stream": stream
        }
        
        return await self._request("POST", "chat/completions", payload)

    async def list_models(self) -> List[Dict[str, Any]]:
        """List available Moonshot models."""
        result = await self._request("GET", "models")
        return result.get("data", [])

    async def chat_thinking(self, prompt: str, system_msg: str = "You are a professional assistant with deep thinking capabilities.", return_usage: bool = False) -> str:
        """
        High-level helper for deep reasoning tasks.
        """
        messages = [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": prompt}
        ]
        response = await self.chat_completion(messages, model="kimi-k2-turbo-preview", use_thinking=True)
        content = response["choices"][0]["message"]["content"]
        if return_usage:
            return content, response.get("usage", {})
        return content

    async def chat_instant(self, prompt: str) -> str:
        """
        High-level helper for fast, routine tasks.
        """
        messages = [{"role": "user", "content": prompt}]
        response = await self.chat_completion(messages, model="kimi-k2-turbo-preview", temperature=0.7)
        return response["choices"][0]["message"]["content"]

# Global convenience instance
kimi_client = KimiClient()
