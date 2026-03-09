import re
import os

filepath = 'c:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente/llm_integration/kimi_client.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Update chat_thinking
pattern1 = r'''    async def chat_thinking\(self, prompt: str, system_msg: str = "You are a professional assistant with deep thinking capabilities\."\) -> str:
        """
        High-level helper for deep reasoning tasks\.
        """
        messages = \[
            \{"role": "system", "content": system_msg\},
            \{"role": "user", "content": prompt\}
        \]
        response = await self\.chat_completion\(messages, model="kimi-k2-turbo-preview", use_thinking=True\)
        return response\["choices"\]\[0\]\["message"\]\["content"\]'''
rep1 = '''    async def chat_thinking(self, prompt: str, system_msg: str = "You are a professional assistant with deep thinking capabilities.", return_usage: bool = False) -> str:
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
        return content'''
content = re.sub(pattern1, rep1, content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated kimi_client.py successfully!")
