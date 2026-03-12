"""
Cognitive Cortex: The Orchestration Layer
Routes tasks to Kimi k2.5 and integrates with CMS for persistent learning.
"""
import asyncio
import sys
import os
from typing import Optional, Dict, Any, List

# Sovereign Path Orchestration
base_dir = "c:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente"
tech_paths = [
    os.path.join(base_dir, "03_CIRCUIT_BREAKER_V3"),
    os.path.join(base_dir, "04_KNOWLEDGE_GRAPH"),
    os.path.join(base_dir, "05_VIBECODE_G7"),
    os.path.join(base_dir, "06_AUDIT_MONITOR_LEDGER"),
    os.path.join(base_dir, "07_KIMI_MEMORY_BRIDGE", "adapter"),
    os.path.join(base_dir, "07_KIMI_MEMORY_BRIDGE", "bridges"),
    os.path.join(base_dir, "02_COGNITIVE_CORTEX", "core")
]

for p in tech_paths:
    if p not in sys.path:
        sys.path.insert(0, p)

# Secure Imports from Sovereign Technologies
from kimi_client import kimi_client
from inception_client import inception_client
from openai_client import openai_client
from claude_client import claude_client
from audit_monitor_master import audit_monitor
from memory_adapter_master import memory_adapter

class CognitiveCortex:
    """
    Main orchestrator for Evolution's advanced reasoning.
    Uses Kimi for deep thought and CMS for memory.
    """
    
    def __init__(self, actor: str = "EVOLUTION_CORTEX"):
        self.actor = actor
        self.kimi_actor = "KIMI_LEARNING_VAULT"
        # Termos sensíveis que nunca devem ser enviados ao Kimi
        self.sensitive_patterns = ["key", "token", "password", "secret", "auth", "credential", "private_key"]

    def _curate_context(self, context_pack: Dict[str, Any]) -> Dict[str, Any]:
        """
        Filtra o context_pack para remover informações sensíveis antes de enviar ao Kimi.
        Implementação do 'Active Memory Curating'.
        """
        curated = {
            "facts": [],
            "artifacts": [],
            "concepts": []
        }
        
        for category in ["facts", "artifacts", "concepts"]:
            items = context_pack.get(category, [])
            for item in items:
                item_str = str(item).lower()
                # Se não contiver padrões sensíveis, adiciona ao contexto curado
                if not any(pattern in item_str for pattern in self.sensitive_patterns):
                    curated[category].append(item)
                    
        return curated

    async def solve_task(self, task_description: str, context_query: Optional[str] = None, intent_id: Optional[str] = None, provider: str = "kimi") -> str:
        """
        Solves a complex task by:
        1. Retrieving context from CMS.
        2. Curating context (Security Gate).
        3. Thinking deep with selected provider (Kimi or Inception).
        4. Verifying against drift (Audit).
        5. Recording the learning/decision with audit trail.
        """
        # Select client
        if provider == "inception":
            client = inception_client
            model_name = "mercury-2"
        elif provider == "openai":
            client = openai_client
            model_name = "o3-mini"
        elif provider == "claude":
            client = claude_client
            model_name = "claude-3-5-sonnet"
        else:
            client = kimi_client
            model_name = "kimi-k2-turbo-preview"

        query = context_query or task_description
        current_intent = intent_id or f"task_{int(asyncio.get_event_loop().time())}"
        
        # ==========================================
        # 🛡️ CIRCUIT BREAKER: Proteção Anti-Vazamento (V3 - Escudo Atômico)
        # ==========================================
        from circuit_breaker_master import circuit_breaker
        
        if not await circuit_breaker.verify_safety():
            msg = "⛔ [Circuit Breaker] BLOQUEIO ATIVADO: Infraestrutura instável ou erro de segurança detectado. Chamada ao LLM abortada."
            print(msg)
            return msg

        try:
            print(f"🧠 [Cortex] Retrieving context for: {query[:50]}...")
            memory_result = await memory_adapter.query_memory(query_text=query)
            
            if isinstance(memory_result, dict) and memory_result.get("status_code") in [429, 401, 403, 500]:
                raise ConnectionError(f"Erro HTTP {memory_result.get('status_code')} nas credenciais do adapter")
                
            raw_context = memory_result.get("context", {}) if isinstance(memory_result, dict) else {}
            
        except Exception as e:
            circuit_breaker_msg = f"❌ [Cortex] Falha na recuperação de contexto: {str(e)}."
            print(circuit_breaker_msg)
            return circuit_breaker_msg
        # ==========================================

        # 2. Curate & Compress Context (Context Shield)
        from context_transformer import context_transformer
        from roi_engine import roi_engine
        
        # Filtragem inicial de segurança
        curated_context = self._curate_context(raw_context)
        # Compressão semântica
        compressed_context = context_transformer.compress(curated_context, level="MEDIUM")
        
        # 3. Prepare Prompt for Kimi
        prompt = f"""
TASK: {task_description}

CONTEÚDO COMPRIMIDO DA MEMÓRIA (Sovereign Data):
- Fatos: {compressed_context.get('facts', [])}
- Artefatos: {compressed_context.get('artifacts', [])}
- Conceitos: {compressed_context.get('concepts', [])}

Pense profundamente e forneça uma solução técnica robusta.
"""
        # 4. Deep Thinking via selected client
        print(f"🚀 [Cortex] Routing to {provider.upper()} (Thinking Mode)...")
        try:
            result = await client.chat_thinking(prompt, return_usage=True)
            
            if isinstance(result, tuple):
                solution, usage = result
            else:
                solution, usage = result, {}
            
            # Token Economy & ROI Math
            import json
            raw_tokens_estimate = len(json.dumps(raw_context)) // 4
            compressed_tokens_estimate = len(json.dumps(compressed_context)) // 4
            
            roi_data = roi_engine.calculate_savings(model_name, raw_tokens_estimate, compressed_tokens_estimate)
            tokens_used = usage.get('total_tokens', 0)
            
            print(f"💰 [ROI Engine] Saved: {roi_data['tokens_saved']} tokens (${roi_data['usd_saved']}) | Efficiency: {roi_data['efficiency_gain']}%")
            
            # 5. Drift Detection
            is_drifted = await audit_monitor.check_drift(current_intent, solution)
            if is_drifted:
                warning_msg = "⚠️ [Cortex] SECURITY ALERT: Potential drift/forbidden action detected in Kimi solution. Action blocked."
                print(warning_msg)
                return warning_msg

            # [SPRINT C] FORMAL VERIFICATION: Verificação de Axiomas
            from formal_verifier_master import FormalVerifier
            verifier = FormalVerifier()
            formal_check = verifier.verify_vibe_axioms(solution)
            if formal_check["status"] == "REJECTED":
                print(f"⚠️ [FormalVerifier] AXIOMA VIOLADO: {formal_check['violations']}")
                # Podemos optar por bloquear ou apenas rotular. Para G7, rotulamos com aviso crítico.
                solution = f"/* [⚠️ SECURITY VIOLATION DETECTED: {formal_check['violations']}] */\n" + solution

            # 6. Record Decision & Audit Trail
            print(f"📝 [Cortex] Recording decision and audit hashes...")
            
            # [SPRINT B] GRAPH LEARNING: Extração de Conhecimento em Background
            from graph_builder_master import graph_builder
            asyncio.create_task(graph_builder.process_solution(solution, current_intent))
            
            decision_payload = {
                "task": task_description,
                "solution_preview": solution[:300] + "...",
                "model": model_name,
                "curated_context_used": True,
                "intent_id": current_intent
            }

            # Log to Kimi Workspace
            await memory_adapter.append_event(
                event_type="KIMI_DECISION",
                payload=decision_payload,
                justification=f"Decisão registrada no workspace isolado do Kimi.",
                correlation_id=current_intent
            )

            # Log to Audit Monitor (Integrity Hash)
            await audit_monitor.log_decision_with_intent(
                intent_id=current_intent,
                decision_payload=decision_payload,
                justification=f"Auditoria forense para a tarefa: {task_description[:50]}",
                tokens_used=tokens_used,
                tokens_saved=roi_data['tokens_saved'],
                usd_saved=roi_data['usd_saved']
            )
            
            return solution
        except Exception as e:
            print(f"❌ [Cortex] LLM Route Error: {e}")
            return f"Error in Cognitive Cortex LLM Route: {e}"

    async def swarm_analyze(self, objective: str, components: List[str]) -> Dict[str, str]:
        """
        Simulates an Agent Swarm by performing parallel analysis of components.
        """
        print(f"🐝 [Cortex] Initiating Swarm Analysis for: {objective}...")
        
        tasks = []
        for component in components:
            task_prompt = f"Analyze the following component in the context of '{objective}': {component}"
            tasks.append(kimi_client.chat_instant(task_prompt))
            
        results = await asyncio.gather(*tasks)
        
        swarm_report = dict(zip(components, results))
        
        # Record swarm completion
        await memory_adapter.append_event(
            event_type="SWARM_COMPLETE",
            payload={
                "objective": objective,
                "components": components,
                "report_summary": "Parallel analysis completed."
            },
            justification="Swarm analysis executed for component mapping."
        )
        
        return swarm_report

# Global instance
cognitive_cortex = CognitiveCortex()
