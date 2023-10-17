import pandas as pd
import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime, timedelta
from lxml import html
import json
import re

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


    def insert_table_product(self, data_list, site):

        product = data_list.get('title', None)
        value = data_list.get('price', None)
        site = site
        link = data_list.get('link', None)
        category = data_list.get('category', None)
        data_current = data_list.get('data', None)
        hour_current = data_list.get('hora', None)

        # Verifica se o valor é um número de ponto flutuante e converte se necessário
        if value is not None:
            try:
                value = re.sub(r'[^\d,.]', '', value)
                value = value.replace('.', '').replace(',', '.')
                value = float(value)
            except ValueError:
                value = None

        self.cursor.execute('''
            INSERT INTO Produtos (Produto, Valor, Site, Link, Categoria, Data, Hora)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (product, value, site, link, category, data_current, hour_current))

        self.connection.commit()