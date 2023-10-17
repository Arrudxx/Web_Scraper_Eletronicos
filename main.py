import json
import DataBase
from datetime import datetime, timedelta
import os
import shutil
import subprocess
import time
import logging

# Configuração do nível de log para CRITICAL
logging.getLogger('scrapy').setLevel(logging.CRITICAL)

def run_scrapy_spider() -> None:
    run_current = os.getcwd()
    project_dir = "scrapy_kabum\scrapy_kabum"
    #spider_name = "spider_kabum"

    # Mude o diretório de trabalho para o diretório do projeto Scrapy
    os.chdir(project_dir)

    command = "scrapy crawl spider_kabum -o output.json"
    subprocess.run(command, shell=True)

    #Se existir o arquivo apaga ele
    if os.path.exists(rf'{os.getcwd()}\json\output.json'):
        os.remove(rf'{os.getcwd()}\json\output.json')


    #Move o arquivo para a pasta Json
    #print(os.getcwd())
    if os.path.exists(rf'{os.getcwd()}\output.json'):
        shutil.move(rf'{os.getcwd()}\output.json', rf'{os.getcwd()}\json\output.json')

    #Retorna para o diretorio inicial
    os.chdir(run_current)

def Treats_json():

    # try:
    with open(rf'{os.getcwd()}\scrapy_kabum\scrapy_kabum\json\output.json', 'r', encoding='utf-8') as json_file:

        # Lê todas as linhas do arquivo
        linhas = json_file.readlines()

        
        # Itera sobre cada linha do arquivo
        for linha in linhas:
            
            # Verificar se a linha contém '[' ou ']'
            if '[' not in linha and ']' not in linha:

                # Remove o caractere de nova linha (\n) no final de cada linha
                linha = linha.rstrip(',\n')
                # Carrega a linha como um objeto JSON (dicionário)
                dict_linha = json.loads(linha)
                
                my_db.insert_table_product(dict_linha, site="Kabum")



if __name__ == "__main__":

    # Registra o tempo de início
    inicio = time.time()

    my_db = DataBase.DataBase(bank_name=r"C:\Users\Daniel\Documents\Meu\Outros\webscraper\DataBase.db")

    run_scrapy_spider()

    Treats_json()

    # Registra o tempo de término
    fim = time.time()

    # Calcula o tempo total de execução
    tempo_total = fim - inicio

    print(f"Tempo de execução: {tempo_total} segundos")


