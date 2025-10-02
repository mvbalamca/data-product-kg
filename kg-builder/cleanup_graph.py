#!/usr/bin/env python3
"""
Cleanup script to remove existing data before running the pipeline linking setup
"""

from kg_registry import DataProductRegistry

def cleanup_graph():
    """Remove existing data products and pipelines to start fresh"""
    
    kgm = DataProductRegistry("bolt://localhost:7687", "neo4j", "password")
    
    print("🧹 Cleaning up existing data...")
    
    # Remove all relationships and nodes
    kgm.graph.run("""
        MATCH (n)
        DETACH DELETE n
    """)
    
    print("✅ Graph cleaned successfully!")
    print("📝 All nodes and relationships have been removed.")
    print("🚀 Ready to run the pipeline linking setup.")

if __name__ == "__main__":
    cleanup_graph() 