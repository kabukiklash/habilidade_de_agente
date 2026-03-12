import asyncio
import json
from datetime import datetime
from backend.models import NeuralTask, BrainState, FlowSession
from backend.logic import FocusScorer, PriorityMatrix
from backend.security import BioSecurity

async def simulate_saga():
    print("🧠 [SAGA] Iniciando Simulação do Ciclo de Vida NEURO-FLOW OS...")
    
    # 1. Autenticação Bio-JWT
    user_id = "eng_01"
    bio_digest = "digest_iris_ppg_8822"
    token = BioSecurity.generate_bio_jwt(user_id, bio_digest)
    print(f"✅ [BIO-AUTH] Usuário '{user_id}' autenticado. JWT gerado: {token[:20]}...")

    # 2. Início de Sessão (Deep Work)
    session = FlowSession(user_id=user_id, mode="deep_work")
    print(f"🚀 [SESSION] Modo DEEP WORK ativado. Início: {session.start_time}")

    # 3. Telemetria Neural (BrainState)
    state = BrainState(
        user_id=user_id,
        dopamine_level=8.5,
        hrv=75.0,
        alpha_power=1.8
    )
    focus = FocusScorer.calculate(state)
    print(f"📊 [BRAIN] Foco calculado via Neuro-Telemetry: {focus}")

    # 4. Gerenciamento de Backlog (PriorityMatrix)
    tasks = [
        NeuralTask(title="Refatorar Core API", cognitive_weight=9, metadata={"impact": 10}),
        NeuralTask(title="Fix CSS Glitch", cognitive_weight=2, metadata={"impact": 3}),
        NeuralTask(title="Code Review de Segurança", cognitive_weight=7, metadata={"impact": 8}),
    ]
    
    # Aplicar o foco atual nas tarefas em progresso
    for t in tasks:
        t.focus_score = focus
        
    ordered_tasks = PriorityMatrix.reorder(tasks)
    
    print("\n📋 [BACKLOG] Reordenado soberanamente pelo FocusScorer:")
    for i, t in enumerate(ordered_tasks):
        print(f"  {i+1}. {t.title} | Prioridade: {t.priority} | Peso: {t.cognitive_weight}")

    # 5. Burnout Simulation
    print("\n⚠️ [SAGA] Simulando queda de energia cognitiva...")
    tired_state = BrainState(user_id=user_id, dopamine_level=2.1, hrv=32.0, alpha_power=0.4)
    low_focus = FocusScorer.calculate(tired_state)
    print(f"🛑 [ALERT] Foco caiu para: {low_focus}. Ativando BURNOUT RECOVERY...")
    
    # 6. E2EE Storage
    encrypted_log = BioSecurity.encrypt_brain_data(str(tired_state), bio_digest)
    print(f"🔒 [SECURITY] Logs neurais cifrados via AES-256-GCM. Tamanho: {len(encrypted_log)} bytes.")

    print("\n✨ [SAGA] Ciclo de Vida concluído. Manifestação V3.1 Verificada.")

if __name__ == "__main__":
    asyncio.run(simulate_saga())
