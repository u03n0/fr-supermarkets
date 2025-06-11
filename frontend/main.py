import streamlit as st
import requests
import pandas as pd
from typing import Dict, List

# Configuration
API_BASE_URL = "http://localhost:8000"  # Change to "http://api:8000" when running in Docker

st.set_page_config(
    page_title="Product Database Explorer",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 Product Database Explorer")
st.markdown("Browse and filter scraped product data")

# Sidebar filters
st.sidebar.header("Filters")

def get_brands() -> List[str]:
    """Fetch available brands from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/brands/names")
        if response.status_code == 200:
            brands_data = response.json()["brands"]
            return [brand["brand"] for brand in brands_data]
        return []
    except:
        return []

def get_products(brand=None, limit=50, offset=0, search_term=None) -> Dict:
    """Fetch products from API"""
    try:
        if search_term:
            response = requests.get(f"{API_BASE_URL}/products/search", params={"q": search_term})
        else:
            params = {"limit": limit, "offset": offset}
            if brand and brand != "All Brands":
                params["brand"] = brand
            response = requests.get(f"{API_BASE_URL}/products/names", params=params)
        
        if response.status_code == 200:
            return response.json()
        return {"products": [], "total": 0}
    except Exception as e:
        st.error(f"Error fetching products: {e}")
        return {"products": [], "total": 0}

# Search functionality
search_term = st.text_input("🔍 Search products", placeholder="Enter product name...")

# Brand filter
brands = get_brands()
if brands:
    selected_brand = st.sidebar.selectbox(
        "Filter by Brand", 
        ["All Brands"] + brands
    )
else:
    selected_brand = "All Brands"
    st.sidebar.info("No brands available")

# Pagination controls
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    items_per_page = st.selectbox("Items per page", [10, 25, 50, 100], index=2)
with col3:
    if 'page_number' not in st.session_state:
        st.session_state.page_number = 0
    
    if st.button("Previous Page") and st.session_state.page_number > 0:
        st.session_state.page_number -= 1
    
    if st.button("Next Page"):
        st.session_state.page_number += 1

# Fetch and display products
if search_term:
    data = get_products(search_term=search_term)
    st.subheader(f"Search Results for: '{search_term}'")
else:
    offset = st.session_state.page_number * items_per_page
    data = get_products(
        brand=selected_brand if selected_brand != "All Brands" else None,
        limit=items_per_page,
        offset=offset
    )

products = data.get("products", [])
total_products = data.get("total", 0)

# Display results info
if not search_term:
    current_page = st.session_state.page_number + 1
    total_pages = (total_products + items_per_page - 1) // items_per_page
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info(f"Page {current_page} of {total_pages} | Total products: {total_products}")

# Display products
if products:
    # Convert to DataFrame for better display
    df = pd.DataFrame(products)
    
    # Format prices for better display
    if 'price' in df.columns:
        df['price'] = df['price'].apply(lambda x: f"€{x:.2f}" if x else "N/A")
    if 'unit_price' in df.columns:
        df['unit_price'] = df['unit_price'].apply(lambda x: f"€{x:.2f}" if x else "N/A")
    
    # Select columns to display
    display_columns = ['name', 'brand', 'price', 'unit_price', 'size']
    available_columns = [col for col in display_columns if col in df.columns]
    
    # Display as interactive table
    st.dataframe(
        df[available_columns],
        use_container_width=True,
        hide_index=True
    )
    
    # Detailed view section
    st.subheader("📋 Detailed Product View")
    
    # Product selector
    product_names = [f"{p['name']} (ID: {p['id']})" for p in products]
    selected_product_idx = st.selectbox(
        "Select a product for detailed view:",
        range(len(product_names)),
        format_func=lambda x: product_names[x]
    )
    
    if selected_product_idx is not None:
        selected_product = products[selected_product_idx]
        
        # Display detailed product info
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Product Details:**")
            st.write(f"**Name:** {selected_product.get('name', 'N/A')}")
            st.write(f"**Brand:** {selected_product.get('brand', 'N/A')}")
            st.write(f"**Size:** {selected_product.get('size', 'N/A')}")
            
        with col2:
            st.markdown("**Pricing:**")
            price = selected_product.get('price')
            unit_price = selected_product.get('unit_price')
            st.write(f"**Price:** €{price:.2f}" if price else "**Price:** N/A")
            st.write(f"**Unit Price:** €{unit_price:.2f}" if unit_price else "**Unit Price:** N/A")
            st.write(f"**Unit Label:** {selected_product.get('unit_label', 'N/A')}")
        
        # Promotion info
        promo = selected_product.get('promo')
        if promo:
            st.markdown("**🎯 Promotion:**")
            st.success(promo)

else:
    st.warning("No products found matching your criteria.")

# Statistics sidebar
st.sidebar.markdown("---")
st.sidebar.header("📊 Quick Stats")

try:
    # Get brand statistics
    brands_response = requests.get(f"{API_BASE_URL}/brands/names")
    if brands_response.status_code == 200:
        brands_data = brands_response.json()["brands"]
        st.sidebar.metric("Total Brands", len(brands_data))
        
        # Show top brands
        if brands_data:
            st.sidebar.markdown("**Top Brands by Product Count:**")
            sorted_brands = sorted(brands_data, key=lambda x: x['product_count'], reverse=True)[:5]
            for brand in sorted_brands:
                st.sidebar.write(f"• {brand['brand']}: {brand['product_count']}")
    
    # Get total products
    total_response = requests.get(f"{API_BASE_URL}/products/names?limit=1")
    if total_response.status_code == 200:
        total = total_response.json().get("total", 0)
        st.sidebar.metric("Total Products", total)

except:
    st.sidebar.error("Unable to load statistics")

# Footer
st.markdown("---")
st.markdown("*Data refreshed from PostgreSQL database via FastAPI*")
