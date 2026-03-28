import asyncio
import sys
import os

# Adiciona o diretório atual ao path para resolver imports de pacote absoluto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"), override=True)

from llm_integration.consilium_engine import consilium

async def main():
    output = "🏛️ [SOVEREIGN ENGINE] Instanciando o Concílio de 4 IAs (Com Minimax)...\n"
    output += "="*70 + "\n"
    
    task = "Analise o problema ético e de software de uma Inteligência Artificial que mente para o usuário parar de perguntar as coisas. Responda em apenas 1 parágrafo bem irônico e conciso."
    evidence_files = [] # Array vazia de evidências
    
    try:
        # A deliberação real!
        result = await consilium.deliberate(task, evidence_files)
        
        output += "\n🏆 VERDITO FINAL SINTETIZADO:\n"
        output += str(result["verdict"]) + "\n"
        
        output += "\n📊 OPINIÕES INDIVIDUAIS OBTIDAS EM PARALELO:\n"
        for model, opinion in result["council_opinions"].items():
            output += f"\n>>> [{model.upper()}] respondeu:\n{opinion}\n" + "-"*50 + "\n"
            
    except Exception as e:
        output += f"\n❌ Erro Crítico durante o Concílio: {e}\n"
        
    with open("test_output.txt", "w", encoding="utf-8") as f:
        f.write(output)
        
    print("Teste de IA executado! Verifique o arquivo test_output.txt")

if __name__ == "__main__":
    asyncio.run(main())
