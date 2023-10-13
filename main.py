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

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Referer': f'https://www.kabum.com.br/busca/{produto}?page_number=1&page_size=100&facet_filters=&sort=most_searched',  # Altere isso para a página de referência real
            'Cache-Control': 'max-age=0',
        }

        link = rf"https://www.kabum.com.br/busca/{produto}?page_number=1&page_size=100&facet_filters=&sort=most_searched"

    elif site == "Terabyte":

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Referer': f'https://www.terabyteshop.com.br/busca?str={produto}',  # Altere isso para a página de referência real
            'Cache-Control': 'max-age=0',
        }

    elif site == "Pichau":

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Referer': f'https://www.pichau.com.br/search?q={produto}',  # Altere isso para a página de referência real
            'Cache-Control': 'max-age=0',
        }

        link = rf"https://www.pichau.com.br/search?q={produto}"

    elif site == "Amazon":

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Referer': f'https://www.amazon.com.br/s?k={produto}',  # Altere isso para a página de referência real
            'Cache-Control': 'max-age=0',
        }

        link = rf"https://www.amazon.com.br/s?k={produto}"


    return link, headers


def Extrai_Dados(site, produto):

    #Deixa o nome do produto em maiusculo
    produto = produto.upper()

    #Gera o url do da pesquisa
    link, header = Gera_Url(site=site, produto=produto)

    scraper = WebScraper.WebScraper(url=link, nome_banco= r"C:\Users\Daniel\Documents\Meu\Outros\webscraper\DataBase.db", header=header)

    #Faz o fetch da pagina
    scraper.fetch_page()


    lista_produtos = scraper.extract_text_by_class(class_name='sc-d79c9c3f-0 nlmfp sc-93fa31de-16 bBOYrL nameCard', element="span")

    lista_preco = scraper.extract_text_by_class(class_name='sc-6889e656-2 bYcXfg priceCard', element="span")

    lista_links = scraper.extract_text_by_xpath(xpath = [f'//*[@id="listing"]/div[3]/div/div/div[2]/div[1]/main/div[{i}]/a' for i in range(1, 101)])

    #Arruma o link transformando em uma url completa
    lista_links = [f"https://www.{site}.com.br/{item}" for item in lista_links]


    #retira todos os erros em lista_preco
    lista_preco = [item.replace("R$", "").replace(".", "").replace(",", ".").replace(",", ".").replace('', '') for item in lista_preco]
    lista_preco = [re.sub(r'[^ -~]', '', item) for item in lista_preco]
    lista_preco = [float(item) for item in lista_preco]
    
    # Replicar os valores de site e data_atual para corresponder ao comprimento das outras listas
    lista_site = [site] * len(lista_produtos)
    lista_data_atual = [data_atual] * len(lista_produtos)

    # Combinacão em um único array de tuplas
    dados_combinados = list(zip(lista_produtos, lista_preco, lista_site,lista_links, lista_data_atual))

    # Remover tuplas onde o primeiro item não contém a variavel produto
    dados_combinados_filtrados = [tupla for tupla in dados_combinados if produto in tupla[0].upper()]


    scraper.inserir_tabela_produto(dados_combinados_filtrados)




if __name__ == "__main__":
    Extrai_Dados("Kabum", "Placa de Vídeo RTX 4070")
















