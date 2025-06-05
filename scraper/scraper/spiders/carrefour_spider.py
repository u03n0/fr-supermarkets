import scrapy


class CarrefourSpider(scrapy.Spider):
    name = "carrefour"
    
    async def start(self):
        url = "https://www.carrefour.fr/promotions"
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        }
        yield scrapy.Request(url=url, headers=headers, callback=self.parse)

    def parse(self, response):
        for product in response.xpath("//div[contains(@class, 'product-list-card-plp-grid__infos')]"):
            yield {
                    "name": product.xpath(".//a/h3/text()").get()
                    }
