from typing import Any, Iterable
import scrapy
import json
import http.cookiejar

from scrapy.http import Request, Response

class ScrapyPichau(scrapy.Spider):
    name = "pichau"
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_START_DELAY": 60,
        "DOWNLOAD_DELAY": 2.5,
        "COOKIES_ENABLED": False,
        'Referer': 'https://www.pichau.com.br/',  # Altere para a página de referência real
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1        
    }


    def start_requests(self) -> Iterable[Request]:
        
        #cookies = {'cookie_name': 'cookie_value'}
        yield scrapy.Request(r"https://www.pichau.com.br",)
        
        #return super().start_requests()
    
    def parse(self, response: Response, **kwargs: Any) -> Any:
        
        props=json.loads(response.xpath('//script[@id="__NEXT_DATA__"]//text()').get())
        houses = props.get("props").get("pageProps")
        #print(houses)

        #return super().parse(response, **kwargs)