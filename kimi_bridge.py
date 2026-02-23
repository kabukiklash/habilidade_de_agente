
import asyncio
import sys
import os

# Add parent directory to sys.path
sys.path.append(os.getcwd())

from llm_integration.cognitive_cortex import cognitive_cortex

async def main():
    user_prompt = sys.argv[1] if len(sys.argv) > 1 else "ola Kimi vc os conhecimentos das skills do antigravity? me diga"
    
    # We use solve_task which automatically queries CMS for context
    response = await cognitive_cortex.solve_task(user_prompt, context_query="habilidades e skills do antigravity")
    
    # Write response to a file with UTF-8 encoding
    with open("kimi_response.txt", "w", encoding="utf-8") as f:
        f.write(response)

if __name__ == "__main__":
    asyncio.run(main())
