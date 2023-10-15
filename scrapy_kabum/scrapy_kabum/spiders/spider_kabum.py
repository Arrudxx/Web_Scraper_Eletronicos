import scrapy
from datetime import datetime



class SpiderKabumSpider(scrapy.Spider):
    name = "spider_kabum"
    allowed_domains = ["www.kabum.com.br"]
    start_urls = ["https://www.kabum.com.br/hardware/placa-de-video-vga?page_number=1&page_size=100&facet_filters=&sort=most_searched", ]

    def parse(self, response):

        products_cards = response.xpath('//div[@class="sc-93fa31de-7 gopyRO productCard"]')

        for product_card in products_cards:
            # Crie um objeto Selector para o produto card
            product_selector = scrapy.Selector(text=product_card.get())

            #Seleciona o que precisa selecionar
            name = product_selector.xpath(".//h2/span/text()").get()
            value = product_selector.xpath('.//a/div/div[1]/span[2]/text()').get()
            link = product_selector.xpath('.//a/@href').get()
            
            # Armazenar as informações em um dicionário
            product_info = {
                'title': name,
                'price': value,
                'link': link,
                'data': str(datetime.today().date()),
                'hora': (datetime.now()).strftime("%H:%M:%S")
            }

            yield product_info
        
        #Obtem numero total de paginas
        total_page = int(response.xpath('//*[@id="listingPagination"]/ul/li[last()-1]/a/text()').get())

        # Obter o número da página atual da URL
        current_page = int(response.url.split('page_number=')[1].split('&')[0])

        # Verificar se estamos na página 9 ou menos
        if current_page <= total_page:
            # Construir a URL da próxima página
            next_page = f'https://www.kabum.com.br/hardware/placa-de-video-vga?page_number={current_page + 1}&page_size=100&facet_filters=&sort=most_searched'

            # Criar uma nova solicitação para a próxima página
            yield scrapy.Request(url=next_page, callback=self.parse)


