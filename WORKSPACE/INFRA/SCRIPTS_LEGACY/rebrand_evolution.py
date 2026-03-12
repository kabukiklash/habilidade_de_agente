import os

def rebrand_files(root_path):
    replacements = {
        "ANTIGRAVITY": "EVOLUTION",
        "Antigravity": "Evolution",
        "antigravity": "evolution"
    }
    
    for root, dirs, files in os.walk(root_path):
        for name in files:
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
                    print(f"✅ Updated: {filepath}")
            except Exception as e:
                print(f"❌ Failed to process {filepath}: {e}")

if __name__ == "__main__":
    template_path = "c:\\Users\\RobsonSilva-AfixGraf\\Habilidade_de_agente\\ANTIGRAVITY_SOVEREIGN_TEMPLATE"
    rebrand_files(template_path)
