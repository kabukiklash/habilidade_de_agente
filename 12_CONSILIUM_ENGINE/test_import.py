import sys
import os

print("Testando caminhos do Antigravity...")
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from llm_integration.consilium_engine import consilium
    print("✅ SUCESSO COGNITIVO: O consilium_engine mestre foi isolado e importado com sucesso a partir de 12_CONSILIUM_ENGINE!")
except Exception as e:
    print(f"❌ ERRO CRÍTICO NA EXTRAÇÃO: Falha ao inicializar o cortex: {e}")
    sys.exit(1)
