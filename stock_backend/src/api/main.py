from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field
from typing import List
import uuid

app = FastAPI(
    title="Stock Management API",
    version="0.1.0",
    description="API for public browsing of categories and products in stock management system.",
    openapi_tags=[
        {"name": "Public", "description": "Endpoints for public browsing of categories and products"},
        {"name": "Admin", "description": "Admin authentication and management endpoints (protected)"},
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- In-memory admin authentication/session logic ---
# Hardcoded admin credentials (for demonstration: in production, use env variables/storage)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin"

# In-memory token/session store: token -> username
ADMIN_SESSIONS = {}

class LoginRequest(BaseModel):
    username: str = Field(..., description="Admin username")
    password: str = Field(..., description="Admin password")

class LoginResponse(BaseModel):
    access_token: str = Field(..., description="Bearer token for admin sessions")
    token_type: str = Field(default="bearer", description="Type of token (bearer)")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# PUBLIC_INTERFACE
def authenticate_admin_token(token: str = Depends(oauth2_scheme)) -> str:
    """
    Dependency to authenticate an admin (bearer token) for protected endpoints.

    Args:
        token (str): Bearer token from Authorization header

    Raises:
        HTTPException: 401 if token invalid or expired

    Returns:
        str: Username if valid token, raises HTTPException otherwise
    """
    if token in ADMIN_SESSIONS:
        return ADMIN_SESSIONS[token]
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired admin authentication token.",
        headers={"WWW-Authenticate": "Bearer"},
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

# --- ADMIN AUTH: /login POST endpoint ---
# PUBLIC_INTERFACE
@app.post(
    "/login",
    response_model=LoginResponse,
    tags=["Admin"],
    summary="Admin login (in-memory demo)",
    description="Authenticate admin via username and password, returns a bearer token for session-based access to protected endpoints.",
    responses={
        200: {"description": "Login successful, returns token"},
        401: {"description": "Invalid credentials"},
    },
)
def admin_login(data: LoginRequest):
    """
    Authenticates an admin with hardcoded credentials and returns a bearer token (in-memory).
    - Username and password must match the system's hardcoded values.
    - On success, generates a UUID4 bearer token and stores it in memory.

    Args:
        data (LoginRequest): JSON body, must include username and password

    Returns:
        LoginResponse with access token (bearer)
    """
    if data.username == ADMIN_USERNAME and data.password == ADMIN_PASSWORD:
        # Issue new random token
        token = str(uuid.uuid4())
        ADMIN_SESSIONS[token] = data.username
        return LoginResponse(access_token=token, token_type="bearer")
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
    )

# Expanded hard-coded data for scroll/organization testing (10 categories, 50+ products)
CATEGORIES = [
    Category(id=1, name="Beverages"),
    Category(id=2, name="Snacks"),
    Category(id=3, name="Meat"),
    Category(id=4, name="Produce"),
    Category(id=5, name="Dairy"),
    Category(id=6, name="Bakery"),
    Category(id=7, name="Frozen Foods"),
    Category(id=8, name="Canned Goods"),
    Category(id=9, name="Condiments"),
    Category(id=10, name="Cleaning Supplies")
]

PRODUCTS = [
    # Beverages
    Product(id=1, name="Apple Juice", category_id=1, image_url="https://via.placeholder.com/150?text=Apple+Juice", quantity=10),
    Product(id=2, name="Orange Soda", category_id=1, image_url="https://via.placeholder.com/150?text=Orange+Soda", quantity=30),
    Product(id=3, name="Bottled Water", category_id=1, image_url="https://via.placeholder.com/150?text=Bottled+Water", quantity=50),
    Product(id=4, name="Lemonade", category_id=1, image_url="https://via.placeholder.com/150?text=Lemonade", quantity=12),
    Product(id=5, name="Iced Tea", category_id=1, image_url="https://via.placeholder.com/150?text=Iced+Tea", quantity=8),
    # Snacks
    Product(id=6, name="Cookies", category_id=2, image_url="https://via.placeholder.com/150?text=Cookies", quantity=15),
    Product(id=7, name="Potato Chips", category_id=2, image_url="https://via.placeholder.com/150?text=Potato+Chips", quantity=25),
    Product(id=8, name="Pretzels", category_id=2, image_url="https://via.placeholder.com/150?text=Pretzels", quantity=7),
    Product(id=9, name="Popcorn", category_id=2, image_url="https://via.placeholder.com/150?text=Popcorn", quantity=30),
    Product(id=10, name="Peanuts", category_id=2, image_url="https://via.placeholder.com/150?text=Peanuts", quantity=22),
    # Meat
    Product(id=11, name="Chicken Breast", category_id=3, image_url="https://via.placeholder.com/150?text=Chicken+Breast", quantity=14),
    Product(id=12, name="Beef Steak", category_id=3, image_url="https://via.placeholder.com/150?text=Beef+Steak", quantity=6),
    Product(id=13, name="Turkey Slices", category_id=3, image_url="https://via.placeholder.com/150?text=Turkey+Slices", quantity=16),
    Product(id=14, name="Bacon", category_id=3, image_url="https://via.placeholder.com/150?text=Bacon", quantity=8),
    Product(id=15, name="Ham", category_id=3, image_url="https://via.placeholder.com/150?text=Ham", quantity=9),
    # Produce
    Product(id=16, name="Bananas", category_id=4, image_url="https://via.placeholder.com/150?text=Bananas", quantity=13),
    Product(id=17, name="Apples", category_id=4, image_url="https://via.placeholder.com/150?text=Apples", quantity=17),
    Product(id=18, name="Carrots", category_id=4, image_url="https://via.placeholder.com/150?text=Carrots", quantity=28),
    Product(id=19, name="Tomatoes", category_id=4, image_url="https://via.placeholder.com/150?text=Tomatoes", quantity=19),
    Product(id=20, name="Lettuce", category_id=4, image_url="https://via.placeholder.com/150?text=Lettuce", quantity=11),
    # Dairy
    Product(id=21, name="Milk", category_id=5, image_url="https://via.placeholder.com/150?text=Milk", quantity=10),
    Product(id=22, name="Cheese", category_id=5, image_url="https://via.placeholder.com/150?text=Cheese", quantity=6),
    Product(id=23, name="Yogurt", category_id=5, image_url="https://via.placeholder.com/150?text=Yogurt", quantity=8),
    Product(id=24, name="Butter", category_id=5, image_url="https://via.placeholder.com/150?text=Butter", quantity=5),
    Product(id=25, name="Eggs (Dozen)", category_id=5, image_url="https://via.placeholder.com/150?text=Eggs", quantity=31),
    # Bakery
    Product(id=26, name="White Bread", category_id=6, image_url="https://via.placeholder.com/150?text=White+Bread", quantity=20),
    Product(id=27, name="Croissant", category_id=6, image_url="https://via.placeholder.com/150?text=Croissant", quantity=10),
    Product(id=28, name="Bagel", category_id=6, image_url="https://via.placeholder.com/150?text=Bagel", quantity=15),
    Product(id=29, name="Multigrain Loaf", category_id=6, image_url="https://via.placeholder.com/150?text=Multigrain+Loaf", quantity=8),
    Product(id=30, name="Donuts", category_id=6, image_url="https://via.placeholder.com/150?text=Donuts", quantity=13),
    # Frozen Foods
    Product(id=31, name="Frozen Pizza", category_id=7, image_url="https://via.placeholder.com/150?text=Frozen+Pizza", quantity=8),
    Product(id=32, name="Ice Cream", category_id=7, image_url="https://via.placeholder.com/150?text=Ice+Cream", quantity=23),
    Product(id=33, name="Waffles", category_id=7, image_url="https://via.placeholder.com/150?text=Waffles", quantity=10),
    Product(id=34, name="Vegetable Mix", category_id=7, image_url="https://via.placeholder.com/150?text=Vegetable+Mix", quantity=16),
    Product(id=35, name="French Fries", category_id=7, image_url="https://via.placeholder.com/150?text=French+Fries", quantity=21),
    # Canned Goods
    Product(id=36, name="Canned Beans", category_id=8, image_url="https://via.placeholder.com/150?text=Canned+Beans", quantity=27),
    Product(id=37, name="Canned Corn", category_id=8, image_url="https://via.placeholder.com/150?text=Canned+Corn", quantity=18),
    Product(id=38, name="Tuna", category_id=8, image_url="https://via.placeholder.com/150?text=Tuna", quantity=20),
    Product(id=39, name="Tomato Soup", category_id=8, image_url="https://via.placeholder.com/150?text=Tomato+Soup", quantity=12),
    Product(id=40, name="Chili", category_id=8, image_url="https://via.placeholder.com/150?text=Chili", quantity=8),
    # Condiments
    Product(id=41, name="Ketchup", category_id=9, image_url="https://via.placeholder.com/150?text=Ketchup", quantity=14),
    Product(id=42, name="Mayonnaise", category_id=9, image_url="https://via.placeholder.com/150?text=Mayonnaise", quantity=6),
    Product(id=43, name="Mustard", category_id=9, image_url="https://via.placeholder.com/150?text=Mustard", quantity=11),
    Product(id=44, name="Soy Sauce", category_id=9, image_url="https://via.placeholder.com/150?text=Soy+Sauce", quantity=5),
    Product(id=45, name="BBQ Sauce", category_id=9, image_url="https://via.placeholder.com/150?text=BBQ+Sauce", quantity=8),
    # Cleaning Supplies
    Product(id=46, name="Detergent", category_id=10, image_url="https://via.placeholder.com/150?text=Detergent", quantity=10),
    Product(id=47, name="Sponge", category_id=10, image_url="https://via.placeholder.com/150?text=Sponge", quantity=18),
    Product(id=48, name="Glass Cleaner", category_id=10, image_url="https://via.placeholder.com/150?text=Glass+Cleaner", quantity=11),
    Product(id=49, name="Disinfectant", category_id=10, image_url="https://via.placeholder.com/150?text=Disinfectant", quantity=12),
    Product(id=50, name="Broom", category_id=10, image_url="https://via.placeholder.com/150?text=Broom", quantity=4),
    # More for robustness
    Product(id=51, name="Herbal Tea", category_id=1, image_url="https://via.placeholder.com/150?text=Herbal+Tea", quantity=12),
    Product(id=52, name="Granola Bar", category_id=2, image_url="https://via.placeholder.com/150?text=Granola+Bar", quantity=21),
    Product(id=53, name="Salami", category_id=3, image_url="https://via.placeholder.com/150?text=Salami", quantity=10)
]

@app.get("/", tags=["Public"])
def health_check():
    """Health check endpoint for the Stock Management API."""
    return {"message": "Healthy"}

# To protect an endpoint for admin, add: @app.get(..., dependencies=[Depends(authenticate_admin_token)], tags=["Admin"])
# Example for admin-only usage (uncomment for protected usage):
# @app.get("/admin/protected", tags=["Admin"], dependencies=[Depends(authenticate_admin_token)])
# def admin_only():
#     return {"msg": "Secret admin data"}

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
