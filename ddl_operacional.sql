-- schema operacional
CREATE SCHEMA IF NOT EXISTS operacional;

-- remover as tabelas se ja existirem 
DROP TABLE IF EXISTS operacional.transactions;
DROP TABLE IF EXISTS operacional.products;
DROP TABLE IF EXISTS operacional.accounts;

-- tabela de contas (clientes)
CREATE TABLE operacional.accounts (
    customer_id VARCHAR PRIMARY KEY,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    address_1 VARCHAR,
    address_2 VARCHAR,
    city VARCHAR,
    state VARCHAR,
    zip_code VARCHAR NOT NULL
);

-- tabela de produtos
CREATE TABLE operacional.products (
    product_id VARCHAR PRIMARY KEY,
    product_code VARCHAR,
    product_name VARCHAR NOT NULL,
    unit_price NUMERIC(10, 2)
);

-- tabela de transacoes
CREATE TABLE operacional.transactions (
    transaction_id VARCHAR PRIMARY KEY,
    customer_id VARCHAR NOT NULL,
    product_id VARCHAR NOT NULL,
    transaction_date DATE NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES operacional.accounts(customer_id),
    FOREIGN KEY (product_id) REFERENCES operacional.products(product_id)
);
