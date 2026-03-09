import asyncio
import json
import logging
from typing import List, Dict, Any, Optional
from .kimi_client import kimi_client
from .inception_client import inception_client
from .openai_client import openai_client
from .proactive_gatherer import gatherer

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
        print(f"🕵️ [Consilium] Initiating PER Fact-Gathering...")
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

        print(f"🗳️ [Consilium] Calling the Council (Kimi + Inception + OpenAI)...")
        
        # Parallel Execution
        tasks = [
            safe_call(kimi_client.chat_thinking(prompt, system_msg="You are the Lead Architect (deep reasoning)."), "Kimi"),
            safe_call(inception_client.chat_thinking(prompt, system_msg="You are the High-Performance Executor."), "Inception"),
            safe_call(openai_client.chat_thinking(prompt, system_msg="You are the Security & Logic Auditor."), "OpenAI")
        ]
        
        results = await asyncio.gather(*tasks)
        solutions = {
            "kimi": results[0],
            "inception": results[1],
            "openai": results[2]
        }
        
        # TODO: Add Claude as the final Auditor/Tie-breaker
        # For now, we use a synthesized verdict
        print(f"⚖️ [Consilium] Synthesizing consensus...")
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
        
        KIMI: {solutions.get('kimi', '')[:500]}
        INCEPTION: {solutions.get('inception', '')[:500]}
        
        EVIDENCE: {json.dumps(evidence['runtime'])}
        """
        
        # Defaulting synthesis to Kimi for now as Lead Architect
        return solutions.get("kimi", "Consensus not reached.")

# Global instance
consilium = ConsiliumEngine()
