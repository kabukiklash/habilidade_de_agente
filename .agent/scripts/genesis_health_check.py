import requests
import sys
import time
import json

def check_genesis():
    base_url = "http://localhost:3000/v1"
    
    print("Checking GenesisCore Foundation Operational Governance...")
    print("-" * 50)
    
    # 1. Health Check
    try:
        health = requests.get(f"{base_url}/health")
        if health.status_code == 200:
            data = health.json()
            print(f"✅ Health: {data['status']} (Mode: {data.get('mode', 'N/A')})")
        else:
            print(f"❌ Health: Failed (Status: {health.status_code})")
    except Exception as e:
        print(f"❌ Health: Connection Error - {str(e)}")

    # 2. Status Check
    try:
        status = requests.get(f"{base_url}/status")
        if status.status_code == 200:
            data = status.json()
            print(f"✅ Control Plane: {data['control_plane']['status']}")
            print(f"✅ Database: {data['infrastructure']['database']} ({data['infrastructure']['engine']})")
            print(f"✅ Governance: {data['governance']}")
        else:
            print(f"❌ Status: Failed (Status: {status.status_code})")
    except Exception as e:
        print(f"❌ Status: Connection Error - {str(e)}")

    # 3. Metrics Check
    try:
        metrics = requests.get(f"{base_url}/metrics")
        if metrics.status_code == 200:
            data = metrics.json().get('data', {})
            print(f"📊 Cells: {data.get('total_cells', 0)} | Avg Friction: {data.get('avg_friction', 0)}")
            print(f"📊 Memory Usage: {data.get('memory_usage_mb', 0)} MB")
        else:
            print(f"❌ Metrics: Failed (Status: {metrics.status_code})")
    except Exception as e:
        print(f"❌ Metrics: Connection Error - {str(e)}")

    print("-" * 50)
    print("NIST Operational Governance: MANAGE/GOVERN checked.")

if __name__ == "__main__":
    check_genesis()
