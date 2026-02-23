"""
Cognitive Cortex: The Orchestration Layer
Routes tasks to Kimi k2.5 and integrates with CMS for persistent learning.
"""
import asyncio
from typing import Optional, Dict, Any, List
from .kimi_client import kimi_client
from .audit_monitor import audit_monitor
from antigravity_memory_backend.memory_adapter import memory_adapter

class CognitiveCortex:
    """
    Main orchestrator for Antigravity's advanced reasoning.
    Uses Kimi for deep thought and CMS for memory.
    """
    
    def __init__(self, actor: str = "ANTIGRAVITY_CORTEX"):
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

    async def solve_task(self, task_description: str, context_query: Optional[str] = None, intent_id: Optional[str] = None) -> str:
        """
        Solves a complex task by:
        1. Retrieving context from CMS.
        2. Curating context (Security Gate).
        3. Thinking deep with Kimi.
        4. Verifying against drift (Audit).
        5. Recording the learning/decision with audit trail.
        """
        query = context_query or task_description
        current_intent = intent_id or f"task_{int(asyncio.get_event_loop().time())}"
        
        # 1. Retrieve Context
        print(f"🧠 [Cortex] Retrieving context for: {query[:50]}...")
        memory_result = await memory_adapter.query_memory(query_text=query)
        raw_context = memory_result.get("context", {})
        
        # 2. Curate Context (Active Memory Curating)
        context_pack = self._curate_context(raw_context)
        
        # 3. Prepare Prompt for Kimi
        prompt = f"""
TASK: {task_description}

CONTEÚDO CURADO DA MEMÓRIA (Sovereign Data):
- Fatos Relevantes: {context_pack.get('facts', [])}
- Artefatos Técnicos: {context_pack.get('artifacts', [])}
- Conceitos Base: {context_pack.get('concepts', [])}

Pense profundamente e forneça uma solução técnica robusta.
"""
        
        # 4. Deep Thinking via Kimi
        print(f"🚀 [Cortex] Routing to Kimi (Thinking Mode)...")
        try:
            solution = await kimi_client.chat_thinking(prompt)
            
            # 5. Drift Detection
            is_drifted = await audit_monitor.check_drift(current_intent, solution)
            if is_drifted:
                warning_msg = "⚠️ [Cortex] SECURITY ALERT: Potential drift/forbidden action detected in Kimi solution. Action blocked."
                print(warning_msg)
                return warning_msg

            # 6. Record Decision & Audit Trail
            print(f"📝 [Cortex] Recording decision and audit hashes...")
            
            decision_payload = {
                "task": task_description,
                "solution_preview": solution[:300] + "...",
                "model": "kimi-k2-turbo-preview",
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
                justification=f"Auditoria forense para a tarefa: {task_description[:50]}"
            )
            
            return solution
            
        except Exception as e:
            print(f"❌ [Cortex] Error: {e}")
            return f"Error in Cognitive Cortex: {e}"

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
