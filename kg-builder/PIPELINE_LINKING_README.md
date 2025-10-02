# Pipeline Linking Knowledge Graph Setup

This document describes the comprehensive test data setup for pipeline linking in the Knowledge Graph.

## Overview

The setup creates a complete data pipeline ecosystem with 8 data products and 7 pipeline links, demonstrating a realistic data flow from raw ingestion to final analytics dashboards.

## Data Products Architecture

### 1. Raw Data Products (Ingest Layer)
- **RawCustomerData**: Raw customer information from CRM, web forms, and third-party sources
- **RawSalesData**: Raw sales transactions and orders from POS systems and e-commerce
- **RawInventoryData**: Raw inventory levels and movements from warehouses and stores

### 2. Processed Data Products (Process/Aggregate Layer)
- **ProcessedCustomerData**: Cleaned and enriched customer data with deduplication
- **AggregatedSalesData**: Daily, weekly, and monthly sales aggregations with KPIs
- **AggregatedInventoryData**: Daily inventory snapshots with turnover rates

### 3. Combined Data Products (Generate Layer)
- **SalesAndInventoryCombined**: Cross-domain analysis combining sales and inventory
- **CustomerSalesSummary**: Customer-centric sales performance dashboard

## Pipeline Flow

```
IngestCustomerData → ProcessCustomerData → GenerateCustomerSalesSummary
IngestSalesData → AggregateSales → GenerateCustomerSalesSummary
IngestInventory → AggregateInventory → GenerateSalesAndInventory
AggregateSalesData → GenerateSalesAndInventory
```

## Detailed Pipeline Links

| From Pipeline | To Pipeline | Description |
|---------------|-------------|-------------|
| IngestCustomerData | ProcessCustomerData | Raw customer data triggers processing |
| IngestSalesData | AggregateSales | Raw sales data triggers aggregation |
| IngestInventory | AggregateInventory | Raw inventory data triggers aggregation |
| AggregateSalesData | GenerateSalesAndInventory | Sales aggregation triggers combined analysis |
| AggregateInventory | GenerateSalesAndInventory | Inventory aggregation triggers combined analysis |
| ProcessCustomerData | GenerateCustomerSalesSummary | Processed customer data triggers summary |
| AggregateSales | GenerateCustomerSalesSummary | Sales aggregation triggers customer summary |

## Data Product Dependencies

The auto-wiring feature creates the following data product dependencies based on pipeline triggers:

- RawCustomerData → ProcessedCustomerData
- RawSalesData → AggregatedSalesData  
- RawInventoryData → AggregatedInventoryData
- AggregatedSalesData → SalesAndInventoryCombined
- AggregatedInventoryData → SalesAndInventoryCombined
- ProcessedCustomerData → CustomerSalesSummary
- AggregatedSalesData → CustomerSalesSummary

## Usage

### Running the Setup

```bash
cd kg-builder
python kg_ops.py
```

### Testing the Setup

```bash
python test_pipeline_links.py
```

### Verification Queries

#### Check all pipeline links:
```cypher
MATCH (p1:Pipeline)-[r:TRIGGERS]->(p2:Pipeline)
RETURN p1.name AS from_pipeline, p2.name AS to_pipeline
```

#### Check data product dependencies:
```cypher
MATCH (dp1:DataProduct)-[r:FEEDS_INTO]->(dp2:DataProduct)
RETURN dp1.name AS from_dp, dp2.name AS to_dp
```

#### Check pipeline-to-dataproduct relationships:
```cypher
MATCH (p:Pipeline)-[r:PRODUCES]->(dp:DataProduct)
RETURN p.name AS pipeline, dp.name AS dataproduct
```

## Data Product Details

### RawCustomerData
- **Type**: Table
- **Domain**: Customer
- **Subdomain**: CustomerData
- **Destination**: Data Lake
- **Schedule**: Daily
- **Owner**: Data Engineering Team

### RawSalesData
- **Type**: Table
- **Domain**: Sales
- **Subdomain**: SalesData
- **Destination**: Data Lake
- **Schedule**: Hourly
- **Owner**: Sales Operations

### RawInventoryData
- **Type**: Table
- **Domain**: Inventory
- **Subdomain**: InventoryData
- **Destination**: Data Lake
- **Schedule**: Daily
- **Owner**: Inventory Management

### ProcessedCustomerData
- **Type**: Table
- **Domain**: Customer
- **Subdomain**: CustomerAnalytics
- **Destination**: Data Warehouse
- **Schedule**: Daily
- **Owner**: Customer Analytics

### AggregatedSalesData
- **Type**: Table
- **Domain**: Sales
- **Subdomain**: SalesAnalytics
- **Destination**: Data Warehouse
- **Schedule**: Daily
- **Owner**: Sales Analytics

### AggregatedInventoryData
- **Type**: Table
- **Domain**: Inventory
- **Subdomain**: InventoryAnalytics
- **Destination**: Data Warehouse
- **Schedule**: Daily
- **Owner**: Supply Chain Analytics

### SalesAndInventoryCombined
- **Type**: Table
- **Domain**: Cross-Domain
- **Subdomain**: SalesInventory
- **Destination**: Data Warehouse
- **Schedule**: Daily
- **Owner**: Business Intelligence

### CustomerSalesSummary
- **Type**: Dashboard
- **Domain**: Customer
- **Subdomain**: CustomerSales
- **Destination**: PowerBI
- **Schedule**: Daily
- **Owner**: Customer Success

## Key Features

1. **Complete Data Lineage**: Full traceability from raw data to final dashboards
2. **Cross-Domain Integration**: Sales and inventory data combined for insights
3. **Realistic Data Flow**: Mimics actual enterprise data pipeline patterns
4. **Auto-Wiring**: Automatic dependency creation based on pipeline relationships
5. **Comprehensive Metadata**: Rich metadata for each data product including owners, stewards, and usage stats

## Testing

The test script (`test_pipeline_links.py`) verifies:
- All pipeline nodes exist
- All pipeline relationships are established
- All data products are created
- Pipeline-to-dataproduct relationships are correct
- Auto-wired dependencies are properly created

Run the test to ensure everything is working correctly:

```bash
python test_pipeline_links.py
``` 