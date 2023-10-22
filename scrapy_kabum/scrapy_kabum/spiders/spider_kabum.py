import scrapy
from datetime import datetime
import json


class SpiderKabumSpider(scrapy.Spider):
    name = "spider_kabum"
    allowed_domains = ["www.kabum.com.br"]

    # Lista de categorias que você deseja rastrear
    categories = [
        "placa-de-video-vga",
        "processadores",
        "placas-mae",
        "memoria-ram",
        "fontes",
        "gabinetes",
        "monitores"
    ]

    def start_requests(self):
        for category in self.categories:
            url = f'https://www.kabum.com.br/hardware/{category}?page_number=1&page_size=100&facet_filters=&sort=most_searched'
            yield scrapy.Request(url=url, callback=self.parse, meta={'category': category, 'page': 1})

    def parse(self, response):
        # Obtem o número total de páginas
        total_page = int(response.xpath('//*[@id="listingPagination"]/ul/li[last()-1]/a/text()').get())

        # Limita a 10 páginas no máximo
        if total_page < 10:
            total_page = 10

        # Obtem categoria e página atual da meta
        category = response.meta.get('category')
        current_page = response.meta.get('page')

        # Verifica se 'category' foi passado corretamente
        if not category:
            self.log('Erro: category não foi passado corretamente.')

        #Pega os dados do json __NEXT_DATA__
        html = json.loads(response.xpath('//script[@id="__NEXT_DATA__"]/text( )').get())
        
        #Entra no json até a parte de dados
        props = html.get("props").get("pageProps").get("data")
        dados = json.loads(props).get("catalogServer").get("data")

        #Quando acha o dict de dados faz um for pegando as informações
        for dado in dados:
            name = dado.get("name")
            cod_produto = dado.get("code")

            #tratamento de alguns casos que não estão em oferta para retornar o preço
            offer = dado.get("offer")
            if offer == None:
                offer = dado.get("priceWithDiscount")


            yield{
                "title" : name,
                "price" : offer,
                "link": f"https://www.kabum.com.br/produto/{cod_produto}",
                "category":category,
                'data': str(datetime.today().date()),
                'hora': (datetime.now()).strftime("%H:%M:%S")
            }

        # products_cards = response.xpath('//div[@class="sc-93fa31de-7 gopyRO productCard"]')

        # for product_card in products_cards:
        #     # Crie um objeto Selector para o produto card
        #     product_selector = scrapy.Selector(text=product_card.get())

            


        #     #Seleciona o que precisa selecionar
        #     name = product_selector.xpath(".//h2/span/text()").get()
        #     value = product_selector.xpath('.//a/div/div[1]/span[2]/text()').get()
        #     link = product_selector.xpath('.//a/@href').get()
            
        #     # Armazenar as informações em um dicionário
        #     product_info = {
        #         'title': name,
        #         'price': value,
        #         'link': link,
        #         "category":category,
        #         'data': str(datetime.today().date()),
        #         'hora': (datetime.now()).strftime("%H:%M:%S")
        #     }

        #     yield product_info
        
        # Obter o número da página atual da URL
        current_page = int(response.url.split('page_number=')[1].split('&')[0])

        # Verifica se estamos na página 9 ou menos
        if current_page < total_page:
            # Construir a URL da próxima página para a categoria atual
            next_page = f'https://www.kabum.com.br/hardware/{category}?page_number={current_page + 1}&page_size=100&facet_filters=&sort=most_searched'

            # Criar uma nova solicitação para a próxima página
            yield scrapy.Request(url=next_page, callback=self.parse, meta={'category': category, 'page': current_page + 1})


