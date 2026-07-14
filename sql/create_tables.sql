-- DDL Schema Setup Script for Retail Sales ETL Pipeline Database
-- Database: PostgreSQL

-- 1. Source Reference Table
CREATE TABLE IF NOT EXISTS outlet_manager (
    outlet_identifier VARCHAR(20) PRIMARY KEY,
    manager_name VARCHAR(100),
    contact_number VARCHAR(20),
    email VARCHAR(100)
);

-- 2. Dimension Tables
CREATE TABLE IF NOT EXISTS dim_product (
    product_id SERIAL PRIMARY KEY,
    item_identifier VARCHAR(20) NOT NULL UNIQUE,
    item_weight NUMERIC(5, 2),
    item_fat_content VARCHAR(20),
    item_type VARCHAR(100),
    item_mrp NUMERIC(10, 2)
);

CREATE TABLE IF NOT EXISTS dim_outlet (
    outlet_id SERIAL PRIMARY KEY,
    outlet_identifier VARCHAR(20) NOT NULL UNIQUE,
    outlet_establishment_year INTEGER,
    outlet_size VARCHAR(20),
    outlet_location_type VARCHAR(20),
    outlet_type VARCHAR(50)
);

-- 3. Fact Table
CREATE TABLE IF NOT EXISTS fact_sales (
    sales_id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES dim_product(product_id),
    outlet_id INTEGER REFERENCES dim_outlet(outlet_id),
    item_visibility NUMERIC(10, 8),
    item_outlet_sales NUMERIC(12, 2),
    load_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source_record_id VARCHAR(100)
);

-- 4. Audit, Reporting & Log Tables
CREATE TABLE IF NOT EXISTS rejected_records (
    reject_id SERIAL PRIMARY KEY,
    item_identifier VARCHAR(20),
    reason TEXT,
    rejected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sales_summary (
    summary_id SERIAL PRIMARY KEY,
    outlet_identifier VARCHAR(20),
    item_type VARCHAR(100),
    total_sales NUMERIC(15, 2),
    average_sales NUMERIC(15, 2),
    total_products INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS etl_metadata (
    id SERIAL PRIMARY KEY,
    pipeline_name VARCHAR(100),
    source_name VARCHAR(100),
    last_run_timestamp TIMESTAMP,
    last_processed_file VARCHAR(255),
    total_records INTEGER,
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS etl_audit_log (
    audit_id SERIAL PRIMARY KEY,
    pipeline_name VARCHAR(100),
    step_name VARCHAR(100),
    records_processed INTEGER,
    status VARCHAR(20),
    error_message TEXT,
    execution_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
