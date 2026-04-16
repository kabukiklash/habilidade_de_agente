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

        # Session Initialization Protocol (Governor V4 Phase 1)
        # Fetch active context before the decision
        try:
            import sys
            import os
            base_dir = r"c:\Users\RobsonSilva-AfixGraf\Habilidade_de_agente"
            tech_01_path = os.path.join(base_dir, "01_COGNITIVE_MEMORY_SERVICE", "client")
            if tech_01_path not in sys.path:
                sys.path.insert(0, tech_01_path)
                
            from cms_client_master import cms_client
            # Fetch active context
            context_res = await cms_client.query_memory("contexto ativo do projeto", vector_topk=3)
            facts = context_res.get("context", {}).get("facts", [])
            
            if facts:
                context_str = "\n".join([f"- {f.get('content', str(f))}" for f in facts])
                system_msg += f"\n\n[SOVEREIGN CONTEXT INJECTED]:\n{context_str}"
        except Exception as e:
            logger.warning(f"Failed to fetch initial context for Claude session: {e}")

        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        # Strict Tool Interface Contracts (Governor V4)
        SOVEREIGN_TOOLS = [
            {
                "name": "query_memory",
                "description": "Searches the Cognitive Memory Service (CMS). OUTPUT: Returns a JSON object with a 'context' key containing 'facts', 'artifacts', and 'links'. ERROR: Returns {'error': '...'} if unreachable. Do NOT infer results or hallucinate context.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The exact search term to query."
                        }
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "store_memory",
                "description": "Stores a new cognitive event. OUTPUT: Returns {'status': 'recorded', 'event_id': '...'} or {'status': 'deduplicated'} on success. ERROR: Returns {'error': '...'} on failure. Do NOT infer success.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "event_type": {
                            "type": "string",
                            "enum": ["KNOWLEDGE_SYNC", "GOAL_UPDATE", "DECISION_LOG"],
                            "description": "Classification of the event."
                        },
                        "payload": {
                            "type": "object",
                            "description": "The actual JSON knowledge payload."
                        },
                        "justification": {
                            "type": "string",
                            "description": "Explicit reason why this must be stored."
                        }
                    },
                    "required": ["event_type", "payload", "justification"]
                }
            }
        ]

        payload = {
            "model": model,
            "max_tokens": 4096,
            "system": system_msg,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "tools": SOVEREIGN_TOOLS
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
