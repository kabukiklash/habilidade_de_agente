
import asyncio
import asyncpg
import json
import os
from datetime import datetime

async def verify_cms_data():
    print("🛠️ Starting Manual Verification of CMS Data...")
    
    try:
        # Connect to the database using the internal port mapped to the host
        conn = await asyncpg.connect(
            user='cms_admin',
            password='cms_secret_2026',
            database='cognitive_memory',
            host='127.0.0.1',
            port=5433
        )
        print("✅ Connection to CMS Database established.")
        
        # Count rows in main tables
        tables = ['events', 'artifacts', 'concepts', 'edges']
        counts = {}
        for table in tables:
            count = await conn.fetchval(f"SELECT count(*) FROM {table}")
            counts[table] = count
            print(f"  - {table}: {count} rows")
            
        # Get latest event timestamp
        max_ts = await conn.fetchval("SELECT max(created_at) FROM events")
        print(f"  - Latest Event: {max_ts}")
        
        await conn.close()
        
        # Generate a "Simulated Manifest" for the validation report
        manifest = {
            "timestamp": datetime.now().isoformat(),
            "database": "cognitive_memory",
            "validation_status": "SUCCESS",
            "row_counts": counts,
            "latest_event_ts": str(max_ts)
        }
        
        with open('cms_validation_data.json', 'w') as f:
            json.dump(manifest, f, indent=2)
        
        print(f"📄 Validation data saved to cms_validation_data.json")
        return True
        
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(verify_cms_data())
