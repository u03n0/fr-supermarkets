from fastapi import FastAPI
from backend.routers import products
from backend.database import get_db_connection

app = FastAPI(title="Product API", description="API for scraped product data")
app.include_router(products.router)

@app.get("/")
async def root():
    return {"message": "Product API is working!"}



#@app.get("/brands")
#async def get_brands():
    #"""Get all unique brands"""
    #try:
        #with get_db_connection() as conn:
         #   cursor = conn.cursor(cursor_factory=RealDictCursor)
          #  cursor.execute("""
           #     SELECT brand, COUNT(*) as product_count 
            #    FROM products 
             #   WHERE brand IS NOT NULL 
              #  GROUP BY brand 
               # ORDER BY brand
            #""")
            #brands = cursor.fetchall()
            #return {"brands": [dict(brand) for brand in brands]}
   # except Exception as e:
    #    raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
