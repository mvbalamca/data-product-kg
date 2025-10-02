from kg_registry import DataProductRegistry
from kg_dataproduct import DataProduct
from datetime import datetime

# Initialize the registry
kgm = DataProductRegistry("bolt://localhost:7687", "neo4j", "password")

# ============================================================================
# DATA PRODUCTS FOR PIPELINE LINKING SCENARIO
# ============================================================================

# 1. Raw Data Products (Ingest pipelines)
raw_customer_data = DataProduct(
    name="RawCustomerData",
    type="Table",
    short_description="Raw customer data from various sources",
    description="Unprocessed customer information from CRM, web forms, and third-party sources",
    source="CRM, Web Forms, Third-party APIs",
    destination="IOMETE LKH",
    tables=["raw_customers", "raw_customer_profiles"],
    domain="Customer",
    subdomain="CustomerData",
    tags=["raw", "customer", "ingestion"],
    data_classification={"level": "Internal"},
    usage_stats={"access_count": 45},
    owner={"name": "Data Engineering Team", "email": "data.eng@example.com"},
    stewards=[{"name": "Data Quality Team"}],
    environment="Development",
    schedule="Daily",
    pipelines=[{"name": "IngestCustomerData", "status": "Active", "frequency": "Daily"}]
)

raw_sales_data = DataProduct(
    name="RawSalesData", 
    type="Table",
    short_description="Raw sales transactions and orders",
    description="Unprocessed sales data from POS systems, e-commerce platforms, and sales channels",
    source="POS Systems, E-commerce, Sales Channels",
    destination="IOMETE LKH",
    tables=["raw_sales", "raw_orders", "raw_transactions"],
    domain="Sales",
    subdomain="SalesData",
    tags=["raw", "sales", "transactions"],
    data_classification={"level": "Internal"},
    usage_stats={"access_count": 67},
    owner={"name": "Sales Operations", "email": "sales.ops@example.com"},
    stewards=[{"name": "Sales Analytics Team"}],
    environment="Development",
    schedule="Hourly",
    pipelines=[{"name": "IngestSalesData", "status": "Active", "frequency": "Hourly"}]
)

raw_inventory_data = DataProduct(
    name="RawInventoryData",
    type="Table", 
    short_description="Raw inventory levels and movements",
    description="Unprocessed inventory data from warehouses, stores, and suppliers",
    source="Warehouse Systems, Store POS, Supplier APIs",
    destination="IOMETE LKH",
    tables=["raw_inventory", "raw_stock_movements"],
    domain="Inventory",
    subdomain="InventoryData",
    tags=["raw", "inventory", "stock"],
    data_classification={"level": "Internal"},
    usage_stats={"access_count": 38},
    owner={"name": "Inventory Management", "email": "inventory@example.com"},
    stewards=[{"name": "Supply Chain Team"}],
    environment="Development",
    schedule="Daily",
    pipelines=[{"name": "IngestInventory", "status": "Active", "frequency": "Daily"}]
)

# 2. Processed Data Products (Process/Aggregate pipelines)
processed_customer_data = DataProduct(
    name="ProcessedCustomerData",
    type="Table",
    short_description="Cleaned and enriched customer data",
    description="Processed customer data with deduplication, validation, and enrichment",
    source="RawCustomerData",
    destination="Data Warehouse",
    tables=["customers_clean", "customer_profiles_enriched"],
    domain="Customer",
    subdomain="CustomerAnalytics",
    tags=["processed", "customer", "enriched"],
    data_classification={"level": "Internal"},
    usage_stats={"access_count": 89},
    owner={"name": "Customer Analytics", "email": "customer.analytics@example.com"},
    stewards=[{"name": "Data Quality Team"}, {"name": "Customer Success"}],
    environment="Production",
    schedule="Daily",
    pipelines=[{"name": "ProcessCustomerData", "status": "Active", "frequency": "Daily"}]
)

aggregated_sales_data = DataProduct(
    name="AggregatedSalesData",
    type="Table",
    short_description="Aggregated sales metrics and KPIs",
    description="Daily, weekly, and monthly sales aggregations with key performance indicators",
    source="RawSalesData",
    destination="Data Warehouse", 
    tables=["sales_daily", "sales_weekly", "sales_monthly"],
    domain="Sales",
    subdomain="SalesAnalytics",
    tags=["aggregated", "sales", "kpis"],
    data_classification={"level": "Internal"},
    usage_stats={"access_count": 156},
    owner={"name": "Sales Analytics", "email": "sales.analytics@example.com"},
    stewards=[{"name": "Sales Operations"}],
    environment="Production",
    schedule="Daily",
    pipelines=[{"name": "AggregateSales", "status": "Active", "frequency": "Daily"}]
)

aggregated_inventory_data = DataProduct(
    name="AggregatedInventoryData",
    type="Table",
    short_description="Aggregated inventory levels and trends",
    description="Daily inventory snapshots with turnover rates and stock predictions",
    source="RawInventoryData",
    destination="Data Warehouse",
    tables=["inventory_daily", "inventory_trends", "stock_predictions"],
    domain="Inventory",
    subdomain="InventoryAnalytics", 
    tags=["aggregated", "inventory", "trends"],
    data_classification={"level": "Internal"},
    usage_stats={"access_count": 72},
    owner={"name": "Supply Chain Analytics", "email": "supply.analytics@example.com"},
    stewards=[{"name": "Inventory Management"}],
    environment="Production",
    schedule="Daily",
    pipelines=[{"name": "AggregateInventory", "status": "Active", "frequency": "Daily"}]
)

