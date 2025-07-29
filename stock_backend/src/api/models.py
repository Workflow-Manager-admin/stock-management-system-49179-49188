"""Pydantic models for stock management system (categories, products, authentication schemas)."""

from pydantic import BaseModel, Field
from typing import Optional


# PUBLIC_INTERFACE
class LoginRequest(BaseModel):
    """Request body for admin login."""
    username: str = Field(..., description="Admin username")
    password: str = Field(..., description="Admin password")


# PUBLIC_INTERFACE
class LoginResponse(BaseModel):
    """Response model for successful admin login."""
    access_token: str = Field(..., description="Bearer token for admin sessions")
    token_type: str = Field(default="bearer", description="Type of token (bearer)")


# PUBLIC_INTERFACE
class Category(BaseModel):
    """A category of products."""
    id: int = Field(..., description="Unique category ID")
    name: str = Field(..., description="Category name")


# PUBLIC_INTERFACE
class Product(BaseModel):
    """A product in stock."""
    id: int = Field(..., description="Unique product ID")
    name: str = Field(..., description="Product name")
    category_id: int = Field(..., description="ID of associated category")
    image_url: str = Field(..., description="Image URL (placeholder for now)")
    quantity: int = Field(..., description="Quantity in stock")


# Request models for create/update (admin)
# PUBLIC_INTERFACE
class CategoryCreate(BaseModel):
    """Admin: Model to create a new category."""
    name: str = Field(..., description="Category name")


# PUBLIC_INTERFACE
class CategoryUpdate(BaseModel):
    """Admin: Model for partial update of a category (fields optional)."""
    name: Optional[str] = Field(None, description="Category name (optional, update only some fields)")


# PUBLIC_INTERFACE
class ProductCreate(BaseModel):
    """Admin: Model to create a new product."""
    name: str = Field(..., description="Product name")
    category_id: int = Field(..., description="ID of associated category")
    image_url: str = Field(..., description="Image URL (placeholder for now)")
    quantity: int = Field(..., description="Quantity in stock")


# PUBLIC_INTERFACE
class ProductUpdate(BaseModel):
    """Admin: Model for partial update of a product (fields optional)."""
    name: Optional[str] = Field(None, description="Product name (optional, update only some fields)")
    category_id: Optional[int] = Field(None, description="ID of associated category (optional)")
    image_url: Optional[str] = Field(None, description="Image URL (optional)")
    quantity: Optional[int] = Field(None, description="Quantity in stock (optional)")
