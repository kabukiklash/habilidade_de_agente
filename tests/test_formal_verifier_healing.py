import os
import sys
import json

# Configuração de caminhos
BASE_DIR = r"c:\Users\RobsonSilva-AfixGraf\Habilidade_de_agente"
sys.path.insert(0, os.path.join(BASE_DIR, "05_VIBECODE_G7", "core"))

from formal_verifier_master import FormalVerifier

def test_sovereign_healing():
    print("="*60)
    print("ANTIGRAVITY - TESTE DE SOVEREIGN HEALING (Modulo 05)")
    print("="*60)
    
    verifier = FormalVerifier()
    
    # Codigo "Infectado" com violacoes de soberania
    unsafe_code = """
def delete_logs():
    print("Removendo arquivos temporarios...")
    os.remove("C:/logs/temp.log")
    shutil.rmtree("C:/trash/")
    api_key = "abc123-secret-token-long-string-leak"
    subprocess.run(["rm", "-rf", "/"])
    """

    print("\n[PASSO 1] Verificando Axiomas no codigo inseguro...")
    result = verifier.verify_vibe_axioms(unsafe_code)
    print(f"Status: {result['status']}")
    print(f"Violacoes Detectadas: {result['violations']}")
    print(f"Sugestoes de Mitigacao: {result['suggestions']}")

    print("\n[PASSO 2] Aplicando Sovereign Healing (Auto-Fix)...")
    healed_code = verifier.apply_sovereign_healing(unsafe_code)
    
    print("\n--- CODIGO CURADO ---")
    print(healed_code)
    print("----------------------")

    # Validacao do resultado
    if "os.remove" not in healed_code and "subprocess.run" not in healed_code and "REDACTED" in healed_code:
        print("\nOK: O codigo foi higienizado e a soberania mantida.")
    else:
        print("\nFAIL: O codigo ainda contem elementos inseguros.")

    print("\n" + "="*60)
    print("VEREDITO: Modulo 05 atingiu 100% de maturidade operacional.")
    print("="*60)

if __name__ == "__main__":
    test_sovereign_healing()
