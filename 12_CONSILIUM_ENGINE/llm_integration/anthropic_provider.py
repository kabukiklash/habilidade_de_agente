import os
import json
import time
import uuid
import logging
import urllib.request
import urllib.error
from .models import LLMRequest, LLMResponse, LLMUsage
from .provider import LLMProvider

# Logger configuration
logger = logging.getLogger("AnthropicProvider")
logger.setLevel(logging.INFO)

class AnthropicProvider(LLMProvider):
    def __init__(self, api_key_env="ANTHROPIC_API_KEY", timeout=30, max_retries=3):
        self.api_key = os.environ.get(api_key_env)
        self.timeout = timeout
        self.max_retries = max_retries
        self.api_url = "https://api.anthropic.com/v1/messages"
        
        if not self.api_key:
            logger.error(f"Missing environment variable: {api_key_env}")

    def _sanitize_log(self, data: dict) -> str:
        sanitized = data.copy()
        if "messages" in sanitized:
            sanitized["messages"] = "[CONTENT PURGED FOR SECURITY]"
        return json.dumps(sanitized)

    def generate(self, request: LLMRequest) -> LLMResponse:
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY is not set.")

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
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }

        logger.info(f"Sending request {request_id}. Payload: {self._sanitize_log(payload)}")

        last_error = None
        for attempt in range(self.max_retries + 1):
            try:
                req = urllib.request.Request(
                    self.api_url, 
                    data=json.dumps(payload).encode("utf-8"), 
                    headers=headers,
                    method="POST"
                )
                
                with urllib.request.urlopen(req, timeout=self.timeout) as response:
                    res_data = json.loads(response.read().decode("utf-8"))
                    
                    usage_data = res_data.get("usage", {})
                    usage = LLMUsage(
                        prompt_tokens=usage_data.get("input_tokens", 0),
                        completion_tokens=usage_data.get("output_tokens", 0),
                        total_tokens=usage_data.get("input_tokens", 0) + usage_data.get("output_tokens", 0)
                    )

                    content = res_data.get("content", [])
                    text = content[0].get("text", "") if content else ""

                    return LLMResponse(
                        text=text,
                        usage=usage,
                        request_id=request_id,
                        model=request.model,
                        metadata={"res_id": res_data.get("id")}
                    )

            except urllib.error.HTTPError as e:
                error_body = e.read().decode("utf-8")
                last_error = f"HTTP Error {e.code}: {error_body}"
                logger.warning(f"Attempt {attempt + 1} failed for {request_id}: {last_error}")
                
                if e.code in [429, 500, 502, 503, 504]:
                    time.sleep(1 * (attempt + 1))
                    continue
                break
            except Exception as e:
                last_error = str(e)
                logger.warning(f"Attempt {attempt + 1} failed for {request_id}: {last_error}")
                time.sleep(1 * (attempt + 1))

        raise Exception(f"Failed to generate after {self.max_retries} retries. Last error: {last_error}")
