![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-%23FE4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)


# French Supermarket Price Comparison Tool

A comprehensive price comparison tool for French supermarkets that helps you find the best deals on groceries and optimize your shopping based on recipes.

## Features

- **Multi-Supermarket Data Collection**: Scrape product data from major French supermarkets
- **Price Comparison**: Compare prices across different stores for similar products
- **Recipe Integration**: Parse recipes and suggest optimal purchasing decisions
- **REST API**: FastAPI backend for data access and manipulation
- **Interactive Dashboard**: Streamlit frontend for visual price comparison
- **Recipe Parsing**: Support for manual entry, copy-paste, or file upload of recipes
- **Shopping Optimization**: Get recommendations on which products to buy from which stores

## Architecture

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐
│   Web Scrapers  │───▶│   FastAPI    │───▶│   Streamlit     │
│   (Data Collection)   │   (API Layer)│    │   (Frontend)    │
└─────────────────┘    └──────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────┐
                       │   Database   │
                       │ (Product Data)│
                       └──────────────┘
```

## Installation

### Prerequisites

- Python 3.8+
- pip or conda package manager

### Setup

1. **Clone the repository**
   ```bash
   git clone git@github.com:u03n0/fr-supermarkets.git
   cd fr-supermarkets
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials and API keys
   ```

4. **Initialize the database**
   ```bash
   python scripts/init_db.py
   ```

## Usage

### Starting the Services

1. **Start the FastAPI backend**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

2. **Launch the Streamlit dashboard**
   ```bash
   streamlit run streamlit_app.py --server.port 8501
   ```

3. **Access the applications**
   - API Documentation: http://localhost:8000/docs
   - Streamlit Dashboard: http://localhost:8501

### Running the Scrapers

⚠️ **Important Legal Notice**: Before using the scrapers, please read the [Legal Disclaimer](#legal-disclaimer) section below.

```bash
# Scrape data from all configured supermarkets
python scrapers/run_all_scrapers.py

# Scrape data from a specific supermarket
python scrapers/carrefour_scraper.py
python scrapers/leclerc_scraper.py
python scrapers/auchan_scraper.py
```

### Using the Recipe Feature

1. **Manual Recipe Entry**: Use the Streamlit interface to manually enter ingredients
2. **Copy-Paste Recipe**: Paste a recipe directly into the text area
3. **File Upload**: Upload a `.txt` file containing your recipe
4. **Get Recommendations**: The system will parse ingredients and suggest optimal purchasing decisions

## API Endpoints

### Products
- `GET /api/products` - List all products
- `GET /api/products/{id}` - Get specific product details
- `GET /api/products/search` - Search products by name/category

### Price Comparison
- `GET /api/compare/{product_name}` - Compare prices across stores
- `GET /api/stores/{store_id}/products` - Get products from specific store

### Recipe Processing
- `POST /api/recipes/parse` - Parse recipe and get ingredient list
- `POST /api/recipes/optimize` - Get optimal shopping recommendations

## Configuration

### Scraper Configuration

Edit `config/scrapers.yaml` to configure scraping parameters:

```yaml
scrapers:
  carrefour:
    base_url: "https://www.carrefour.fr"
    rate_limit: 1  # seconds between requests
    user_agent: "Mozilla/5.0..."
    
  leclerc:
    base_url: "https://www.leclerc.fr"
    rate_limit: 1
    user_agent: "Mozilla/5.0..."
```

### Database Configuration

Configure your database connection in `.env`:

```env
DATABASE_URL=sqlite:///./supermarket_data.db
# or for PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost/dbname
```

## Data Sources

This project uses open-source product information for demonstration purposes. The scrapers are provided as examples and should be used responsibly according to each website's terms of service.

### Sample Data

The repository includes sample product data from:
- Open Food Facts API
- Government price monitoring databases
- Anonymized product catalogs

## Legal Disclaimer

⚠️ **IMPORTANT**: This project includes web scraping functionality for educational and demonstration purposes only.

### Your Responsibilities

1. **Terms of Service Compliance**: You are solely responsible for ensuring your use of the scrapers complies with each website's Terms of Service and robots.txt file.

2. **Rate Limiting**: Implement appropriate delays between requests to avoid overwhelming target servers.

3. **Legal Compliance**: Ensure your scraping activities comply with local laws and regulations, including GDPR and other data protection laws.

4. **Ethical Use**: Use the scrapers responsibly and consider the impact on the target websites.

### Recommendations

- Always check and respect `robots.txt` files
- Implement proper error handling and retry logic
- Use reasonable request intervals (minimum 1 second between requests)
- Monitor for changes in website structure that might break scrapers
- Consider using official APIs when available

**The maintainers of this project are not responsible for any misuse of the scraping functionality or any legal consequences arising from such use.**

## Development

### Project Structure

```
├── app/
│   ├── main.py              # FastAPI application
│   ├── models/              # Database models
│   ├── api/                 # API routes
│   └── services/            # Business logic
├── scrapers/
│   ├── base_scraper.py      # Base scraper class
│   ├── carrefour_scraper.py # Carrefour scraper
│   └── leclerc_scraper.py   # Leclerc scraper
├── streamlit_app.py         # Streamlit dashboard
├── data/
│   └── sample_products.json # Sample product data
├── config/
│   └── scrapers.yaml        # Scraper configuration
└── requirements.txt
```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Adding New Scrapers

1. Inherit from `BaseScaper` in `scrapers/base_scraper.py`
2. Implement required methods (`scrape_products`, `parse_product`)
3. Add configuration to `config/scrapers.yaml`
4. Update documentation

## Testing

```bash
# Run all tests
pytest

# Run specific test categories
pytest tests/test_scrapers.py
pytest tests/test_api.py
pytest tests/test_recipe_parser.py
```

## Deployment

### Docker Deployment

```bash
# Build the container
docker build -t supermarket-comparison .

# Run with docker-compose
docker-compose up -d
```

### Environment Variables for Production

```env
DATABASE_URL=postgresql://user:password@localhost/dbname
API_HOST=0.0.0.0
API_PORT=8000
STREAMLIT_PORT=8501
LOG_LEVEL=INFO
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/french-supermarket-comparison/issues) page
2. Create a new issue with detailed information about your problem
3. For general questions, use the [Discussions](https://github.com/yourusername/french-supermarket-comparison/discussions) tab

## Acknowledgments

- Open Food Facts for providing open product data
- The Python community for excellent scraping and web framework libraries
- Contributors who help improve this project

---

**Disclaimer**: This tool is for personal use and educational purposes. Always respect website terms of service and applicable laws when scraping data.
