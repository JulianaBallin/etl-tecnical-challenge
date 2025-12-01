# Desafio de Engenharia de Dados - ETL com Python e PostgreSQL

## Sobre o Projeto
Este projeto implementa um pipeline completo de ETL (Extração, Transformação e Carga) utilizando Python e PostgreSQL, com foco na limpeza de dados, validação, análise e geração de relatórios e visualizações.

O objetivo é simular um fluxo de dados operacionais (accounts, products e transactions), tratá-los e armazenar as informações em um modelo dimensional (data warehouse) para análise.

## Estrutura do Projeto
```
tecnical_challenge/
├── data/                    # Arquivos CSV brutos de entrada
├── etl/                     # Códigos de ETL
│   ├── db.py
│   ├── loader.py
│   ├── transformers.py
│   ├── validators.py
│   └── report_generator.py
├── reports/                 # Arquivos CSV dos relatórios analíticos gerados
├── graficos/                # Gráficos gerados a partir dos relatórios
├── tests/                   # Testes automatizados com pytest
│   └── test_etl.py
├── analytics.sql            # Consultas analíticas
├── ddl_operacional.sql      # Criação de tabelas operacionais
├── ddl_analytics.sql        # Criação de tabelas dimensionais (data warehouse)
├── main.py                  # Script principal de execução do ETL
├── graficos.py              # Geração de gráficos a partir dos relatórios
├── gerar_pdf_relatorios.py  # Gera um relatório PDF com os resultados
├── requirements.txt         # Dependências Python
├── Dockerfile               # Ambiente Docker para execução
├── docker-compose.yml       # Orquestração do container
└── README.md                # Documentação
```

## Como Executar o Projeto

### Requisitos:
- Docker + Docker Compose

### 1. Build da imagem:
```bash
docker-compose build
```

### 2. Executar o processo ETL completo:
```bash
docker-compose run run
```

### 3. Executar os testes automatizados:
```bash
docker-compose run test
```

### 4. Gerar os gráficos localmente:
```bash
python graficos.py
```

### 5. Gerar PDF com os relatórios:
```bash
python gerar_pdf_relatorios.py
```

## Funcionalidades
- Validação dos dados (nome, CEP, datas, IDs inexistentes)
- Registro de erros em logs separados por tipo
- Carga dos dados operacionais em tabelas normalizadas
- Modelagem dimensional com fato e dimensões (star schema)
- Consultas analíticas via SQL
- Geração de gráficos com Matplotlib
- Relatório consolidado em PDF com os dados

## Tecnologias Utilizadas
- Python 3.10
- PostgreSQL 10.5
- Docker / Docker Compose
- Pandas / Matplotlib
- Pytest

## Status do Projeto
Concluído com sucesso. Todas as etapas do pipeline estão funcionais e automatizadas. Relatórios e visualizações geradas corretamente.

## Autor(a)
Projeto desenvolvido por Juliana Ballin graduanda do curso de Sistemas de Informação pela UEA-EST.
