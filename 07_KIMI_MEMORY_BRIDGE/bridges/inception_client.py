"""
Inception Client: Integration with Inception Labs (Mercury-2)
Specialized client for high-performance reasoning tasks.
"""
import httpx
import json
import os
from typing import Optional, List, Dict, Any, Union
from dotenv import load_dotenv

# Load environment variables
load_dotenv(".env.inception")

class InceptionClient:
    """
    Client for Inception Labs API.
    Compatible with OpenAI chat completion format.
    """
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.inceptionlabs.ai/v1"):
        self.api_key = api_key or os.getenv("INCEPTION_API_KEY")
        self.base_url = base_url
        if not self.api_key:
            # Fallback to check if it's already in the environment without load_dotenv
            self.api_key = os.environ.get("INCEPTION_API_KEY")
            
        if not self.api_key:
            # Silently fail initialization to avoid crashing the whole system if key is missing
            # But log it if used.
            pass

    async def _request(self, method: str, endpoint: str, json_data: Optional[Dict] = None) -> Dict[str, Any]:
        """Generic requester for Inception API."""
        if not self.api_key:
            raise ValueError("INCEPTION_API_KEY not found. Please set it in .env.inception")

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
                raise Exception(f"Inception API Error ({response.status_code}): {json.dumps(error_detail)}")
            return response.json()

    async def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        model: str = "mercury-2",
        temperature: float = 0.7,
        max_tokens: int = 4096,
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        Generic chat completion for Inception Mercury models.
        """
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream
        }
        
        return await self._request("POST", "chat/completions", payload)

    async def chat_instant(self, prompt: str, model: str = "mercury-2") -> str:
        """
        High-level helper for fast, routine tasks using Inception.
        """
        messages = [{"role": "user", "content": prompt}]
        response = await self.chat_completion(messages, model=model)
        return response["choices"][0]["message"]["content"]

    async def chat_thinking(self, prompt: str, system_msg: str = "You are a highly capable AI assistant.", return_usage: bool = False, model: str = "mercury-2") -> str:
        """
        High-level helper for reasoning tasks using Inception.
        """
        messages = [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": prompt}
        ]
        response = await self.chat_completion(messages, model=model)
        content = response["choices"][0]["message"]["content"]
        if return_usage:
            return content, response.get("usage", {})
        return content

# Global convenience instance
inception_client = InceptionClient()
