import csv
import os
from datetime import datetime
from etl.db import get_connection
from etl.validators import (
    validar_account,
    validar_product,
    validar_transaction
)
from etl.transformers import (
    formatar_nome,
    combinar_endereco,
    extrair_data_completa,
    calcular_total_price
)


# carregamento operacional
def carregar_accounts():
    conn = get_connection()
    cur = conn.cursor()
    rejeitadas = []

    with open('data/accounts.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            erros = validar_account(row)
            if erros:
                row['motivo'] = "; ".join(erros)
                rejeitadas.append(row)
                continue

            cur.execute("""
                INSERT INTO operacional.accounts (
                    customer_id, first_name, last_name,
                    address_1, address_2, city, state, zip_code
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (customer_id) DO NOTHING
            """, (
                row['customer_id'],
                formatar_nome(row['first_name']),
                formatar_nome(row['last_name']),
                row['address_1'],
                row['address_2'],
                row['city'],
                row['state'],
                row['zip_code']
            ))

    conn.commit()
    cur.close()
    conn.close()

    if rejeitadas:
        salvar_rejeitadas(rejeitadas, "accounts")


def carregar_products():
    conn = get_connection()
    cur = conn.cursor()
    rejeitadas = []

    with open('data/products.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            erros = validar_product(row)
            if erros:
                row['motivo'] = "; ".join(erros)
                rejeitadas.append(row)
                continue

            precos_ficticios = {
                '200': 4.50,
                '201': 5.20,
                '202': 3.90,
                '203': 4.10,
                '204': 5.00
            }

            unit_price = precos_ficticios.get(row['product_id'], 1.00)

            cur.execute("""
                INSERT INTO operacional.products (
                    product_id, product_code, product_name, unit_price
                ) VALUES (%s, %s, %s, %s)
                ON CONFLICT (product_id) DO NOTHING
            """, (
                row['product_id'],
                row['product_code'],
                formatar_nome(row['product_description']),
                unit_price
            ))

    conn.commit()
    cur.close()
    conn.close()

    if rejeitadas:
        salvar_rejeitadas(rejeitadas, "products")


def carregar_transactions():
    conn = get_connection()
    cur = conn.cursor()
    rejeitadas = []

    # coleta os IDs validos do banco antes da validacao
    cur.execute("SELECT customer_id FROM operacional.accounts")
    contas_validas = {str(row[0]) for row in cur.fetchall()}

    cur.execute("SELECT product_id FROM operacional.products")
    produtos_validos = {str(row[0]) for row in cur.fetchall()}

    with open('data/transactions.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            erros = validar_transaction(row, contas_validas, produtos_validos)
            if erros:
                row['motivo'] = "; ".join(erros)
                row['data_rejeicao'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                rejeitadas.append(row)
                continue

            customer_id = row['account_id']

            cur.execute("""
                INSERT INTO operacional.transactions (
                    transaction_id, customer_id, product_id, transaction_date, quantity
                ) VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (transaction_id) DO NOTHING
            """, (
                row['transaction_id'],
                customer_id,
                row['product_id'],
                row['transaction_date'],
                int(row['quantity'])
            ))

    conn.commit()
    cur.close()
    conn.close()

    if rejeitadas:
        salvar_rejeitadas(rejeitadas, "transactions")


# carregamento analitico
def carregar_dim_account():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO mart.dim_account (account_id, full_name, city, state, zip_code)
        SELECT
            customer_id,
            CONCAT(UPPER(LEFT(first_name, 1)), LOWER(SUBSTRING(first_name FROM 2))) || ' ' ||
            CONCAT(UPPER(LEFT(last_name, 1)), LOWER(SUBSTRING(last_name FROM 2))) AS full_name,
            city, state, zip_code
        FROM operacional.accounts
        ON CONFLICT (account_id) DO NOTHING;
    """)
    conn.commit()
    cur.close()
    conn.close()


def carregar_dim_product():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO mart.dim_product (product_id, product_name, unit_price)
        SELECT product_id, product_name, unit_price
        FROM operacional.products
        ON CONFLICT (product_id) DO NOTHING;
    """)
    conn.commit()
    cur.close()
    conn.close()


def carregar_dim_date():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT DISTINCT transaction_date FROM operacional.transactions")
    datas = cur.fetchall()

    for (data,) in datas:
        data_info = extrair_data_completa(str(data))
        if data_info:
            cur.execute("""
                INSERT INTO mart.dim_date (date_id, day, month, year, month_name, quarter)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (date_id) DO NOTHING;
            """, (
                data_info['date_id'],
                data_info['day'],
                data_info['month'],
                data_info['year'],
                data_info['month_name'],
                data_info['quarter']
            ))

    conn.commit()
    cur.close()
    conn.close()


def carregar_fact_sales():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            t.transaction_id,
            t.customer_id,
            t.product_id,
            t.transaction_date,
            t.quantity,
            p.unit_price
        FROM operacional.transactions t
        JOIN operacional.products p ON t.product_id = p.product_id
    """)
    transacoes = cur.fetchall()

    for trans in transacoes:
        _, customer_id, product_id, date_id, quantity, unit_price = trans
        total_price = calcular_total_price(unit_price, quantity)

        cur.execute("""
            INSERT INTO mart.fact_sales (
                account_id, product_id, date_id,
                quantity, unit_price, total_price
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            customer_id,
            product_id,
            date_id,
            quantity,
            unit_price,
            total_price
        ))

    conn.commit()
    cur.close()
    conn.close()


# salvar logs
def salvar_rejeitadas(rejeitadas, nome_base):
    """
    Salva rejeicoes em um unico arquivo CSV por tipo,
    acrescentando novas linhas com data/hora no campo 'data_rejeicao'.
    """
    import csv
    from datetime import datetime

    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # adiciona campo de data_log aos registros
    for row in rejeitadas:
        row["data_log"] = timestamp

    path = f"logs/rejected_{nome_base}.csv"
    escrever_cabecalho = not os.path.exists(path)

    with open(path, 'a', newline='', encoding='utf-8') as log:
        fieldnames = list(rejeitadas[0].keys())
        writer = csv.DictWriter(log, fieldnames=fieldnames)

        if escrever_cabecalho:
            writer.writeheader()

        writer.writerows(rejeitadas)
