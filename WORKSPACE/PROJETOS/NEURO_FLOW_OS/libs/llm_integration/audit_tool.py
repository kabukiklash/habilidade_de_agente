import json
import sys
from ledger_manager import LedgerManager

def run_audit():
    """
    Antigravity Audit Command: Verifies full system integrity.
    """
    print("="*50)
    print("🛡️ ANTIGRAVITY SYSTEM AUDIT")
    print("="*50)
    
    ledger = LedgerManager()
    report = ledger.verify_integrity()
    
    print(f"[*] Status: {report['status']}")
    print(f"[*] Total Events: {report['total_events']}")
    
    if report["status"] == "OK":
        print("\n✅ INTEGRITY VERIFIED: No unauthorized alterations detected.")
    else:
        print("\n❌ CRITICAL: TAMPERING DETECTED!")
        for violation in report["violations"]:
            print(f"  - Event ID: {violation.get('event_id')}")
            print(f"    Type: {violation.get('type')}")
            print(f"    Index: {violation.get('id')}")
    
    print("="*50)

if __name__ == "__main__":
    run_audit()
