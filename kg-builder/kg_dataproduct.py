
from typing import List, Dict, Optional

class DataProduct:
    def __init__(
        self,
        name: Optional[str] = None,
        type: Optional[str] = None,
        description: Optional[str] = None,
        short_description: Optional[str] = None,
        source: Optional[str] = None,
        destination: Optional[str] = None,
        tables: Optional[List[str]] = None,
        pipelines: Optional[List[Dict]] = None,
        owner: Optional[Dict[str, str]] = None,
        manager: Optional[Dict[str, str]] = None,
        domain: Optional[str] = None,
        subdomain: Optional[str] = None,
        metrics: Optional[Dict] = None,
        data_quality: Optional[Dict] = None,
        data_classification: Optional[Dict] = None,

        # 🔍 Metadata & Discovery
        tags: Optional[List[str]] = None,
        business_terms: Optional[List[str]] = None,
        glossary_links: Optional[List[str]] = None,
        schema: Optional[Dict] = None,

        # 📊 Quality, Trust, and Usage
        usage_stats: Optional[Dict] = None,
        known_issues: Optional[List[str]] = None,

        # 🤝 People & Responsibility
        stewards: Optional[List[Dict[str, str]]] = None,
        consumers: Optional[List[Dict[str, str]]] = None,
        team: Optional[Dict[str, str]] = None,

        # 🔐 Security & Compliance
        policies: Optional[List[Dict[str, str]]] = None,
        access_controls: Optional[Dict[str, str]] = None,
        pii_fields: Optional[List[str]] = None,

        # 🧪 Tech & Infra
        database: Optional[Dict[str, str]] = None,
        environment: Optional[str] = None,
        jobs: Optional[List[Dict]] = None,
        schedule: Optional[str] = None,

        # 📚 Documentation
        documentation_links: Optional[List[str]] = None,
        faqs: Optional[List[str]] = None,
        sample_queries: Optional[List[str]] = None,

        # 🔁 Lineage
        upstream_sources: Optional[List[str]] = None,
        downstream_targets: Optional[List[str]] = None,
        field_lineage: Optional[List[Dict[str, str]]] = None,

    ):
        self.name = name
        self.type = type
        self.description = description
        self.short_description = short_description
        self.source = source
        self.destination = destination
        self.tables = tables or []
        self.pipelines = pipelines or []
        self.owner = owner
        self.manager = manager
        self.domain = domain
        self.subdomain = subdomain
        self.metrics = metrics
        self.data_quality = data_quality
        self.data_classification = data_classification

        # Discovery
        self.tags = tags or []
        self.business_terms = business_terms or []
        self.glossary_links = glossary_links or []
        self.schema = schema

        # Quality & Usage
        self.usage_stats = usage_stats or {}
        self.known_issues = known_issues or []

        # People
        self.stewards = stewards or []
        self.consumers = consumers or []
        self.team = team

        # Security
        self.policies = policies or []
        self.access_controls = access_controls
        self.pii_fields = pii_fields or []

        # Infra
        self.database = database
        self.environment = environment
        self.jobs = jobs or []
        self.schedule = schedule

        # Docs
        self.documentation_links = documentation_links or []
        self.faqs = faqs or []
        self.sample_queries = sample_queries or []

        # Lineage
        self.upstream_sources = upstream_sources or []
        self.downstream_targets = downstream_targets or []
        self.field_lineage = field_lineage or []

    def __repr__(self):
        return f"<DataProduct name={self.name}, domain={self.domain}, subdomain={self.subdomain}>"

    def summary(self) -> str:
        return (
            f"📦 Data Product: {self.name}\n"
            f"💡 Type: {self.type}\n"
            f"🗂️ Source / Destination: {self.source} / {self.destination}\n"
            f"📝 Description: {self.short_description}\n"
            f"👑 Domain/Sub: {self.domain} / {self.subdomain}\n"
            f"📊 Tables: {len(self.tables)} | Pipelines: {len(self.pipelines)}\n"
            f"👥 Owner: {self.owner.get('name') if self.owner else 'N/A'} | "
            f"Manager: {self.manager.get('name') if self.manager else 'N/A'}\n"
            f"🏷️ Tags: {', '.join(self.tags) if self.tags else 'None'}\n"
            f"🔒 Classification: {self.data_classification.get('level') if self.data_classification else 'Unclassified'}\n"
            f"📈 Usage: {self.usage_stats.get('access_count') if self.usage_stats else 'Unknown'} accesses\n"
            f"🧪 Quality Issues: {len(self.known_issues)} known\n"
            f"🔁 Lineage: {len(self.upstream_sources)} upstream / {len(self.downstream_targets)} downstream\n"
        )