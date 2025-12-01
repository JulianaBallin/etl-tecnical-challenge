import psycopg2
import os
import glob
import csv
from etl.db import get_connection
from etl.validators import validar_transaction

def test_tabelas_existem():
    conn = get_connection()
    cur = conn.cursor()

    tabelas = [
        'operacional.accounts',
        'operacional.products',
        'operacional.transactions',
        'mart.dim_account',
        'mart.dim_product',
        'mart.dim_date',
        'mart.fact_sales'
    ]

    for tabela in tabelas:
        cur.execute(f"SELECT to_regclass('{tabela}')")
        resultado = cur.fetchone()[0]
        assert resultado == tabela, f"Tabela {tabela} não encontrada."

    cur.close()
    conn.close()


def test_total_linhas_transactions():
    conn = get_connection()
    cur = conn.cursor()

    total_validas = 0
    with open('data/transactions.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            erros = validar_transaction(row)
            if not erros:
                total_validas += 1

    cur.execute("SELECT COUNT(*) FROM operacional.transactions")
    total_banco = cur.fetchone()[0]

    assert total_validas == total_banco, f"Numero de transações carregadas está incorreto. CSV: {total_validas}, Banco: {total_banco}"

    cur.close()
    conn.close()


def test_total_price_nunca_negativo():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM mart.fact_sales WHERE total_price < 0")
    negativos = cur.fetchone()[0]

    assert negativos == 0, "Existem registros com total_price negativo na fact_sales."

    cur.close()
    conn.close()
