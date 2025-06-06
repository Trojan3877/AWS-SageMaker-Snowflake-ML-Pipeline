
---

### File: `sql/setup_snowflake.sql`

```sql
-- Create a new database for fraud detection (if not exists)
CREATE OR REPLACE DATABASE fraud_db;

-- Use the newly created database
USE DATABASE fraud_db;

-- Create schema (if not exists)
CREATE OR REPLACE SCHEMA public;

-- Create the raw_transactions table
CREATE OR REPLACE TABLE public.raw_transactions (
  transaction_id             STRING,
  account_id                 STRING,
  transaction_amount         FLOAT,
  transaction_date           DATE,
  merchant_id                STRING,
  account_age_days           INTEGER,
  num_prev_transactions      INTEGER,
  is_foreign_transaction     BOOLEAN,
  transaction_category       STRING,
  card_present               BOOLEAN,
  device_id                  STRING,
  ip_address                 STRING
  -- Add other columns as needed for your feature engineering
);

-- Example: Copy data from an internal stage to this table
-- COPY INTO public.raw_transactions
-- FROM @your_internal_stage/sample_transactions.csv
-- FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY '"' SKIP_HEADER = 1);

-- Grant privileges (optional: adjust roles/users accordingly)
GRANT USAGE ON DATABASE fraud_db TO ROLE <YOUR_ROLE>;
GRANT USAGE ON SCHEMA fraud_db.public TO ROLE <YOUR_ROLE>;
GRANT INSERT, SELECT, UPDATE, DELETE ON ALL TABLES IN SCHEMA fraud_db.public TO ROLE <YOUR_ROLE>;
