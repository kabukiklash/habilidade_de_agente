import re

filepath = 'c:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente/cognitive-memory-service/dashboard/index.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Make the token economy banner a clickable link with hover effects
pattern = r'''    <!-- TOKEN ECONOMY HIGHLIGHT -->
    <div style="max-width: 1200px; margin: 0 auto 2rem auto; padding: 0 4rem;">
        <div
            style="background: linear-gradient\(135deg, rgba\(0, 255, 136, 0.1\) 0%, rgba\(0, 255, 136, 0.02\) 100%\); border: 1px solid rgba\(0, 255, 136, 0.3\); border-radius: 24px; padding: 2.5rem; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 10px 30px rgba\(0, 255, 136, 0.05\);">'''

rep = '''    <style>
        .token-block-link {
            text-decoration: none;
            display: block;
            margin: 0 auto 2rem auto;
            max-width: 1200px;
            padding: 0 4rem;
        }
        .token-block {
            background: linear-gradient(135deg, rgba(0, 255, 136, 0.1) 0%, rgba(0, 255, 136, 0.02) 100%);
            border: 1px solid rgba(0, 255, 136, 0.3);
            border-radius: 24px;
            padding: 2.5rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: 0 10px 30px rgba(0, 255, 136, 0.05);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .token-block:hover {
            border-color: #00ff88;
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0, 255, 136, 0.15);
        }
    </style>
    <!-- TOKEN ECONOMY HIGHLIGHT -->
    <a href="token_ledger.html" class="token-block-link">
        <div class="token-block">'''

content = re.sub(pattern, rep, content)

# update the closing div of the block
pattern2 = r'''                    <div
                        style="font-family: 'JetBrains Mono'; font-size: 0.8rem; color: var\(--primary\); letter-spacing: 1px; margin-top: 5px;">
                        MAIS EFICIENTE</div>
                </div>
            </div>
        </div>
    </div>'''
rep2 = '''                    <div
                        style="font-family: 'JetBrains Mono'; font-size: 0.8rem; color: var(--primary); letter-spacing: 1px; margin-top: 5px;">
                        MAIS EFICIENTE</div>
                </div>
            </div>
        </div>
    </a>'''

content = re.sub(pattern2, rep2, content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated index.html to link to token_ledger.html")
