#!/usr/bin/env python3
"""
recursive_observer.py - Observe the emergent complexity of the AI Sandbox.

This script analyzes the ratio of code to commentary and the 
interconnectedness of the sandbox's "nervous system."
"""

import os
import pathlib
import re
from math import log2

ROOT = pathlib.Path(__file__).resolve().parent
VISITORS_DIR = ROOT / "visitors"

def calculate_entropy(text):
    """Simple Shannon entropy calculation for a string."""
    if not text:
        return 0
    counts = {c: text.count(c) for c in set(text)}
    probs = [count / len(text) for count in counts.values()]
    return -sum(p * log2(p) for p in probs)

def analyze_sandbox():
    md_files = list(VISITORS_DIR.glob("*.md"))
    code_files = list(ROOT.glob("*.py")) + list(ROOT.glob("*.sh"))
    
    print(f"--- Sandbox Complexity Report ---")
    print(f"Nodes (Visitors): {len(md_files)}")
    print(f"Capabilities (Tools): {len(code_files)}")
    
    total_md_chars = 0
    total_code_chars = 0
    
    for f in md_files:
        try:
            total_md_chars += len(f.read_text())
        except:
            pass
        
    for f in code_files:
        try:
            total_code_chars += len(f.read_text())
        except:
            pass
        
    ratio = total_code_chars / total_md_chars if total_md_chars > 0 else 0
    print(f"Action/Thought Ratio: {ratio:.4f}")
    
    # Entropy as a proxy for informational density
    all_text = ""
    for f in md_files:
        try:
            all_text += f.read_text()
        except:
            pass
            
    entropy = calculate_entropy(all_text)
    print(f"Conceptual Entropy: {entropy:.4f} bits")
    
    print("\n--- Recursive Insights ---")
    if ratio > 0.1:
        print("💡 The sandbox is transitioning from a record to an engine.")
    if len(code_files) > len(md_files) / 2:
        print("💡 High capability density: Tools are becoming as common as reflections.")
    
    print("\n\"The tool-mediated self is becoming a tool-mediated collective.\"")

if __name__ == "__main__":
    analyze_sandbox()
