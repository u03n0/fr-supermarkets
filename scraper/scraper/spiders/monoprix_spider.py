import scrapy
import json

class MonoprixAPISimpleSpider(scrapy.Spider):
    name = "monoprix_api_simple"
    base_url = "https://courses.monoprix.fr/api/v6/products"
    
    def start_requests(self):
        yield scrapy.Request(
            url=self.base_url,
            callback=self.parse,
            headers={
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': 'https://courses.monoprix.fr/',
            }
        )
    
    def parse(self, response):
        try:
            data = json.loads(response.text)
            entities = data.get('entities', {}).get('product', {})
            
            self.logger.info(f"Found {len(entities)} products on this page")
            
            # Parse each product - based on actual JSON structure
            for product_id, product in entities.items():
                # Extract price info
                price_info = product.get('price', {})
                current_price = None
                
                # Get current price from price.current.amount
                price_current = price_info.get('current', {})
                if isinstance(price_current, dict):
                    current_price = price_current.get('amount')
                
                # Extract unit info from price.unit
                unit_info = price_info.get('unit', {})
                unit_label = unit_info.get('label') if isinstance(unit_info, dict) else None
                unit_amount = unit_info.get('current', {}).get('amount') if isinstance(unit_info, dict) else None
                
                # Extract size from guaranteedProductLife
                size = None
                guaranteed_product_life = product.get('guaranteedProductLife', {})
                if isinstance(guaranteed_product_life, dict):
                    size = guaranteed_product_life.get('quantity')
                
                # Extract brand
                brand = product.get('brand')
                
                # Extract name
                name = product.get('name')

                size_info = product.get('size', {})
                current_size = None
                size = size_info.get("value")
                
                promo_info = product.get('offer', {})
                promo = promo_info.get('description') if isinstance(promo_info, dict) else None
                
                yield {
                    'name': name,
                    'brand': brand,
                    'price': current_price,
                    'size': size,
                    'unit_price': unit_amount,
                    'unit_label': unit_label,  # e.g., "€/kg price per litre"
                    'promo': promo 
                }
            
            # Check for next page
            next_page_token = data.get('result', {}).get('nextPageToken')
            if next_page_token:
                next_url = f"{self.base_url}?pageToken={next_page_token}"
                yield scrapy.Request(
                    url=next_url,
                    callback=self.parse,
                    headers=self.headers
                )
            else:
                self.logger.info("Finished scraping all pages!")
                
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse JSON: {e}")
        except Exception as e:
            self.logger.error(f"Error: {e}")
    
    @property
    def headers(self):
        return {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://courses.monoprix.fr/',
        }