# 3. Combined Data Products (Generate pipelines)
sales_inventory_combined = DataProduct(
    name="SalesAndInventoryCombined",
    type="Table",
    short_description="Combined sales and inventory insights",
    description="Cross-domain analysis combining sales performance with inventory availability",
    source="AggregatedSalesData, AggregatedInventoryData",
    destination="Data Warehouse",
    tables=["sales_inventory_cross", "availability_analysis"],
    domain="Cross-Domain",
    subdomain="SalesInventory",
    tags=["combined", "cross-domain", "insights"],
    data_classification={"level": "Internal"},
    usage_stats={"access_count": 203},
    owner={"name": "Business Intelligence", "email": "bi@example.com"},
    stewards=[{"name": "Sales Analytics"}, {"name": "Supply Chain Analytics"}],
    environment="Production",
    schedule="Daily",
    pipelines=[{"name": "GenerateSalesAndInventory", "status": "Active", "frequency": "Daily"}]
)

customer_sales_summary = DataProduct(
    name="CustomerSalesSummary",
    type="Dashboard",
    short_description="Customer-centric sales performance dashboard",
    description="Comprehensive view of customer behavior and sales performance",
    source="ProcessedCustomerData, AggregatedSalesData",
    destination="PowerBI",
    tables=["customer_sales_summary", "customer_segments"],
    domain="Customer",
    subdomain="CustomerSales",
    tags=["dashboard", "customer", "sales", "summary"],
    data_classification={"level": "Internal"},
    usage_stats={"access_count": 234},
    owner={"name": "Customer Success", "email": "customer.success@example.com"},
    stewards=[{"name": "Customer Analytics"}, {"name": "Sales Analytics"}],
    environment="Production",
    schedule="Daily",
    pipelines=[{"name": "GenerateCustomerSalesSummary", "status": "Active", "frequency": "Daily"}]
)

# ============================================================================
# ADD ALL DATA PRODUCTS TO THE REGISTRY
# ============================================================================

print("🚀 Adding Data Products to Knowledge Graph...")

# Add raw data products
id_raw_customer = kgm.add_dataproduct(raw_customer_data)
id_raw_sales = kgm.add_dataproduct(raw_sales_data)
id_raw_inventory = kgm.add_dataproduct(raw_inventory_data)

# Add processed data products
id_processed_customer = kgm.add_dataproduct(processed_customer_data)
id_aggregated_sales = kgm.add_dataproduct(aggregated_sales_data)
id_aggregated_inventory = kgm.add_dataproduct(aggregated_inventory_data)

# Add combined data products
id_sales_inventory_combined = kgm.add_dataproduct(sales_inventory_combined)
id_customer_sales_summary = kgm.add_dataproduct(customer_sales_summary)

print("✅ All Data Products added successfully!")

# ============================================================================
# LINK PIPELINES AS SPECIFIED
# ============================================================================

print("\n🔗 Linking Pipelines...")

# Link the pipelines as specified in the requirements
kgm.link_pipelines({"name": "IngestCustomerData"}, {"name": "ProcessCustomerData"})
kgm.link_pipelines({"name": "IngestSalesData"}, {"name": "AggregateSales"})
kgm.link_pipelines({"name": "IngestInventory"}, {"name": "AggregateInventory"})
kgm.link_pipelines({"name": "AggregateSalesData"}, {"name": "GenerateSalesAndInventory"})
kgm.link_pipelines({"name": "AggregateInventory"}, {"name": "GenerateSalesAndInventory"})
kgm.link_pipelines({"name": "ProcessCustomerData"}, {"name": "GenerateCustomerSalesSummary"})
kgm.link_pipelines({"name": "AggregateSales"}, {"name": "GenerateCustomerSalesSummary"})

print("✅ All pipeline links created successfully!")

# ============================================================================
# CREATE PIPELINE-TO-DATAPRODUCT RELATIONSHIPS
# ============================================================================

print("\n📦 Linking Pipelines to Data Products...")

# Link pipelines to the data products they produce
kgm.pipeline_produces({"name": "IngestCustomerData", "status": "Active"}, id_raw_customer)
kgm.pipeline_produces({"name": "IngestSalesData", "status": "Active"}, id_raw_sales)
kgm.pipeline_produces({"name": "IngestInventory", "status": "Active"}, id_raw_inventory)
kgm.pipeline_produces({"name": "ProcessCustomerData", "status": "Active"}, id_processed_customer)
kgm.pipeline_produces({"name": "AggregateSales", "status": "Active"}, id_aggregated_sales)
kgm.pipeline_produces({"name": "AggregateInventory", "status": "Active"}, id_aggregated_inventory)
kgm.pipeline_produces({"name": "GenerateSalesAndInventory", "status": "Active"}, id_sales_inventory_combined)
kgm.pipeline_produces({"name": "GenerateCustomerSalesSummary", "status": "Active"}, id_customer_sales_summary)

print("✅ All pipeline-to-dataproduct relationships created!")

# ============================================================================
# AUTO-WIRE DEPENDENCIES
# ============================================================================

print("\n🔗 Auto-wiring data product dependencies...")
kgm.auto_wire_dependencies()

print("\n🎉 Knowledge Graph setup complete!")
print("📊 Summary:")
print(f"   • {8} Data Products created")
print(f"   • {7} Pipeline links established")
print(f"   • {8} Pipeline-to-DataProduct relationships created")
print(f"   • Dependencies auto-wired based on pipeline triggers")