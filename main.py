import pandas as pd
import selenium
import WebScraper
from datetime import datetime
import sqlite3
import re





data_atual = str(datetime.today().date())

def Gera_Url(site, produto) -> str:
    
    #Trata caso se vim com mais de 1 espaco
    produto = produto.split()
    produto = ' '.join(produto)

    #Substitui o espaco por -
    produto = produto.replace(" ", "-")

    if site == "Kabum":

        link = rf"https://www.kabum.com.br/busca/{produto}?page_number=1&page_size=100&facet_filters=&sort=most_searched"

        return link


def Extrai_Dados(site, produto):

    #Deixa o nome do produto em maiusculo
    produto = produto.upper()

    #Gera o url do da pesquisa
    link = Gera_Url(site=site, produto=produto)

    scraper = WebScraper.WebScraper(url=link, nome_banco= r"C:\Users\Daniel\Documents\Meu\Outros\webscraper\DataBase.db")

    #Faz o fetch da pagina
    scraper.fetch_page()

    lista_produtos = scraper.extract_span_text_by_class(class_name='sc-d79c9c3f-0 nlmfp sc-93fa31de-16 bBOYrL nameCard')

    lista_preco = scraper.extract_span_text_by_class(class_name='sc-6889e656-2 bYcXfg priceCard')

    #retira todos os erros em lista_preco
    lista_preco = [item.replace("R$", "").replace(".", "").replace(",", ".").replace(",", ".").replace('', '') for item in lista_preco]
    lista_preco = [re.sub(r'[^ -~]', '', item) for item in lista_preco]
    lista_preco = [float(item) for item in lista_preco]
    
    # Replicar os valores de site e data_atual para corresponder ao comprimento das outras listas
    lista_site = [site] * len(lista_produtos)
    lista_data_atual = [data_atual] * len(lista_produtos)

    # Combinacão em um único array de tuplas
    dados_combinados = list(zip(lista_produtos, lista_preco, lista_site, lista_data_atual))

    # Remover tuplas onde o primeiro item não contém a variavel produto
    dados_combinados_filtrados = [tupla for tupla in dados_combinados if produto in tupla[0].upper()]


    scraper.inserir_tabela_produto(dados_combinados_filtrados)





Extrai_Dados("Kabum", "Placa de Vídeo RTX 4060")














