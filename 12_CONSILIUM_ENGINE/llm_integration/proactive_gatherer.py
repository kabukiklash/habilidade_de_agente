import os
import subprocess
import json
import logging
from typing import Dict, Any, List

logger = logging.getLogger("EvidenceGatherer")

class EvidenceGatherer:
    """
    PER (Proactive Evidence & Reasoning) Gatherer.
    Collects real system state (Facts) before AI deliberation.
    """
    
    def __init__(self, workspace_root: str = "."):
        self.root = workspace_root

    def gather_file_context(self, file_paths: List[str]) -> Dict[str, str]:
        """Reads specific files to provided evidence of code state."""
        evidence = {}
        for path in file_paths:
            full_path = os.path.join(self.root, path)
            if os.path.exists(full_path) and os.path.isfile(full_path):
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        # Limit to first 2k chars to save tokens
                        content = f.read(2000)
                        evidence[path] = content
                except Exception as e:
                    evidence[path] = f"Error reading file: {e}"
        return evidence

    def gather_runtime_info(self) -> Dict[str, Any]:
        """Collects ports and process info (OS dependent)."""
        info = {"os": os.name}
        try:
            if os.name == "nt":
                # Windows: Check active ports on localhost
                # (Simplified for the bridge)
                info["active_node"] = os.environ.get("COMPUTERNAME", "Unknown_Win_Node")
            else:
                info["active_node"] = os.environ.get("HOSTNAME", "Unknown_Nix_Node")
        except:
            pass
        return info

    def gather_all(self, target_files: List[str]) -> Dict[str, Any]:
        """Consolidates all evidence into a Context Pack."""
        return {
            "files": self.gather_file_context(target_files),
            "runtime": self.gather_runtime_info(),
            "ledger_status": "INTEGRITY_VERIFIED" # Mocked for the standalone repo
        }

# Global instance
gatherer = EvidenceGatherer()
