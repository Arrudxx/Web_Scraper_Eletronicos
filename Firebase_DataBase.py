import pandas as pd
import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime, timedelta
from lxml import html
import concurrent.futures
import json
import re
from datetime import datetime
from tqdm import tqdm

class FireBase_DataBase:
    def __init__(self, api_key) -> None:

        self.api_key = api_key
        pass


    #def request_prdutos_post(self, dates):

        # num_itens = len(dates)
        # # Inicializa a barra de carregamento
        # with tqdm(total=num_itens) as barra_progresso:
        #     for date in dates:

        #         response = requests.post(f'{self.api_key}/Produtos/.json', data=json.dumps(date))

        #         if response.status_code != 200:
        #             # Salva os detalhes da requisição no arquivo de log
        #             with open('logfile.txt', 'a') as log_file:
        #                 log_file.write(f'{datetime.datetime.now()} - Status Code: {response.status_code}\n')
        #                 log_file.write(f'Request Data: {json.dumps(date)}\n')
        #                 log_file.write(f'Response Content: {response.text}\n')
        #                 log_file.write('\n')  # Adiciona uma linha em branco para separar entradas no arquivo de log

        #         # Atualiza a barra de carregamento
        #         barra_progresso.update(1)

            #return response, response.text

    def make_request(self, date):
        response = requests.post(f'{self.api_key}/Produtos/.json', data=json.dumps(date))
        return response

    def handle_response(self, response, date, n_threads):
        if response.status_code != 200:
            # Salva os detalhes da requisição no arquivo de log
            with open('logfile.txt', 'a') as log_file:
                log_file.write(f'{datetime.datetime.now()} - Status Code: {response.status_code}\n')
                log_file.write(f'Request Data: {json.dumps(date)}\n')
                log_file.write(f'Response Content: {response.text}\n')
                log_file.write('\n')  # Adiciona uma linha em branco para separar entradas no arquivo de log

        # Atualiza a barra de carregamento
        self.progress_bar.update(1)

    def enviar_requisicoes(self, dates, n_threads):
        # Inicializa a barra de carregamento
        self.progress_bar = tqdm(total=len(dates), desc="Enviando Requisições", unit="req")

        # Número máximo de threads no pool (ajuste conforme necessário)
        max_threads = n_threads

        # Cria um ThreadPoolExecutor com o número máximo de threads
        with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
            # Faz as requisições em paralelo
            futures = [executor.submit(self.make_request, date) for date in dates]

            # Processa as respostas à medida que elas ficam disponíveis
            for future, date in zip(concurrent.futures.as_completed(futures), dates):
                response = future.result()
                self.handle_response(response, date, n_threads)

        # Fecha a barra de carregamento ao finalizar
        self.progress_bar.close()

        

