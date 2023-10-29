import json
import DataBase
from datetime import datetime, timedelta
import os
import shutil
import subprocess
import time
import logging
import Firebase_DataBase
from dotenv import load_dotenv




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
                
                db_sqlite.insert_table_product(dict_linha, site="Kabum")

def Post_Firebase():

    

    # Obtém a data e hora atuais
    agora = datetime.now()
    data_hora_formatada = agora.strftime(r"%Y-%m-%d %H:%M:%S")

    # Leitura do arquivo e processamento de cada JSON
    with open(rf'{os.getcwd()}\scrapy_kabum\scrapy_kabum\json\output.json', 'r', encoding="utf-8 sig") as json_file:

        data_list = json.load(json_file)

        db_firebase.enviar_requisicoes(data_list, n_threads=8)


if __name__ == "__main__":

    
    load_dotenv(override=True)
    api_key = os.getenv("WEBSCRAPING_FIREBASE_KEY")

    # Registra o tempo de início
    inicio = time.time()

    #Instancia as classes de db
    db_sqlite = DataBase.DataBase(bank_name=r"C:\Users\Daniel\Documents\Meu\Outros\webscraper\DataBase.db")
    db_firebase = Firebase_DataBase.FireBase_DataBase(api_key)

    #Roda a spider
    #run_scrapy_spider()

    #Trata e joga no sqlite
    Treats_json()

    #faz o post no firebase
    #Post_Firebase()



    # Registra o tempo de término
    fim = time.time()

    # Calcula o tempo total de execução
    tempo_total = fim - inicio

    print(f"Tempo de execução: {tempo_total} segundos")


