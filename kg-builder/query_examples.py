#!/usr/bin/env python3
"""
Example script demonstrating how to execute Cypher queries on the Knowledge Graph
"""

from kg_registry import DataProductRegistry
import json

def execute_queries():
    """Execute various Cypher queries and display results"""
    
    # Initialize connection
    kgm = DataProductRegistry("bolt://localhost:7687", "<<user-name>>", "<<password>>")
    
    print("🔍 Knowledge Graph Query Examples")
    print("=" * 50)
    
    # Query 1: Basic Data Product Overview
    print("\n1️⃣ Basic Data Product Overview:")
    print("-" * 30)
    result = kgm.graph.run("""
        MATCH (dp:DataProduct)
        RETURN dp.name AS Name, 
               dp.type AS Type, 
               dp.domain AS Domain, 
               dp.subdomain AS Subdomain,
               dp.destination AS Destination,
               dp.schedule AS Schedule
        ORDER BY dp.domain, dp.name
    """).data()
    
    for row in result:
        print(f"📦 {row['Name']} ({row['Type']}) - {row['Domain']}/{row['Subdomain']}")
        print(f"   Destination: {row['Destination']} | Schedule: {row['Schedule']}")
    
    # Query 2: Pipeline Flow
    print("\n2️⃣ Pipeline Flow:")
    print("-" * 30)
    result = kgm.graph.run("""
        MATCH (p1:Pipeline)-[r:TRIGGERS]->(p2:Pipeline)
        RETURN p1.name AS FromPipeline, p2.name AS ToPipeline
        ORDER BY p1.name, p2.name
    """).data()
    
    for row in result:
        print(f"🔁 {row['FromPipeline']} → {row['ToPipeline']}")
    
    # Query 3: Data Product Dependencies
    print("\n3️⃣ Data Product Dependencies:")
    print("-" * 30)
    result = kgm.graph.run("""
        MATCH (dp1:DataProduct)-[r:FEEDS_INTO]->(dp2:DataProduct)
        RETURN dp1.name AS Source, dp2.name AS Target, dp1.domain AS SourceDomain
        ORDER BY dp1.domain, dp1.name
    """).data()
    
    for row in result:
        print(f"📊 {row['Source']} → {row['Target']} ({row['SourceDomain']})")
    
    # Query 4: Domain Analysis
    print("\n4️⃣ Data Products by Domain:")
    print("-" * 30)
    result = kgm.graph.run("""
        MATCH (dp:DataProduct)
        RETURN dp.domain AS Domain, count(dp) AS Count, collect(dp.name) AS Products
        ORDER BY Count DESC
    """).data()
    
    for row in result:
        print(f"🏷️ {row['Domain']}: {row['Count']} products")
        print(f"   Products: {', '.join(row['Products'])}")
    
    # Query 5: Pipeline to Data Product Mapping
    print("\n5️⃣ Pipeline to Data Product Mapping:")
    print("-" * 30)
    result = kgm.graph.run("""
        MATCH (p:Pipeline)-[r:PRODUCES]->(dp:DataProduct)
        RETURN p.name AS Pipeline, dp.name AS DataProduct, dp.type AS Type
        ORDER BY p.name
    """).data()
    
    for row in result:
        print(f"⚙️ {row['Pipeline']} → {row['DataProduct']} ({row['Type']})")
    
    # Query 6: Complete Lineage Path
    print("\n6️⃣ Complete Data Lineage Paths:")
    print("-" * 30)
    result = kgm.graph.run("""
        MATCH path = (start:DataProduct)-[:FEEDS_INTO*]->(end:DataProduct)
        WHERE start.name CONTAINS 'Raw' AND end.name CONTAINS 'Summary'
        RETURN [node in nodes(path) | node.name] AS LineagePath,
               length(path) AS PathLength
        ORDER BY PathLength DESC
    """).data()
    
    for row in result:
        print(f"🔄 Lineage ({row['PathLength']} steps): {' → '.join(row['LineagePath'])}")
    
    # Query 7: Impact Analysis
    print("\n7️⃣ Data Product Impact Analysis:")
    print("-" * 30)
    result = kgm.graph.run("""
        MATCH (dp:DataProduct)
        OPTIONAL MATCH (dp)-[:FEEDS_INTO]->(downstream:DataProduct)
        OPTIONAL MATCH (upstream:DataProduct)-[:FEEDS_INTO]->(dp)
        RETURN dp.name AS DataProduct,
               count(DISTINCT downstream) AS Downstream,
               count(DISTINCT upstream) AS Upstream,
               count(DISTINCT downstream) + count(DISTINCT upstream) AS TotalConnections
        ORDER BY TotalConnections DESC
    """).data()
    
    for row in result:
        print(f"📈 {row['DataProduct']}: {row['Downstream']} downstream, {row['Upstream']} upstream ({row['TotalConnections']} total)")
    
    # Query 8: Pipeline Execution Order
    print("\n8️⃣ Pipeline Execution Order:")
    print("-" * 30)
    result = kgm.graph.run("""
        MATCH (p:Pipeline)
        OPTIONAL MATCH (p)-[:TRIGGERS]->(dependent:Pipeline)
        WITH p, count(dependent) AS dependencies
        RETURN p.name AS Pipeline, dependencies AS Dependencies
        ORDER BY dependencies ASC
    """).data()
    
    for row in result:
        status = "Can run first" if row['Dependencies'] == 0 else f"Depends on {row['Dependencies']} pipeline(s)"
        print(f"⚙️ {row['Pipeline']}: {status}")
    
    # Query 9: Lifecycle Analysis
    print("\n9️⃣ Data Product Lifecycle Analysis:")
    print("-" * 30)
    result = kgm.graph.run("""
        MATCH (dp:DataProduct)
        RETURN 
          CASE 
            WHEN dp.name CONTAINS 'Raw' THEN 'Raw Data'
            WHEN dp.name CONTAINS 'Processed' OR dp.name CONTAINS 'Aggregated' THEN 'Processed Data'
            WHEN dp.name CONTAINS 'Combined' OR dp.name CONTAINS 'Summary' THEN 'Analytics'
            ELSE 'Other'
          END AS LifecycleStage,
          count(dp) AS Count,
          collect(dp.name) AS DataProducts
        ORDER BY LifecycleStage
    """).data()
    
    for row in result:
        print(f"🔄 {row['LifecycleStage']}: {row['Count']} products")
        print(f"   Products: {', '.join(row['DataProducts'])}")
    
    # Query 10: Graph Statistics
    print("\n🔟 Knowledge Graph Statistics:")
    print("-" * 30)
    result = kgm.graph.run("""
        MATCH (n)
        RETURN labels(n) AS NodeType, count(n) AS Count
        ORDER BY Count DESC
    """).data()
    
    for row in result:
        print(f"📊 {row['NodeType']}: {row['Count']} nodes")

def interactive_query():
    """Allow user to input custom Cypher queries"""
    
    kgm = DataProductRegistry("bolt://localhost:7687", "neo4j", "password")
    
    print("\n🎯 Interactive Query Mode")
    print("Enter 'quit' to exit")
    print("-" * 30)
    
    while True:
        query = input("\nEnter Cypher query: ").strip()
        
        if query.lower() == 'quit':
            break
            
        if not query:
            continue
            
        try:
            result = kgm.graph.run(query).data()
            
            if result:
                print(f"\n✅ Query returned {len(result)} results:")
                print(json.dumps(result, indent=2, default=str))
            else:
                print("ℹ️ Query executed successfully but returned no results.")
                
        except Exception as e:
            print(f"❌ Query error: {str(e)}")

if __name__ == "__main__":
    try:
        execute_queries()
        
        # Uncomment the line below to enable interactive mode
        # interactive_query()
        
    except Exception as e:
        print(f"❌ Connection error: {str(e)}")
        print("Make sure Neo4j is running and the knowledge graph is populated.") 
