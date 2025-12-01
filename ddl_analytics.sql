-- criacao do schema analitico
CREATE SCHEMA IF NOT EXISTS mart;

-- tabela de dimensao: contas
CREATE TABLE IF NOT EXISTS mart.dim_account (
    account_id VARCHAR PRIMARY KEY,
    full_name VARCHAR NOT NULL,
    city VARCHAR,
    state VARCHAR,
    zip_code VARCHAR
);

-- tabela de dimensao: produtos
CREATE TABLE IF NOT EXISTS mart.dim_product (
    product_id VARCHAR PRIMARY KEY,
    product_name VARCHAR NOT NULL,
    unit_price NUMERIC(10, 2) NOT NULL
);

-- tabela de dimensao: datas
CREATE TABLE IF NOT EXISTS mart.dim_date (
    date_id DATE PRIMARY KEY,
    day INTEGER,
    month INTEGER,
    year INTEGER,
    month_name VARCHAR,
    quarter INTEGER
);

-- tabela fato particionada por ano-mes (sem PK/FK por limitação)
DROP TABLE IF EXISTS mart.fact_sales CASCADE;

CREATE TABLE mart.fact_sales (
    account_id VARCHAR NOT NULL,
    product_id VARCHAR NOT NULL,
    date_id DATE NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price NUMERIC(10,2) NOT NULL,
    total_price NUMERIC(12,2) NOT NULL
) PARTITION BY RANGE (date_id);

-- particoes e indices de 2023 a 2025
DO $$
DECLARE
    ano INT;
    mes INT;
    data_ini DATE;
    data_fim DATE;
    nome_tabela TEXT;
BEGIN
    FOR ano IN 2023..2025 LOOP
        FOR mes IN 1..12 LOOP
            data_ini := TO_DATE(ano || '-' || mes || '-01', 'YYYY-MM-DD');
            data_fim := (data_ini + INTERVAL '1 month');
            nome_tabela := FORMAT('fact_sales_%s_%s',
                ano, LPAD(mes::TEXT, 2, '0'));

            EXECUTE FORMAT($sql$
                CREATE TABLE IF NOT EXISTS mart.%I PARTITION OF mart.fact_sales
                FOR VALUES FROM (%L) TO (%L);
            $sql$, nome_tabela, data_ini, data_fim);

            EXECUTE FORMAT($sql$
                CREATE INDEX IF NOT EXISTS idx_%I ON mart.%I (date_id, product_id);
            $sql$, nome_tabela, nome_tabela);
        END LOOP;
    END LOOP;
END
$$;
