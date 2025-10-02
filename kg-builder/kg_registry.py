import uuid
import yaml
from kg_dataproduct import DataProduct
import json
from py2neo import Graph, Node, Relationship, NodeMatcher
from datetime import datetime

class DataProductRegistry:

    def load_config(self) -> dict:
        path="dataproduct_config.yaml"
        with open(path, "r") as f:
            return yaml.safe_load(f)

    def __init__(self, uri, user, password):
        self.graph = Graph(uri, auth=(user, password))
        self.dataproducts = {}
        self.config = self.load_config()
        self.updatable_fields = self.config.get("updatable_fields", [])

    def add_dataproduct(self, dataproduct: DataProduct) -> str:
        dataproduct_id = str(uuid.uuid4())
        dataproduct.id = dataproduct_id
        self.dataproducts[dataproduct_id] = dataproduct

        # 1️⃣ Core DataProduct Node
        dp_node = Node(
            "DataProduct",
            id=dataproduct_id,
            name=dataproduct.name,
            type=dataproduct.type,
            source=dataproduct.source,
            description=dataproduct.description,
            short_description=dataproduct.short_description,
            destination=dataproduct.destination,
            domain=dataproduct.domain,
            subdomain=dataproduct.subdomain,
            environment=dataproduct.environment,
            schedule=dataproduct.schedule
        )
        self.graph.create(dp_node)

        # 2️⃣ Simple List Properties → Create & Relate
        def create_multiple(label, values, rel):
            for val in values or []:
                node = Node(label, name=val)
                self.graph.merge(node, label, "name")
                self.graph.create(Relationship(dp_node, rel, node))
                
        create_multiple("Tag", dataproduct.tags, "HAS_TAG")
        create_multiple("BusinessTerm", dataproduct.business_terms, "HAS_TERM")
        create_multiple("Glossary", dataproduct.glossary_links, "GLOSSARY_LINK")
        create_multiple("KnownIssue", dataproduct.known_issues, "HAS_ISSUE")
        create_multiple("Documentation", dataproduct.documentation_links, "HAS_DOC")
        create_multiple("FAQ", dataproduct.faqs, "HAS_FAQ")
        create_multiple("Query", dataproduct.sample_queries, "HAS_QUERY")
        create_multiple("Table", dataproduct.tables, "USES_TABLE")
        create_multiple("PIIField", dataproduct.pii_fields, "HAS_PII")

        # 3️⃣ Dictionaries → Nodes with attributes
        def create_dict_node(label, data, rel):
            if data:
                node = Node(label, **data)
                self.graph.create(node)
                self.graph.create(Relationship(dp_node, rel, node))

        create_dict_node("Owner", dataproduct.owner, "OWNED_BY")
        create_dict_node("Manager", dataproduct.manager, "MANAGED_BY")
        create_dict_node("Metrics", dataproduct.metrics, "HAS_METRIC")
        create_dict_node("DataQuality", dataproduct.data_quality, "HAS_QUALITY")
        create_dict_node("Classification", dataproduct.data_classification, "CLASSIFIED_AS")
        create_dict_node("UsageStats", dataproduct.usage_stats, "HAS_USAGE")
        create_dict_node("Team", dataproduct.team, "PART_OF_TEAM")
        create_dict_node("AccessControl", dataproduct.access_controls, "HAS_ACCESS_CTRL")
        create_dict_node("Database", dataproduct.database, "STORED_IN")
        create_dict_node("Schema", dataproduct.schema, "HAS_SCHEMA")

        # 4️⃣ Lists of Dicts → Nodes with attributes
        def create_list_of_dicts(label, items, rel):
            for item in items or []:
                if isinstance(item, dict):
                    node = Node(label, **item)
                    self.graph.create(node)
                    self.graph.create(Relationship(dp_node, rel, node))

        create_list_of_dicts("Steward", dataproduct.stewards, "STEWARDED_BY")
        create_list_of_dicts("Consumer", dataproduct.consumers, "CONSUMED_BY")
        create_list_of_dicts("Policy", dataproduct.policies, "HAS_POLICY")
        create_list_of_dicts("Pipeline", dataproduct.pipelines, "HAS_PIPELINE")
        create_list_of_dicts("Job", dataproduct.jobs, "HAS_JOB")
        create_list_of_dicts("FieldLineage", dataproduct.field_lineage, "HAS_FIELD_LINEAGE")

        print(f"✅ DataProduct '{dataproduct.name}' added with {len(dp_node)} properties and multiple relationships!")
        return dataproduct_id
    
    def update_dataproduct(self, dataproduct: DataProduct) -> bool:
        matcher = NodeMatcher(self.graph)
        updated_fields = []

        if not dataproduct.id:
            print("❗ DataProduct ID is required for update.")
            return False

        dp_node = matcher.match("DataProduct", id=dataproduct.id).first()
        if not dp_node:
            print(f"❗ No DataProduct found with id: {dataproduct.id}")
            return False

        # 1️⃣ update core properties
        def update_core_properties(dataproduct):
            
            #  Core property comparison (PATCH-style)
            core_props = [
                "name", "type", "description", "short_description", "source", "destination",
                "domain", "subdomain", "environment", "schedule"
            ]
            for prop in core_props:
                new_val = getattr(dataproduct, prop, None)
                if new_val is not None:
                    old_val = dp_node.get(prop)
                    if new_val != old_val:
                        dp_node[prop] = new_val
                        updated_fields.append((prop, old_val, new_val))
            if updated_fields:
                self.graph.push(dp_node)

        # 2️⃣ Change logger
        def log_change(field, old, new):
            log_node = Node("ChangeLog",
                            timestamp=datetime.utcnow().isoformat(),
                            field=field,
                            old_value=str(old),
                            new_value=str(new))
            self.graph.create(log_node)
            self.graph.create(Relationship(dp_node, "HAS_CHANGE_LOG", log_node))

        # 3️⃣ Relational updates (smart + logged)
        def update_single_relation(label, data, rel_type):
            if data is not None:
                old_rel = self.graph.run(f"""
                    MATCH (dp:DataProduct {{id: $id}})-[r:{rel_type}]->(n)
                    RETURN n
                """, id=dataproduct.id).data()

                old_data = old_rel[0]['n'] if old_rel else None
                if old_data != data:
                    # Delete old
                    self.graph.run(f"""
                        MATCH (dp:DataProduct {{id: $id}})-[r:{rel_type}]->()
                        DELETE r
                    """, id=dataproduct.id)
                    # Create new
                    node = Node(label, **data)
                    self.graph.merge(node, label, "name" if "name" in data else list(data.keys())[0])
                    self.graph.create(Relationship(dp_node, rel_type, node))
                    log_change(rel_type, old_data, data)

        def update_multi_string_relation(label, values, rel_type):
            if values is not None:
                existing = self.graph.run(f"""
                    MATCH (dp:DataProduct {{id: $id}})-[:{rel_type}]->(n:{label})
                    RETURN collect(n.name) AS existing
                """, id=dataproduct.id).evaluate()

                if set(existing or []) != set(values):
                    # Delete old
                    self.graph.run(f"""
                        MATCH (dp:DataProduct {{id: $id}})-[r:{rel_type}]->()
                        DELETE r
                    """, id=dataproduct.id)
                    # Add new
                    for val in values:
                        node = Node(label, name=val)
                        self.graph.merge(node, label, "name")
                        self.graph.create(Relationship(dp_node, rel_type, node))
                    log_change(rel_type, existing, values)

        def update_multi_dict_relation(label, items, rel_type):
            if items is not None:
                # Always delete and recreate for dicts (simpler/cleaner)
                self.graph.run(f"""
                    MATCH (dp:DataProduct {{id: $id}})-[r:{rel_type}]->()
                    DELETE r
                """, id=dataproduct.id)
                for item in items:
                    if isinstance(item, dict):
                        node = Node(label, **item)
                        self.graph.create(node)
                        self.graph.create(Relationship(dp_node, rel_type, node))
                log_change(rel_type, "previous entries", items)

        # Initiate update of core properties
        update_core_properties(dataproduct)

        # 4️⃣ Dictionary fields
        update_single_relation("Owner", dataproduct.owner, "OWNED_BY")
        update_single_relation("Manager", dataproduct.manager, "MANAGED_BY")
        update_single_relation("Metrics", dataproduct.metrics, "HAS_METRIC")
        update_single_relation("DataQuality", dataproduct.data_quality, "HAS_QUALITY")
        update_single_relation("Classification", dataproduct.data_classification, "CLASSIFIED_AS")
        update_single_relation("UsageStats", dataproduct.usage_stats, "HAS_USAGE")
        update_single_relation("Team", dataproduct.team, "PART_OF_TEAM")
        update_single_relation("AccessControl", dataproduct.access_controls, "HAS_ACCESS_CTRL")
        update_single_relation("Database", dataproduct.database, "STORED_IN")
        update_single_relation("Schema", dataproduct.schema, "HAS_SCHEMA")

        # 5️⃣ Lists of strings
        update_multi_string_relation("Tag", dataproduct.tags, "HAS_TAG")
        update_multi_string_relation("BusinessTerm", dataproduct.business_terms, "HAS_TERM")
        update_multi_string_relation("Glossary", dataproduct.glossary_links, "GLOSSARY_LINK")
        update_multi_string_relation("KnownIssue", dataproduct.known_issues, "HAS_ISSUE")
        update_multi_string_relation("Documentation", dataproduct.documentation_links, "HAS_DOC")
        update_multi_string_relation("FAQ", dataproduct.faqs, "HAS_FAQ")
        update_multi_string_relation("Query", dataproduct.sample_queries, "HAS_QUERY")
        update_multi_string_relation("Table", dataproduct.tables, "USES_TABLE")
        update_multi_string_relation("PIIField", dataproduct.pii_fields, "HAS_PII")

        # 6️⃣ Lists of dicts
        update_multi_dict_relation("Steward", dataproduct.stewards, "STEWARDED_BY")
        update_multi_dict_relation("Consumer", dataproduct.consumers, "CONSUMED_BY")
        update_multi_dict_relation("Policy", dataproduct.policies, "HAS_POLICY")
        update_multi_dict_relation("Pipeline", dataproduct.pipelines, "HAS_PIPELINE")
        update_multi_dict_relation("Job", dataproduct.jobs, "HAS_JOB")
        update_multi_dict_relation("FieldLineage", dataproduct.field_lineage, "HAS_FIELD_LINEAGE")

        # Final log
        if updated_fields:
            print(f"✅ Updated fields for '{dataproduct.name}': {[f[0] for f in updated_fields]}")
        else:
            print(f"⚠️ No core field changes for '{dataproduct.name}'.")

        return True 
            
    def add_dataproduct_dependency_by_id(self, from_dpid: str, to_dpid: str) -> bool:
        matcher = NodeMatcher(self.graph)
        from_dp = matcher.match("DataProduct", id=from_dpid).first()
        to_dp = matcher.match("DataProduct", id=to_dpid).first()
        if not from_dp or not to_dp:
            print("❗ One or both DataProducts not found.")
            return False
        else:
            rel = Relationship(from_dp, "FEEDS_INTO", to_dp)
            self.graph.merge(rel)
            print(f"✅ Added dependency: {from_dp['name']} ➡️ {to_dp['name']}")
            return True    
        
    def add_dataproduct_dependency_by_name(self, from_name, to_name):
        from_id = self.get_dataproduct_id_by_name(from_name)
        to_id = self.get_dataproduct_id_by_name(to_name)
        self.add_dependency(from_id, to_id)        
    
    def link_pipelines(self, pipeline1: dict, pipeline2: dict) -> None:
        # First, try to find existing pipeline nodes
        matcher = NodeMatcher(self.graph)
        p1 = matcher.match("Pipeline", name=pipeline1['name']).first()
        p2 = matcher.match("Pipeline", name=pipeline2['name']).first()
        
        # If not found, create them
        if not p1:
            p1 = Node("Pipeline", **pipeline1)
            self.graph.create(p1)
        if not p2:
            p2 = Node("Pipeline", **pipeline2)
            self.graph.create(p2)
        
        # Create the relationship (use merge to avoid duplicates)
        rel = Relationship(p1, "TRIGGERS", p2)
        self.graph.merge(rel)
        print(f"🔁 {pipeline1['name']} TRIGGERS {pipeline2['name']}")    

    def pipeline_produces(self, pipeline_data: dict, dataproduct_dpid: str) -> None:
        matcher = NodeMatcher(self.graph)
        dp = matcher.match("DataProduct", id=dataproduct_dpid).first()
        
        # Try to find existing pipeline node
        pipeline = matcher.match("Pipeline", name=pipeline_data['name']).first()
        
        # If not found, create it
        if not pipeline:
            pipeline = Node("Pipeline", **pipeline_data)
            self.graph.create(pipeline)
        
        # Create the relationship (use merge to avoid duplicates)
        rel = Relationship(pipeline, "PRODUCES", dp)
        self.graph.merge(rel)
        print(f"📦 {pipeline_data['name']} PRODUCES {dp['name']}")        

    def get_dataproduct_id_by_name(self, name):
        result = self.graph.run("""
            MATCH (dp:DataProduct {name: $name})
            RETURN dp.id AS id
            LIMIT 1
        """, name=name).data()        
        if not result:
            raise ValueError(f"No DataProduct found with name: '{name}'")
        else:        
            return result[0]['id']
    
    def auto_wire_dependencies(self):
        self.graph.run("""
            MATCH (p1:Pipeline)-[:PRODUCES]->(dp1:DataProduct),
                (p1)-[:TRIGGERS]->(p2:Pipeline)-[:PRODUCES]->(dp2:DataProduct)
            MERGE (dp1)-[:FEEDS_INTO]->(dp2)
        """)
        print("🔗 Auto-wired data product dependencies via pipeline triggers.")        