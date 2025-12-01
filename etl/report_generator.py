import psycopg2
import os
import csv
from etl.db import get_connection

def gerar_relatorios():
    conn = get_connection()
    cur = conn.cursor()

    # pasta reports/ existe
    os.makedirs("reports", exist_ok=True)

    # leitura do arquivo analytics.sql
    with open("analytics.sql", "r", encoding="utf-8") as f:
        conteudo = f.read()

    # separa as consultas
    consultas = [q.strip() for q in conteudo.split(';') if 'select' in q.lower()]

    if not consultas:
        print("Nenhuma consulta encontrada no analytics.sql")
        return

    for i, query in enumerate(consultas, 1):
        print(f"Executando consulta {i}: {query[:60]}...")
        try:
            cur.execute(query)
            colunas = [desc[0] for desc in cur.description]
            linhas = cur.fetchall()

            nome_arquivo = f"reports/q{i}.csv"
            with open(nome_arquivo, "w", newline='', encoding="utf-8") as f_out:
                writer = csv.writer(f_out)
                writer.writerow(colunas)
                writer.writerows(linhas)

            print(f"Consulta {i} salva em {nome_arquivo}")
        except Exception as e:
            print(f"Erro ao executar consulta {i}: {e}")

    cur.close()
    conn.close()