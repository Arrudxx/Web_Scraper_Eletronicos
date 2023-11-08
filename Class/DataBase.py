import pandas as pd
import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime, timedelta
from lxml import html
import json
import re
import csv

class DataBase:
    def __init__(self,bank_name = "database.db") -> None:
        self.bank_name = bank_name
        self.connection = None
        self.cursor = None
        self.connect()
        self.crate_table_product()


    def crate_table_product(self):
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Produtos (
                    id INTEGER PRIMARY KEY,
                    Produto TEXT,
                    Valor FLOAT,
                    Site TEXT,
                    Link TEXT,
                    Categoria TEXT,
                    Data TEXT,
                    Hora TEXT
                )
            ''')


    def connect(self) -> None:
        self.connection = sqlite3.connect(self.bank_name)
        self.cursor = self.connection.cursor()



    def insert_table_product(self, data_list, site) -> None:
        
        product = data_list.get('title', None)
        value = data_list.get('price', None)
        site = site
        link = data_list.get('link', None)
        category = data_list.get('category', None)
        data_current = data_list.get('data', None)
        hour_current = data_list.get('hora', None)

        # Verifica se o produto já existe no banco
        self.cursor.execute('SELECT * FROM Produtos WHERE Produto = ?', (product,))
        existing_row = self.cursor.fetchone()

        # Verifica se há algum resultado
        if existing_row:
            
            # Se o produto já existe, verifica se o valor é diferente
            if existing_row[2] != value:

                # Adiciona este produto com um novo valor
                self.cursor.execute('''
                INSERT INTO Produtos (Produto, Valor, Site, Link, Categoria, Data, Hora)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (product, value, site, link, category, data_current, hour_current))
                self.connection.commit()
                #print(f"Novo preço encontrado, nova linha gerada.")

            else:
                pass
                #print(f"Produto {product} já existe no banco, nenhum update necessário.")
        else:
            # Se o produto não existe, insere uma nova linha
            self.cursor.execute('''
                INSERT INTO Produtos (Produto, Valor, Site, Link, Categoria, Data, Hora)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (product, value, site, link, category, data_current, hour_current))
            self.connection.commit()
            #print(f"Novo produto {product} adicionado ao banco.")

    def export_table_to_csv(self, table_name, csv_file_name) -> str:

        # Selecionar todos os dados da tabela
        self.cursor.execute(f"SELECT * FROM {table_name}")
        table_data = self.cursor.fetchall()

        # Obter os nomes das colunas
        self.cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [column[1] for column in self.cursor.fetchall()]

        # Fechar a conexão com o banco de dados
        self.connection.close()

        # Escrever os dados no arquivo CSV
        with open(csv_file_name, 'w', newline='', encoding='utf-8-sig') as csv_file:
            csv_writer = csv.writer(csv_file)

            # Escrever os nomes das colunas como cabeçalho
            csv_writer.writerow(columns)

            # Escrever os dados
            csv_writer.writerows(table_data)

        return print(f'Dados da tabela {table_name} exportados para {csv_file_name}.')