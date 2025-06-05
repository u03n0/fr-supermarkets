import scrapy

class FranprixSpider(scrapy.Spider):
    name = "franprix_improved"
    
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 1,
        'RANDOMIZE_DOWNLOAD_DELAY': 0.5,
    }
    
    def start_requests(self):  # Fixed: should be start_requests, not async start
        url = "https://www.franprix.fr/courses/promotions"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        }
        yield scrapy.Request(url=url, headers=headers, callback=self.parse)
    
    def parse(self, response):
        # Extract current page number for logging
        current_page = self.get_current_page(response.url)
        self.logger.info(f"📄 Scraping page {current_page}: {response.url}")
        
        # Extract products (your existing code)
        products_found = 0
        for product in response.xpath("//div[contains(@class, 'product-item-content-resume')]"):
            try:
                brand_unit = product.xpath(".//div[contains(@class, 'product-item-more')]/span/text()").getall()
                price = "".join(product.xpath(".//div[contains(@class, 'product-item-price')]/span/text()").getall())
                
                # Handle unit_price safely
                unit_price_text = product.xpath(".//span[contains(@class, 'product-item-priceperkilo')]/text()").get()
                unit_price, unit_label = None, None
                
                if unit_price_text and "/" in unit_price_text:
                    unit_price, unit_label = unit_price_text.split("/", 1)
                
                product_data = {
                    "name": product.xpath(".//span[contains(@class, 'product-item-name')]/text()").get(),
                    "brand": brand_unit[0] if brand_unit else None,
                    "price": price,
                    "size": brand_unit[1] if len(brand_unit) > 1 else None,
                    "unit_price": unit_price,
                    "unit_label": unit_label,
                    "promo": product.xpath(".//div[contains(@class, 'product-item__promo__regular')]/span/text()").get(),
                    "page": current_page,
                    "source_url": response.url
                }
                
                # Only yield if we have a name
                if product_data["name"]:
                    products_found += 1
                    yield product_data
                    
            except Exception as e:
                self.logger.warning(f"Error extracting product: {e}")
                continue
        
        self.logger.info(f"✅ Found {products_found} products on page {current_page}")
        
        # Handle pagination - based on your HTML structure
        next_page_url = self.find_next_page(response)
        
        if next_page_url:
            self.logger.info(f"🔄 Following to next page: {next_page_url}")
            yield scrapy.Request(
                url=next_page_url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
                },
                callback=self.parse,
                meta={'dont_cache': True}
            )
        else:
            self.logger.info(f"🏁 No more pages found after page {current_page}")
    
    def get_current_page(self, url):
        """Extract current page number from URL"""
        import re
        if 'page=' in url:
            match = re.search(r'page=(\d+)', url)
            return int(match.group(1)) if match else 1
        return 1
    
    def find_next_page(self, response):
        """Find next page URL from pagination"""
        
        # Strategy 1: Look for active page and find the next numbered page
        # Based on your HTML: <a class="flex items-center justify-center w-7 h-7 rounded text-sm tex cursor-pointer p-1.5 border border-solid border-transparent" href="/courses/promotions?page=2">
        
        current_page = self.get_current_page(response.url)
        next_page = current_page + 1
        
        # Look for next page link directly
        next_page_xpath = f"//a[@href and contains(@href, 'page={next_page}')]/@href"
        next_page_url = response.xpath(next_page_xpath).get()
        
        if next_page_url:
            return response.urljoin(next_page_url)
