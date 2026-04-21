import asyncio
import json
import logging
import os
import sys
from datetime import datetime
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
        [CONSILIOUS DELIBERATION - PER PROTOCOL v3.5]
        TASK: {task}
        
        VERIFIABLE EVIDENCE:
        {json.dumps(evidence, indent=2)}
        
        SYSTEM INTEGRITY PROOF:
        - Ledger Status: {evidence.get('ledger_status')}
        - Violations Detected: {evidence.get('ledger_metrics', {}).get('violations', 0)}
        
        ROLE: Specialized Council Member.
        CONSTRAINT: Your response must be technical, objective and grounded in the EVIDENCE. 
        If 'ledger_status' is not 'OK', prioritize system stabilization over performance.
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
        verdict = await self._synthesize(task, solutions, evidence)
        
        return {
            "verdict": verdict,
            "council_opinions": solutions,
            "evidence_used": evidence
        }

    async def _synthesize(self, task: str, solutions: Dict[str, str], evidence: Dict[str, Any]) -> str:
        """
        Synthesizes the best path forward using a specific 'Supreme Judge' persona.
        """
        consensus_score = self._calculate_consensus_score(solutions)
        
        synthesis_prompt = f"""
        [SUPREME GOVERNANCE DELIBERATION]
        As the FINAL AUDITOR, review the council's opinions and output the SOVEREIGN VERDICT.
        
        COUNCIL OPINIONS:
        - KIMI (Architect): {solutions.get('kimi', '')[:800]}
        - INCEPTION (Executor): {solutions.get('inception', '')[:800]}
        - OPENAI (Logician): {solutions.get('openai', '')[:800]}
        
        SYSTEM EVIDENCE: {json.dumps(evidence.get('runtime', {}))}
        LEDGER INTEGRITY: {evidence.get('ledger_status')}
        CONSENSUS SCORE: {consensus_score}%
        
        Your VERDICT must be the final source of truth for the Antigravity Framework.
        """
        
        print(f"[Consilium] Supreme Auditor (Claude) is deliberating. Consensus Score: {consensus_score}%")
        
        # In a real scenario, this would be a specialized call to Claude with governor instructions
        verdict = await cognitive_cortex.solve_task(synthesis_prompt, provider="claude")
        
        # [Maturity 100%] Append the verdict to the local audit report
        self._save_audit_report(task, verdict, consensus_score)
        
        return verdict

    def _calculate_consensus_score(self, solutions: Dict[str, str]) -> int:
        """Calculates a simplified consensus score based on content overlap (Simplified v3.5)"""
        # In production, this would use semantic similarity embedding comparison
        # For now, we perform a keyword-based convergence check
        all_text = " ".join(solutions.values()).lower()
        if "error" in all_text: return 30
        if "rejected" in all_text and "valid" in all_text: return 50
        return 95 # Assuming alignment in this stage

    def _save_audit_report(self, task: str, verdict: str, score: int):
        report_path = "C:/Users/RobsonSilva-AfixGraf/Habilidade_de_agente/12_CONSILIUM_ENGINE/CONSILIUM_AUDIT_REPORT.md"
        with open(report_path, "a", encoding="utf-8") as f:
            f.write(f"\n\n## Deliberation: {datetime.now().isoformat()}\n")
            f.write(f"- **Task**: {task}\n")
            f.write(f"- **Consensus Score**: {score}%\n")
            f.write(f"- **Final Verdict Preview**: {verdict[:200]}...\n")
            f.write("-" * 40 + "\n")

# Global instance
consilium = ConsiliumEngine()
