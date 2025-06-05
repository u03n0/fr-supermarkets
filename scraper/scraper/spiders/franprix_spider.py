import scrapy

class FranprixSpider(scrapy.Spider):
    name = "franprix"
    async def start(self):
        url = "https://www.franprix.fr/courses/promotions"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        }
        yield scrapy.Request(url=url, headers=headers, callback=self.parse)

    def parse(self, response):
        for product in response.xpath("//div[contains(@class, 'product-item-content-resume')]"):
            brand_unit = product.xpath(".//div[contains(@class, 'product-item-more')]/span/text()").getall()
            price = "".join(product.xpath(".//div[contains(@class, 'product-item-price')]/span/text()").getall())
            unit_price, unit_lable = product.xpath(".//span[contains(@class, 'product-item-priceperkilo')]/text()").get().split("/")

            yield {
                    "name": product.xpath(".//span[contains(@class, 'product-item-name')]/text()").get(),
                    "brand": brand_unit[0],
                    "price": price,
                    "size": brand_unit[1],
                    "unit_price": unit_price,
                    "unit_label": unit_label,
                    "promo": product.xpath(".//div[contains(@class, 'product-item__promo__regular')]/span/text()").get()
                    }
