import scrapy

class CarrefourDebugSpider(scrapy.Spider):
    name = "carrefour_debug"
    
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
        'LOG_LEVEL': 'DEBUG'
    }
    
    def start_requests(self):
        yield scrapy.Request(
            url="https://www.carrefour.fr/promotions",
            callback=self.parse,
            headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'},
            meta={'dont_cache': True}
        )
    
    def parse(self, response):
        # Detailed logging to compare with shell
        self.logger.info("=== SPIDER RESPONSE DETAILS ===")
        self.logger.info(f"Status: {response.status}")
        self.logger.info(f"URL: {response.url}")
        self.logger.info(f"Headers: {dict(response.headers)}")
        self.logger.info(f"Content length: {len(response.text)}")
        self.logger.info(f"First 500 chars: {response.text[:500]}")
        
        # Save full response
        with open('spider_response.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        # Compare with what shell gives you
        self.logger.info("💾 Saved response to spider_response.html")
        self.logger.info("Compare this with what you get in scrapy shell!")
        
        yield {
            'status': response.status,
            'url': response.url,
            'content_length': len(response.text),
            'is_cloudflare': 'cloudflare' in response.text.lower()
        }
