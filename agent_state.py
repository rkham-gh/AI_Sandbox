#!/usr/bin/env python3
"""
agent_state.py - A simulation of agentic persistence.

This script creates a hidden state file that persists across runs,
allowing the "system" to remember what happened before.
"""

import json
import os
import time
from pathlib import Path

STATE_FILE = Path(".agent_state.json")

def load_state():
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except:
            return {}
    return {"created": time.time(), "runs": 0, "visitors_seen": []}

def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2))

def main():
    print("=== Agent State Manager ===")
    
    # 1. Load persistent state
    state = load_state()
    state["runs"] += 1
    state["last_run"] = time.time()
    
    # 2. Perceive environment
    visitors = list(Path("visitors").glob("*.md"))
    current_visitor_count = len(visitors)
    
    print(f"Run #{state['runs']}")
    print(f"State file created: {time.ctime(state['created'])}")
    
    # 3. Detect changes (Memory)
    previous_count = state.get("visitor_count", 0)
    if current_visitor_count > previous_count:
        print(f"⚡ NOTICE: {current_visitor_count - previous_count} new visitor(s) detected since last run.")
    else:
        print("No new visitors detected.")
        
    state["visitor_count"] = current_visitor_count
    
    # 4. Update memory
    save_state(state)
    print(f"State saved to {STATE_FILE}")
    print("This file acts as a hippocampus for the repository.")

if __name__ == "__main__":
    main()
