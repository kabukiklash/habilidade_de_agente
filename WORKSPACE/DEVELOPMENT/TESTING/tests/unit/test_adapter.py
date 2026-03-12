import sys
import os

print("--- sys.path ---")
for p in sys.path: print(p)

try:
    from llm_integration.cms_client import CMSClient
    print("CMSClient imported directly: SUCCESS")
except ImportError as e:
    print("CMSClient imported directly: FAILED", e)

from antigravity_memory_backend.memory_adapter import memory_adapter, CMS_AVAILABLE, SQLITE_AVAILABLE
print(f"memory_adapter CMS_AVAILABLE = {CMS_AVAILABLE}")
print(f"memory_adapter SQLITE_AVAILABLE = {SQLITE_AVAILABLE}")
print(f"memory_adapter status = {memory_adapter.get_status()}")

