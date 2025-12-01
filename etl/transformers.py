from datetime import datetime


def formatar_nome(nome: str) -> str:
    """
    nomes em title case
    """
    return nome.title() if nome else ""


def combinar_endereco(address_1: str, address_2: str) -> str:
    """
    concatena address_1 e address_2
    """
    if address_1 and address_2:
        return f"{address_1}, {address_2}"
    return address_1 or address_2 or ""


def extrair_data_completa(data_str: str) -> dict:
    """
    recebe uma data em string (YYYY-MM-DD) e separa
    """
    try:
        data = datetime.strptime(data_str, "%Y-%m-%d")
        return {
            'date_id': data.date(),
            'day': data.day,
            'month': data.month,
            'year': data.year,
            'month_name': data.strftime("%B"),
            'quarter': (data.month - 1) // 3 + 1
        }
    except ValueError:
        return {}


def calcular_total_price(unit_price: float, quantity: int) -> float:
    """
    calcula total_price = unit_price * quantity
    """
    return round(unit_price * quantity, 2)
