import json
import pandas as pd
import Class.DataBase
from datetime import datetime, timedelta
import os
import shutil
import subprocess
import time
import logging
import Class.Firebase_DataBase
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

def Create_Dim_Table(df, caminho, nome_colunas= [], tema_tabela = ""):

    for nome_coluna in nome_colunas:

        #df[nome_coluna].apply(lambda x: x.title())

        coluna_normalizada = df.groupby([nome_coluna]).size().to_frame(name="count").reset_index()
        coluna_normalizada.drop("count", axis=1, inplace=True)
        coluna_normalizada.insert(0,f"id_{nome_coluna}",range(1,1 + len(coluna_normalizada)))

        #Utiliza o index como id dinamico
        coluna_normalizada_csv = coluna_normalizada.set_index(f"id_{nome_coluna}")

        #Gera as dimensões no formato csv
        coluna_normalizada[f"id_{nome_coluna}"] = coluna_normalizada[f"id_{nome_coluna}"].fillna(0)
        coluna_normalizada[f"id_{nome_coluna}"] = coluna_normalizada[f"id_{nome_coluna}"].astype(int)
        coluna_normalizada_csv.to_csv(rf"{caminho}\DIM_{nome_coluna}{tema_tabela}.csv")

        df = pd.merge(df, coluna_normalizada, how="left", on=[nome_coluna], suffixes=('','_remover'))

        df.drop([i for i in df.columns if 'remover' in i], axis=1, inplace=True)

        df.drop(nome_coluna, axis=1, inplace=True)

        df[f"id_{nome_coluna}"].fillna(0, inplace=True)

        df[f"id_{nome_coluna}"] = df[f"id_{nome_coluna}"].astype(int)

        df.index.names = ["id_fin"]

    df.to_csv(rf"{caminho}\FATO{tema_tabela}.csv", index=False)

def Create_Etl() -> None:

    #Cria os dataframes
    df_archives = pd.read_csv(r"Archive\Archives.csv", encoding="utf-8-sig")
    df = pd.read_csv(r"Resultado.csv", encoding="utf-8-sig")

    # Função para verificar a presença de names na string
    def check_string(names, my_string):
        for name in names:
            if name in my_string:
                return name
        return None

    # Aplicar a função a cada linha dos DataFrames usando a função apply e axis=1
    df['Marca'] = df['Produto'].apply(lambda my_string: check_string(df_archives["Marcas"], my_string))

    df["Valor"] = df["Valor"].apply(lambda x: str(x).replace(".", ","))

    #Cria Tabelas Dim
    Create_Dim_Table(df, caminho=r"Archive\Tables_BI", nome_colunas=["Produto", "Site", "Link", "Categoria", "Marca"])






if __name__ == "__main__":

    # load_dotenv(override=True)
    # api_key = os.getenv("WEBSCRAPING_FIREBASE_KEY")

    # # Registra o tempo de início
    # inicio = time.time()

    # #Instancia as classes de db
    # db_sqlite = Class.DataBase.DataBase(bank_name=r"C:\Users\Daniel\Documents\Meu\Outros\webscraper\DataBase.db")
    # #db_firebase = Class.Firebase_DataBase.FireBase_DataBase(api_key)

    # #Roda a spider
    # run_scrapy_spider()

    # #Trata e joga no sqlite
    # Treats_json()

    # #faz o post no firebase
    # #Post_Firebase()

    # #Exporta a tabela para um csv
    # db_sqlite.export_table_to_csv("Produtos", "Resultado.csv")

    # # Registra o tempo de término
    # fim = time.time()

    # # Calcula o tempo total de execução
    # tempo_total = fim - inicio

    Create_Etl()

    # print(f"Tempo de execução: {tempo_total} segundos")


