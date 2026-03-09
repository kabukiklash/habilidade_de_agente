import os

def rebrand_artifacts(root_path):
    replacements = {
        "ANTIGRAVITY": "EVOLUTION",
        "Antigravity": "Evolution",
        "antigravity": "evolution"
    }
    
    for root, dirs, files in os.walk(root_path):
        for name in files:
            if name.endswith(".md"):
                filepath = os.path.join(root, name)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    new_content = content
                    for old, new in replacements.items():
                        new_content = new_content.replace(old, new)
                    
                    if new_content != content:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"✅ Updated Artifact: {filepath}")
                except Exception as e:
                    print(f"❌ Failed to process artifact {filepath}: {e}")

if __name__ == "__main__":
    brain_path = "C:\\Users\\RobsonSilva-AfixGraf\\.gemini\\antigravity\\brain\\460d72a8-2989-42ce-82e1-2e5e5665e46d"
    rebrand_artifacts(brain_path)
