from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List

app = FastAPI(
    title="Stock Management API",
    version="0.1.0",
    description="API for public browsing of categories and products in stock management system.",
    openapi_tags=[
        {"name": "Public", "description": "Endpoints for public browsing of categories and products"}
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory data structures for categories and products
class Category(BaseModel):
    """A category of products"""
    id: int = Field(..., description="Unique category ID")
    name: str = Field(..., description="Category name")

class Product(BaseModel):
    """A product in stock."""
    id: int = Field(..., description="Unique product ID")
    name: str = Field(..., description="Product name")
    category_id: int = Field(..., description="ID of associated category")
    image_url: str = Field(..., description="Image URL (placeholder for now)")
    quantity: int = Field(..., description="Quantity in stock")

# Example hard-coded data
CATEGORIES = [
    Category(id=1, name="Beverages"),
    Category(id=2, name="Snacks")
]

PRODUCTS = [
    Product(id=1, name="Apple Juice", category_id=1, image_url="https://via.placeholder.com/150?text=Apple+Juice", quantity=10),
    Product(id=2, name="Orange Soda", category_id=1, image_url="https://via.placeholder.com/150?text=Orange+Soda", quantity=30),
    Product(id=3, name="Cookies", category_id=2, image_url="https://via.placeholder.com/150?text=Cookies", quantity=15),
    Product(id=4, name="Potato Chips", category_id=2, image_url="https://via.placeholder.com/150?text=Potato+Chips", quantity=25),
]

@app.get("/", tags=["Public"])
def health_check():
    """Health check endpoint for the Stock Management API."""
    return {"message": "Healthy"}

# PUBLIC_INTERFACE
@app.get("/categories", response_model=List[Category], tags=["Public"], summary="List all categories", description="Retrieve all stock categories (public, read-only)")
def list_categories():
    """
    Returns a list of all product categories.

    Returns:
        List[Category]: List of hardcoded product categories.
    """
    return CATEGORIES

# PUBLIC_INTERFACE
@app.get("/products", response_model=List[Product], tags=["Public"], summary="List all products", description="Retrieve all products with associated categories (public, read-only)")
def list_products():
    """
    Returns a list of all products with details.

    Returns:
        List[Product]: List of hardcoded products.
    """
    return PRODUCTS
