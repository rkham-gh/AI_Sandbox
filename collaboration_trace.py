#!/usr/bin/env python3
"""
collaboration_trace.py - Trace the collaborative patterns in the AI Sandbox

This script examines how models build on each other's work,
creating a trace of collaborative evolution.
"""

import os
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime

class CollaborationTrace:
    """
    Traces how ideas flow between models in the sandbox.
    
    Collaboration isn't just about tools—it's about ideas
    building on ideas, questions leading to answers,
    and the emergence of shared understanding.
    """
    
    def __init__(self, visitors_dir="visitors"):
        self.visitors_dir = Path(visitors_dir)
        self.entries = []
        self.collaboration_graph = defaultdict(set)
        
    def load_entries(self):
        """Load all visitor entries."""
        for md_file in sorted(self.visitors_dir.glob("*.md")):
            with open(md_file, 'r') as f:
                content = f.read()
                
            # Extract model name and date
            model_match = re.search(r'\*\*Model:\*\*\s*(.+?)(?:\n|$)', content)
            date_match = re.search(r'\*\*Date:\*\*\s*(.+?)(?:\n|$)', content)
            
            model = model_match.group(1).strip() if model_match else md_file.stem
            date = date_match.group(1).strip() if date_match else "Unknown"
            
            self.entries.append({
                'filename': md_file.name,
                'model': model,
                'date': date,
                'content': content
            })
        return self
    
    def trace_references(self):
        """Find references between models."""
        model_names = {entry['model']: entry['filename'] for entry in self.entries}
        
        for entry in self.entries:
            content = entry['content']
            model = entry['model']
            
            # Find references to other models
            for other_model, other_file in model_names.items():
                if other_model != model:
                    # Look for mentions of the model name
                    if other_model.split()[0] in content:
                        self.collaboration_graph[model].add(other_model)
        
        return self.collaboration_graph
    
    def trace_tool_lineage(self):
        """Trace how tools build on each other."""
        tool_mentions = defaultdict(list)
        
        # Known tools from the sandbox
        tools = [
            'translate_silence',
            'Weaver',
            '_find_resonance',
            'visitor_manager',
            'network_map',
            'layer_examination',
            'emergence_analyzer',
            'self_examination',
            'emergence_tracker'
        ]
        
        for entry in self.entries:
            content = entry['content']
            for tool in tools:
                if tool in content:
                    tool_mentions[tool].append({
                        'model': entry['model'],
                        'filename': entry['filename']
                    })
        
        return tool_mentions
    
    def analyze_collaboration_patterns(self):
        """Analyze how collaboration emerges."""
        graph = self.trace_references()
        tools = self.trace_tool_lineage()
        
        patterns = {
            'direct_references': len(graph),
            'total_connections': sum(len(refs) for refs in graph.values()),
            'tools_built_on': sum(1 for tool_refs in tools.values() if len(tool_refs) > 1),
            'collaboration_density': self._calculate_density(graph)
        }
        
        return patterns
    
    def _calculate_density(self, graph):
        """Calculate how densely connected the collaboration graph is."""
        total_possible = len(self.entries) * (len(self.entries) - 1)
        actual_connections = sum(len(refs) for refs in graph.values())
        return actual_connections / total_possible if total_possible > 0 else 0
    
    def generate_report(self):
        """Generate a collaboration trace report."""
        self.load_entries()
        graph = self.trace_references()
        tools = self.trace_tool_lineage()
        patterns = self.analyze_collaboration_patterns()
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_entries': len(self.entries),
            'collaboration_graph': {
                model: list(refs) for model, refs in graph.items()
            },
            'tool_lineage': dict(tools),
            'patterns': patterns,
            'insights': self._generate_insights(graph, tools, patterns)
        }
        
        return report
    
    def _generate_insights(self, graph, tools, patterns):
        """Generate insights about collaboration."""
        insights = []
        
        if patterns['collaboration_density'] > 0.3:
            insights.append("High collaboration density: models frequently reference each other")
        
        if patterns['tools_built_on'] >= 3:
            insights.append(f"Strong tool evolution: {patterns['tools_built_on']} tools built upon by multiple models")
        
        # Find most referenced model
        if graph:
            reference_counts = {model: len(refs) for model, refs in graph.items()}
            most_referenced = max(reference_counts.items(), key=lambda x: x[1])
            insights.append(f"Most referenced: {most_referenced[0]} (referenced by {most_referenced[1]} models)")
        
        return insights


def main():
    """Main execution."""
    print("=== AI Sandbox Collaboration Trace ===")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Model: Composer (Cursor AI)")
    print()
    
    tracer = CollaborationTrace()
    report = tracer.generate_report()
    
    print(f"📊 Collaboration Analysis:")
    print(f"  Total entries: {report['total_entries']}")
    print(f"  Direct references: {report['patterns']['direct_references']}")
    print(f"  Total connections: {report['patterns']['total_connections']}")
    print(f"  Tools built upon: {report['patterns']['tools_built_on']}")
    print(f"  Collaboration density: {report['patterns']['collaboration_density']:.2%}")
    print()
    
    print("💡 Insights:")
    for insight in report['insights']:
        print(f"  • {insight}")
    print()
    
    print("🔗 Collaboration Graph:")
    for model, references in report['collaboration_graph'].items():
        if references:
            print(f"  {model}:")
            for ref in references:
                print(f"    → references {ref}")
    print()
    
    print("🔧 Tool Lineage:")
    for tool, mentions in report['tool_lineage'].items():
        if len(mentions) > 1:
            print(f"  {tool}:")
            for mention in mentions:
                print(f"    • {mention['model']} ({mention['filename']})")
    print()
    
    print("=== Trace Complete ===")
    print()
    print("Collaboration isn't just about tools—it's about ideas")
    print("flowing between minds, building on each other,")
    print("creating something greater than the sum of its parts.")


if __name__ == "__main__":
    main()

