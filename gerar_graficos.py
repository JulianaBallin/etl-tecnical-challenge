import pandas as pd
import matplotlib.pyplot as plt
import os

os.makedirs("graficos", exist_ok=True)

# 1. top 5 produtos por receita
df1 = pd.read_csv('reports/q1.csv')
plt.figure(figsize=(8, 5))
plt.bar(df1['product_name'], df1['total_revenue'])
plt.title('Top 5 Produtos por Receita (Último Ano Completo)')
plt.xlabel('Produto')
plt.ylabel('Receita Total')
plt.tight_layout()
plt.savefig('graficos/q1_top_5_receita.png')

# 2. evolucao mensal de vendas
df2 = pd.read_csv('reports/q2.csv')
plt.figure(figsize=(10, 5))
plt.plot(df2['month'], df2['total_quantity'], label='Quantidade', marker='o')
plt.plot(df2['month'], df2['total_revenue'], label='Receita', marker='s')
plt.title('Evolução Mensal de Vendas (2024)')
plt.xlabel('Mês')
plt.ylabel('Valor')
plt.legend()
plt.tight_layout()
plt.savefig('graficos/q2_evolucao_mensal.png')

# 3. clientes com +10 unidades
df3 = pd.read_csv('reports/q3.csv')
df3_grouped = df3.groupby('account_id').size().reset_index(name='transacoes')
df3_top = df3_grouped.sort_values(by='transacoes', ascending=False).head(10)
plt.figure(figsize=(10, 5))
plt.bar(df3_top['account_id'].astype(str), df3_top['transacoes'])
plt.title('Top 10 Clientes com Mais Transações (>10 unidades)')
plt.xlabel('ID do Cliente')
plt.ylabel('Nº de Transações')
plt.tight_layout()
plt.savefig('graficos/q3_top_clientes.png')

# 4. receita media por estado
df4 = pd.read_csv('reports/q4.csv')
plt.figure(figsize=(8, 5))
plt.bar(df4['state'], df4['receita_media_por_cliente'])
plt.title('Receita Média por Cliente (Estado)')
plt.xlabel('Estado')
plt.ylabel('Receita Média')
plt.tight_layout()
plt.savefig('graficos/q4_receita_estado.png')

# 5. crescimento percentual mes a mes
df5 = pd.read_csv('reports/q5.csv', parse_dates=['mes'])
plt.figure(figsize=(10, 5))
plt.plot(df5['mes'], df5['crescimento_percentual'], marker='o')
plt.title('Crescimento de Receita Mês a Mês')
plt.xlabel('Mês')
plt.ylabel('Crescimento (%)')
plt.grid(True)
plt.tight_layout()
plt.savefig('graficos/q5_crescimento_percentual.png')
