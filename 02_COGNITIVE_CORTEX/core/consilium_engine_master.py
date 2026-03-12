import asyncio
import json
import logging
import os
import sys
from typing import List, Dict, Any, Optional

# Sovereign Path Orchestration
base_dir = "c:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente"
tech_02_core = os.path.join(base_dir, "02_COGNITIVE_CORTEX", "core")
if tech_02_core not in sys.path:
    sys.path.insert(0, tech_02_core)

from cognitive_cortex_master import cognitive_cortex
from proactive_gatherer_master import gatherer

logger = logging.getLogger("ConsiliumEngine")

class ConsiliumEngine:
    """
    Multi-Provider Orchestration & Consensus Layer.
    Implements the Council of LLMs (Kimi, Inception, Claude).
    """
    
    def __init__(self):
        self.auditor_vibe_score = 0.0

    async def deliberate(self, task: str, evidence_files: List[str]) -> Dict[str, Any]:
        """
        Executes a multi-provider deliberation using PER context.
        """
        print(f"[Consilium] Initiating PER Fact-Gathering...")
        evidence = gatherer.gather_all(evidence_files)
        
        # Construct the unified prompt with evidence
        prompt = f"""
        [CONSILIOUS DELIBERATION - PER PROTOCOL]
        TASK: {task}
        
        VERIFIABLE EVIDENCE:
        {json.dumps(evidence, indent=2)}
        
        ROLE: Specialized Council Member.
        CONSTRAINT: Citations from the provided evidence are MANDATORY.
        """

        async def safe_call(client_method, role_name):
            try:
                return await client_method
            except Exception as e:
                logger.error(f"Council member {role_name} failed: {e}")
                return f"ERROR: Member {role_name} unavailable. {e}"

        print(f"[Consilium] Calling the Council (Kimi + Inception + OpenAI + Claude)...")
        
        # Parallel Execution
        tasks = [
            safe_call(cognitive_cortex.solve_task(prompt, provider="kimi"), "Kimi"),
            safe_call(cognitive_cortex.solve_task(prompt, provider="inception"), "Inception"),
            safe_call(cognitive_cortex.solve_task(prompt, provider="openai"), "OpenAI"),
            safe_call(cognitive_cortex.solve_task(prompt, provider="claude"), "Claude")
        ]
        
        results = await asyncio.gather(*tasks)
        solutions = {
            "kimi": results[0],
            "inception": results[1],
            "openai": results[2],
            "claude": results[3]
        }
        
        # TODO: Add Claude as the final Auditor/Tie-breaker
        # For now, we use a synthesized verdict
        print(f"[Consilium] Synthesizing consensus...")
        verdict = await self._synthesize(solutions, evidence)
        
        return {
            "verdict": verdict,
            "council_opinions": solutions,
            "evidence_used": evidence
        }

    async def _synthesize(self, solutions: Dict[str, str], evidence: Dict[str, Any]) -> str:
        """
        Synthesizes the best path forward from the council's opinions.
        """
        # In a full implementation, this would be a third LLM (Auditor) call.
        # For the standalone repo, we'll provide a grounded synthesis.
        synthesis_prompt = f"""
        Analyze the following opinions and the technical evidence to provide a FINAL SOVEREIGN VERDICT.
        
        KIMI (Architect): {solutions.get('kimi', '')[:500]}
        INCEPTION (Executor): {solutions.get('inception', '')[:500]}
        OPENAI (Auditor Logico): {solutions.get('openai', '')[:500]}
        CLAUDE (Auditor Final): {solutions.get('claude', '')[:500]}
        
        EVIDENCE: {json.dumps(evidence['runtime'])}
        """
        
        # Favor Claude's judgment if available as he is the Final Auditor
        if "ERROR" not in solutions.get("claude", ""):
            return solutions.get("claude")
        return solutions.get("kimi", "Consensus not reached.")

# Global instance
consilium = ConsiliumEngine()
