import argparse
import json
import urllib.request
import os

# Configuration
API_URL = "https://fees-str-producers-binary.trycloudflare.com/v1/chat/completions"
# Map aliases to actual model names loaded in LM Studio (this might need adjustment based on what's active)
MODEL_MAP = {
    "code-beast": "local-model", # LM Studio often exposes the active model as 'local-model'
    "logic-beast": "local-model",
    "creative-beast": "local-model"
}

def ask_local(prompt, model_alias="code-beast", temperature=0.7):
    model_name = MODEL_MAP.get(model_alias, "local-model")
    
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": f"You are {model_alias}. Respond concisely and accurately."},
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature,
        "max_tokens": 2000
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        req = urllib.request.Request(API_URL, data=json.dumps(payload).encode('utf-8'), headers=headers)
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            print(result['choices'][0]['message']['content'])
    except Exception as e:
        print(f"Error reaching Local Brain: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ask the Local Brain")
    parser.add_argument("--prompt", required=True, help="The prompt to send")
    parser.add_argument("--model", default="code-beast", help="Model alias: code-beast, logic-beast, creative-beast")
    args = parser.parse_args()
    
    ask_local(args.prompt, args.model)
