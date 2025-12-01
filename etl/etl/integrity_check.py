from etl.db import get_connection

def carregar_ids_validos():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT customer_id FROM operacional.accounts")
    accounts = {row[0] for row in cur.fetchall()}

    cur.execute("SELECT product_id FROM operacional.products")
    products = {row[0] for row in cur.fetchall()}

    cur.close()
    conn.close()

    return accounts, products
