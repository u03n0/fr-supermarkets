from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
#from backend.database import get_db_connection
from database import get_db_connection

router = APIRouter(prefix="/brands", tags=["brands"])
# ... rest of your routes




@router.get("/names")
async def get_brand_names():
    """Get all brand names"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT  distinct(brand) FROM products ORDER BY brand")
            brands = cursor.fetchall()
            return {"brands": [dict(brand) for brand in brands]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


