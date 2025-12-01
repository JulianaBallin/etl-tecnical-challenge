import psycopg2
from etl.db import get_connection
from etl.loader import (
    carregar_accounts,
    carregar_products,
    carregar_transactions,
    carregar_dim_account,
    carregar_dim_product,
    carregar_dim_date,
    carregar_fact_sales
)
from etl.report_generator import gerar_relatorios


def executar_sql(path_arquivo):
    """
    executa o conteudo de um arquivo .sql no bd
    """
    with open(path_arquivo, 'r') as f:
        sql = f.read()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()


def main():
    print("iniciando o processo de ETL")

    # tabelas operacionais
    print("executando ddl_operacional.sql")
    executar_sql("ddl_operacional.sql")

    # tabelas analíticas
    print("executando ddl_analytics.sql")
    executar_sql("ddl_analytics.sql")

    print("tabelas criadas com sucesso")

    # dados operacionais
    print("carregando accounts")
    carregar_accounts()
    print("accounts carregados com sucesso")

    print("carregando products")
    carregar_products()
    print("products carregados com sucesso")

    print("carregando transactions")
    carregar_transactions()
    print("transactions carregadas com sucesso")

    # dados analiticos (dimensoes)
    print("carregando dimensão dim_account")
    carregar_dim_account()
    print("dim_account carregada")

    print("carregando dimensão dim_product")
    carregar_dim_product()
    print("dim_product carregada")

    print("carregando dimensão dim_date")
    carregar_dim_date()
    print("dim_date carregada")

    # tabela facto
    print("carregando tabela fato fact_sales")
    carregar_fact_sales()
    print("fact_sales carregada com sucesso")

    # relatorios
    print("gerando relatórios das consultas analíticas.")
    gerar_relatorios()
    print("relatórios salvos em reports/")


if __name__ == "__main__":
    main()
