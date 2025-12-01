from fpdf import FPDF
import pandas as pd
from datetime import datetime
import os

# pasta de gráficos
os.makedirs("graficos", exist_ok=True)

# classe para PDF
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Relatório Analítico de Vendas", border=False, ln=True, align="C")
        self.set_font("Arial", "", 10)
        self.cell(0, 10, f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align="C")
        self.ln(5)

    def chapter_title(self, title):
        self.set_font("Arial", "B", 12)
        self.set_text_color(40, 40, 40)
        self.cell(0, 10, title, ln=True)
        self.ln(2)

    def chapter_body(self, df):
        self.set_font("Arial", "", 10)
        colunas = list(df.columns)
        self.set_fill_color(240, 240, 240)
        self.set_text_color(0)
        col_width = self.w / (len(colunas) + 1)

        # cabecalho da tabela
        for col in colunas:
            self.cell(col_width, 10, col, 1, 0, 'C', 1)
        self.ln()

        # dados
        for i, row in df.iterrows():
            for val in row:
                self.cell(col_width, 10, str(val), 1, 0, 'C')
            self.ln()
        self.ln()

    def insert_image(self, path):
        if os.path.exists(path):
            self.image(path, w=160)
            self.ln(10)

# inicia o PDF
pdf = PDF()
pdf.add_page()

# caminhos
relatorios = [
    ("Top 5 Produtos por Receita", "reports/q1.csv", "graficos/q1_top_5_receita.png"),
    ("Evolução Mensal de Vendas (2024)", "reports/q2.csv", "graficos/q2_evolucao_mensal.png"),
    ("Top 10 Clientes com Mais Transações (>10)", "reports/q3.csv", "graficos/q3_top_clientes.png"),
    ("Receita Média por Estado", "reports/q4.csv", "graficos/q4_receita_estado.png"),
    ("Crescimento Percentual Mês a Mês", "reports/q5.csv", "graficos/q5_crescimento_percentual.png"),
]

# adiciona cada secao
for titulo, csv_path, grafico_path in relatorios:
    pdf.chapter_title(titulo)
    df = pd.read_csv(csv_path)
    pdf.chapter_body(df.head(10))  # limita a 10 linhas
    pdf.insert_image(grafico_path)

# salva o PDF
pdf.output("relatorio_analitico.pdf")

print("Relatório PDF gerado com sucesso: relatorio_analitico.pdf")
