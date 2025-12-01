FROM python:3.10

#  pasta de trabalho dentro do container
WORKDIR /app

#diretorio na imagem usada pelo run
RUN mkdir -p /app/reports

# copia todos os arquivos para dentro do container
COPY . /app

# instala as dependências do requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
