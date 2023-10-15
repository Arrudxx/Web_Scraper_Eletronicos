import json
import DataBase
from datetime import datetime, timedelta
import os
import shutil
import subprocess

#A FAZER
    #! Remover kabum do metodo database
    #! adicionar site ao dicionario antes
    #! Arruma problemas com este dicionario
    

def run_scrapy_spider() -> None:
    project_dir = "scrapy_kabum\scrapy_kabum"  # Substitua pelo caminho real do seu projeto
    spider_name = "spider_kabum"

    # Mude o diretório de trabalho para o diretório do projeto Scrapy
    os.chdir(project_dir)

    command = "scrapy crawl spider_kabum -o output.json"
    subprocess.run(command, shell=True)

    #Se existir o arquivo apaga ele
    if os.path.exists(rf'{os.getcwd()}\json\output.json'):
        os.remove(rf'{os.getcwd()}\json\output.json')


    #Move o arquivo para a pasta Json
    print(os.getcwd())
    if os.path.exists(rf'{os.getcwd()}\output.json'):
        shutil.move(rf'{os.getcwd()}\output.json', rf'{os.getcwd()}\json\output.json')

def Treats_json():

    # try:
    with open(rf'{os.getcwd()}\scrapy_kabum\scrapy_kabum\json\output.json', 'r', encoding='utf-8') as json_file:

        # Lê todas as linhas do arquivo
        linhas = json_file.readlines()

        # Se a primeira linha contiver apenas '[', remova-a
        if linhas and linhas[0].strip() == '[':
            linhas = linhas[1:]
        
        # Itera sobre cada linha do arquivo
        for linha in linhas:

            # Remove o caractere de nova linha (\n) no final de cada linha
            linha = linha.rstrip(',\n')
            linha = linha.rstrip('')
            # Carrega a linha como um objeto JSON (dicionário)
            dict_linha = json.loads(linha)
            
            my_db.insert_table_product(dict_linha)



if __name__ == "__main__":
    my_db = DataBase.DataBase(bank_name=r"C:\Users\Daniel\Documents\Meu\Outros\webscraper\DataBase.db")

    #run_scrapy_spider()
    
    for dicionario in Treats_json():
        # Chame a função insert_table_product para cada dicionário
        my_db.insert_table_product(**dicionario)

        

        # print(data_generator)

    # except Exception as e:
    #     print(f"Erro ao ler e inserir no banco de dados: {e}")

#DataBase = DataBase.DataBase(name_bank="database.db")

