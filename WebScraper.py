import pandas as pd
import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime, timedelta
from lxml import html

class WebScraper:
    def __init__(self, url, nome_banco = "database.db", header = "") -> None:
        self.url = url
        self.header = header
        self.html_content = None
        self.soup = None
        self.array_text = []
        self.nome_banco = nome_banco
        self.conexao = None
        self.cursor = None
        self.conectar()
        self.criar_tabela_produtos()

    def criar_tabela_produtos(self):
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Produtos (
                    id INTEGER PRIMARY KEY,
                    Produto TEXT,
                    Valor FLOAT,
                    Site TEXT,
                    Link TEXT,
                    Data TEXT,
                    Hora TEXT
                )
            ''')

    def conectar(self) -> None:
        self.conexao = sqlite3.connect(self.nome_banco)
        self.cursor = self.conexao.cursor()


    def inserir_tabela_produto(self, dados_produtos):
        
        hora_atual = (datetime.now()).strftime("%H:%M:%S")

        for produto, valor, site, link, data_atual in dados_produtos:
            self.cursor.execute('''
                INSERT INTO Produtos (Produto, Valor, Site, Link, Data, Hora)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (produto, valor, site, link, data_atual, hora_atual))

        self.conexao.commit()

    def fetch_page(self):

        # Faça a solicitação HTTP
        req = requests.get(url=self.url, headers=self.header)

        # Verifique se a solicitação foi bem-sucedida
        if req.status_code == 200:
            self.html_content = req.text
            self.soup = BeautifulSoup(self.html_content, 'html.parser')
            #print(self.soup)
        else:
            print(f"Falha ao obter a página. Código de status: {req.status_code}")

    def extract_text_by_class(self,class_name = None, element=None, xpath = None) -> list:
        
        if self.soup is not None:

            self.array_text = []


            if xpath == None:
                
                # Encontrar todos os spans com a classe específica
                spans_target = self.soup.find_all(element, class_=class_name)

                # Iterar sobre os spans e extrair o texto de cada um
                for span_target in spans_target:
                    span_text = span_target.text
                    #print(f"Conteúdo do span: {span_text}")

                    self.array_text.append(span_text)

            
            return self.array_text

    def extract_text_by_xpath(self,class_name = None, element=None, xpath = None) -> list:
    
        if self.soup is not None:

            self.array_text = []


            # Convertendo o objeto BeautifulSoup para um objeto lxml
            root = html.fromstring(str(self.soup))

            # Usando XPath para encontrar os elementos desejados
            if type(xpath) == list:
                for xpath  in xpath:
                    link = root.xpath(xpath)
                    for link in link:
                        #print(link.get('href'))
                        self.array_text.append(link.get('href'))
            
            return self.array_text



        else:
            print("A página ainda não foi carregada. Execute fetch_page() primeiro.")

    
