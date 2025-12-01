import psycopg2

def get_connection():
    return psycopg2.connect(
        host="postgres",
        dbname="postgres",
        user="postgres",
        password="postgres"
    )
