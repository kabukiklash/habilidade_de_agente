import json
import re
import sys
import os

def parse_logs(log_file):
    if not os.path.exists(log_file):
        print(f"Error: Log file {log_file} not found.")
        return

    with open(log_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by the separator
    entries = content.split("-" * 80)
    
    flow = []
    
    for entry in entries:
        if not entry.strip(): continue
        
        # Extract metadata
        meta_match = re.search(r"\[(.*?)\] IP: (.*?)\nSession: (.*?) \| URL: (.*?)\n", entry)
        if not meta_match: continue
        
        timestamp, ip, session, url = meta_match.groups()
        
        # Extract events
        event_lines = re.findall(r"  -> \[(.*?)\] (.*?) \[Trace: (.*?)\] : (.*)\n", entry)
        
        for evt_type, evt_ts, trace_id, details in event_lines:
            try:
                data = json.loads(details)
            except:
                data = details
            
            flow.append({
                "timestamp": timestamp,
                "type": evt_type,
                "traceId": trace_id,
                "url": url,
                "data": data
            })
            
    return flow

def generate_mermaid(flow, filter_trace=None):
    mermaid = ["sequenceDiagram", "    autonumber", "    participant User as 👤 User", "    participant Browser as 🌐 Browser", "    participant API as 🚀 Backend"]
    
    current_trace = None
    
    for evt in flow:
        if filter_trace and evt['traceId'] != filter_trace:
            continue
            
        trace_label = f"[{evt['traceId']}]"
        
        if evt['type'] == 'CLICK':
            mermaid.append(f"    User->>Browser: Click {evt['data'].get('path')} ({evt['data'].get('text')})")
        elif evt['type'] in ['AJAX_SUCCESS', 'FETCH_SUCCESS']:
            mermaid.append(f"    Browser->>API: {evt['data'].get('method', 'GET')} {evt['data'].get('url')}")
            mermaid.append(f"    API-->>Browser: HTTP {evt['data'].get('status')} ({evt['data'].get('duration')})")
        elif evt['type'] == 'BACKEND':
            mermaid.append(f"    Note right of API: Execution: {evt['data']}")
        elif evt['type'] == 'ERROR' or evt['type'].endswith('_ERROR'):
            mermaid.append(f"    Browser-->>User: ❌ Error: {evt['data']}")
            
    return "\n".join(mermaid)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyzer.py <log_file> [trace_id]")
        sys.exit(1)
        
    log_file = sys.argv[1]
    filter_trace = sys.argv[2] if len(sys.argv) > 2 else None
    
    flow = parse_logs(log_file)
    if flow:
        print("\n--- MERMAID FLOW ---\n")
        print(generate_mermaid(flow, filter_trace))
        print("\n--------------------\n")
