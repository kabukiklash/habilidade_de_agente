import asyncio
import sys
import os

# Ensure paths point to Tecnologia 07 and 01
base_dir = "c:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente"
tech_07_path = os.path.join(base_dir, "07_KIMI_MEMORY_BRIDGE", "adapter")
sys.path.insert(0, tech_07_path)

from memory_adapter_master import memory_adapter

async def verify_fixes():
    print("[INFO] Verificando fix de encoding (Sem emojis)...")
    print("[SUCCESS] Se voce esta lendo isso, o encoding basico funcionou no Windows.")
    
    print("\n[INFO] Testando persistencia com event_id (dedupeKey)...")
    try:
        payload = {"test": "data", "priority": "high"}
        result = await memory_adapter.append_event(
            event_type="VERIFICATION_TEST",
            payload=payload,
            justification="Teste de verificacao apos fix de persistencia."
        )
        print(f"[SUCCESS] Evento gravado: {result}")
        
        if "event_id" in result:
            print(f"[INFO] Idempotency Key (event_id) gerada: {result['event_id']}")
        else:
            print("[ERROR] event_id ausente no resultado!")
            
    except Exception as e:
        print(f"[ERROR] Falha na persistencia: {e}")

if __name__ == "__main__":
    asyncio.run(verify_fixes())
