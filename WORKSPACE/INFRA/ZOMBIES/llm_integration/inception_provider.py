import os
import json
import time
import uuid
import logging
import httpx
from dotenv import load_dotenv
from .models import LLMRequest, LLMResponse, LLMUsage
from .provider import LLMProvider

# Load environment variables (Local first)
load_dotenv(".env.inception")

# Logger configuration
logger = logging.getLogger("InceptionProvider")
logger.setLevel(logging.INFO)

class InceptionProvider(LLMProvider):
    """
    Provider for Inception Labs Mercury models.
    Compatible with the chat/completions OpenAI-style endpoint.
    """
    def __init__(self, api_key_env="INCEPTION_API_KEY", timeout=60, max_retries=3):
        self.api_key = os.environ.get(api_key_env)
        self.timeout = timeout
        self.max_retries = max_retries
        self.api_url = os.environ.get("INCEPTION_BASE_URL", "https://api.inceptionlabs.ai/v1") + "/chat/completions"
        
        if not self.api_key:
            logger.error(f"Missing environment variable: {api_key_env}")

    def _sanitize_log(self, data: dict) -> str:
        sanitized = data.copy()
        if "messages" in sanitized:
            sanitized["messages"] = "[CONTENT PURGED FOR SECURITY]"
        return json.dumps(sanitized)

    def generate(self, request: LLMRequest) -> LLMResponse:
        """
        Synchronous generation wrapper (as per LLMProvider interface).
        In Antigravity, we prefer async, but we maintain the base interface.
        """
        import asyncio
        try:
            # Check if an event loop is already running
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # This is tricky in a sync wrapper. For now, we'll use a local sync client.
                return self._generate_sync(request)
            else:
                return loop.run_until_complete(self.generate_async(request))
        except RuntimeError:
            # No loop running, create one
            return asyncio.run(self.generate_async(request))

    def _generate_sync(self, request: LLMRequest) -> LLMResponse:
        if not self.api_key:
            raise ValueError("INCEPTION_API_KEY is not set.")

        request_id = request.request_id or str(uuid.uuid4())
        
        payload = {
            "model": request.model,
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
            "messages": [
                {"role": "user", "content": request.prompt}
            ],
            **request.options
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        logger.info(f"Sending request {request_id}. Payload: {self._sanitize_log(payload)}")

        last_error = None
        for attempt in range(self.max_retries + 1):
            try:
                with httpx.Client(timeout=self.timeout) as client:
                    response = client.post(
                        self.api_url, 
                        json=payload, 
                        headers=headers
                    )
                    
                    if response.status_code != 200:
                        last_error = f"HTTP Error {response.status_code}: {response.text}"
                        if response.status_code in [429, 500, 502, 503, 504]:
                            time.sleep(1 * (attempt + 1))
                            continue
                        break

                    res_data = response.json()
                    
                    usage_data = res_data.get("usage", {})
                    usage = LLMUsage(
                        prompt_tokens=usage_data.get("prompt_tokens", 0),
                        completion_tokens=usage_data.get("completion_tokens", 0),
                        total_tokens=usage_data.get("total_tokens", 0)
                    )

                    choices = res_data.get("choices", [])
                    text = choices[0].get("message", {}).get("content", "") if choices else ""

                    return LLMResponse(
                        text=text,
                        usage=usage,
                        request_id=request_id,
                        model=request.model,
                        metadata={"res_id": res_data.get("id")}
                    )

            except Exception as e:
                last_error = str(e)
                logger.warning(f"Attempt {attempt + 1} failed for {request_id}: {last_error}")
                time.sleep(1 * (attempt + 1))

        raise Exception(f"Failed to generate after {self.max_retries} retries. Last error: {last_error}")

    async def generate_async(self, request: LLMRequest) -> LLMResponse:
        if not self.api_key:
            raise ValueError("INCEPTION_API_KEY is not set.")

        request_id = request.request_id or str(uuid.uuid4())
        
        payload = {
            "model": request.model,
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
            "messages": [
                {"role": "user", "content": request.prompt}
            ],
            **request.options
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        logger.info(f"Sending async request {request_id}. Payload: {self._sanitize_log(payload)}")

        last_error = None
        for attempt in range(self.max_retries + 1):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.post(
                        self.api_url, 
                        json=payload, 
                        headers=headers
                    )
                    
                    if response.status_code != 200:
                        last_error = f"HTTP Error {response.status_code}: {response.text}"
                        if response.status_code in [429, 500, 502, 503, 504]:
                            await asyncio.sleep(1 * (attempt + 1))
                            continue
                        break

                    res_data = response.json()
                    
                    usage_data = res_data.get("usage", {})
                    usage = LLMUsage(
                        prompt_tokens=usage_data.get("prompt_tokens", 0),
                        completion_tokens=usage_data.get("completion_tokens", 0),
                        total_tokens=usage_data.get("total_tokens", 0)
                    )

                    choices = res_data.get("choices", [])
                    text = choices[0].get("message", {}).get("content", "") if choices else ""

                    return LLMResponse(
                        text=text,
                        usage=usage,
                        request_id=request_id,
                        model=request.model,
                        metadata={"res_id": res_data.get("id")}
                    )

            except Exception as e:
                last_error = str(e)
                logger.warning(f"Attempt {attempt + 1} failed for {request_id}: {last_error}")
                await asyncio.sleep(1 * (attempt + 1))

        raise Exception(f"Failed to generate after {self.max_retries} retries. Last error: {last_error}")
