import re
from datetime import datetime

# clientes
def validar_account(row):
    erros = []

    if not row.get('customer_id'):
        erros.append("customer_id ausente")

    if not row.get('first_name') or not row.get('last_name'):
        erros.append("Nome incompleto")

    zip_code = row.get('zip_code', '')
    if not re.match(r'^\d{5}$', zip_code):
        erros.append("ZIP inválido")

    return erros


# produtos
def validar_product(row):
    erros = []

    if not row.get('product_id'):
        erros.append("product_id ausente")

    if not row.get('product_description'):
        erros.append("Nome do produto ausente")

    return erros


# transacoes (IDs opcionais como parametros externos)
def validar_transaction(row, contas_validas=None, produtos_validos=None):
    erros = []

    if not row.get('transaction_id'):
        erros.append("transaction_id ausente")

    if not row.get('transaction_date'):
        erros.append("Data ausente")
    else:
        try:
            datetime.strptime(row['transaction_date'], '%Y-%m-%d')
        except ValueError:
            erros.append("Data em formato inválido")

    if not row.get('product_id'):
        erros.append("product_id ausente")

    if not row.get('account_id'):
        erros.append("account_id ausente")

    try:
        quantidade = int(row.get('quantity', 0))
        if quantidade <= 0:
            erros.append("Quantidade deve ser maior que 0")
    except:
        erros.append("Quantidade inválida")

    # verificacao se os IDs existem, se conjuntos forem passados
    if contas_validas is not None and row.get('account_id') not in contas_validas:
        erros.append("account_id inexistente")
    if produtos_validos is not None and row.get('product_id') not in produtos_validos:
        erros.append("product_id inexistente")

    return erros
