from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
#from backend.database import get_db_connection
from database import get_db_connection

router = APIRouter(prefix="/products", tags=["products"])
# ... rest of your routes




@router.get("/names")
async def get_product_names():
    """Get all product names"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT id, name FROM products ORDER BY name")
            products = cursor.fetchall()
            return {"products": [dict(product) for product in products]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/products")
async def get_products(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    brand: Optional[str] = None
):
    """Get products with optional filtering and pagination"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Build query with optional brand filter
            base_query = "SELECT * FROM products"
            count_query = "SELECT COUNT(*) FROM products"
            
            if brand:
                base_query += " WHERE brand ILIKE %s"
                count_query += " WHERE brand ILIKE %s"
                params = [f"%{brand}%"]
            else:
                params = []
            
            # Get total count
            cursor.execute(count_query, params)
            total = cursor.fetchone()[0]
            
            # Get products with pagination
            base_query += " ORDER BY name LIMIT %s OFFSET %s"
            cursor.execute(base_query, params + [limit, offset])
            products = cursor.fetchall()
            
            return {
                "products": [dict(product) for product in products],
                "total": total,
                "limit": limit,
                "offset": offset
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/{product_id}")
async def get_product(product_id: int):
    """Get a specific product by ID"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
            product = cursor.fetchone()
            
            if not product:
                raise HTTPException(status_code=404, detail="Product not found")
            
            return {"product": dict(product)}
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/search")
async def search_products(q: str = Query(..., min_length=2)):
    """Search products by name"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("""
                SELECT * FROM products 
                WHERE name ILIKE %s 
                ORDER BY name 
                LIMIT 20
            """, (f"%{q}%",))
            products = cursor.fetchall()
            return {"products": [dict(product) for product in products]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
