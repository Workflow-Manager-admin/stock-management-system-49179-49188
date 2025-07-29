"""Utility helpers for in-memory admin authentication and data storage/ID generation."""

import uuid
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

# Demo, unsafe values for demonstration only. Use secure vault/env in prod!
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin"
ADMIN_SESSIONS = {}  # token: username

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

# PUBLIC_INTERFACE
def generate_admin_token(username: str) -> str:
    """Creates a session, returns a random token and persists this session."""
    token = str(uuid.uuid4())
    ADMIN_SESSIONS[token] = username
    return token

# In-memory data for categories and products (to be imported by main)
def load_initial_categories(models_module) -> list:
    """Return an initial list of demo categories."""
    Category = models_module.Category
    return [
        Category(id=1, name="Beverages"),
        Category(id=2, name="Snacks"),
        Category(id=3, name="Meat"),
        Category(id=4, name="Produce"),
        Category(id=5, name="Dairy"),
        Category(id=6, name="Bakery"),
        Category(id=7, name="Frozen Foods"),
        Category(id=8, name="Canned Goods"),
        Category(id=9, name="Condiments"),
        Category(id=10, name="Cleaning Supplies"),
    ]

def load_initial_products(models_module) -> list:
    """Return an initial list of demo products."""
    Product = models_module.Product
    # No dependency on CATEGORIES at function definition time
    return [
        Product(id=1, name="Apple Juice", category_id=1, image_url="https://via.placeholder.com/150?text=Apple+Juice", quantity=10),
        Product(id=2, name="Orange Soda", category_id=1, image_url="https://via.placeholder.com/150?text=Orange+Soda", quantity=30),
        Product(id=3, name="Bottled Water", category_id=1, image_url="https://via.placeholder.com/150?text=Bottled+Water", quantity=50),
        Product(id=4, name="Lemonade", category_id=1, image_url="https://via.placeholder.com/150?text=Lemonade", quantity=12),
        Product(id=5, name="Iced Tea", category_id=1, image_url="https://via.placeholder.com/150?text=Iced+Tea", quantity=8),
        Product(id=6, name="Cookies", category_id=2, image_url="https://via.placeholder.com/150?text=Cookies", quantity=15),
        Product(id=7, name="Potato Chips", category_id=2, image_url="https://via.placeholder.com/150?text=Potato+Chips", quantity=25),
        Product(id=8, name="Pretzels", category_id=2, image_url="https://via.placeholder.com/150?text=Pretzels", quantity=7),
        Product(id=9, name="Popcorn", category_id=2, image_url="https://via.placeholder.com/150?text=Popcorn", quantity=30),
        Product(id=10, name="Peanuts", category_id=2, image_url="https://via.placeholder.com/150?text=Peanuts", quantity=22),
        Product(id=11, name="Chicken Breast", category_id=3, image_url="https://via.placeholder.com/150?text=Chicken+Breast", quantity=14),
        Product(id=12, name="Beef Steak", category_id=3, image_url="https://via.placeholder.com/150?text=Beef+Steak", quantity=6),
        Product(id=13, name="Turkey Slices", category_id=3, image_url="https://via.placeholder.com/150?text=Turkey+Slices", quantity=16),
        Product(id=14, name="Bacon", category_id=3, image_url="https://via.placeholder.com/150?text=Bacon", quantity=8),
        Product(id=15, name="Ham", category_id=3, image_url="https://via.placeholder.com/150?text=Ham", quantity=9),
        Product(id=16, name="Bananas", category_id=4, image_url="https://via.placeholder.com/150?text=Bananas", quantity=13),
        Product(id=17, name="Apples", category_id=4, image_url="https://via.placeholder.com/150?text=Apples", quantity=17),
        Product(id=18, name="Carrots", category_id=4, image_url="https://via.placeholder.com/150?text=Carrots", quantity=28),
        Product(id=19, name="Tomatoes", category_id=4, image_url="https://via.placeholder.com/150?text=Tomatoes", quantity=19),
        Product(id=20, name="Lettuce", category_id=4, image_url="https://via.placeholder.com/150?text=Lettuce", quantity=11),
        Product(id=21, name="Milk", category_id=5, image_url="https://via.placeholder.com/150?text=Milk", quantity=10),
        Product(id=22, name="Cheese", category_id=5, image_url="https://via.placeholder.com/150?text=Cheese", quantity=6),
        Product(id=23, name="Yogurt", category_id=5, image_url="https://via.placeholder.com/150?text=Yogurt", quantity=8),
        Product(id=24, name="Butter", category_id=5, image_url="https://via.placeholder.com/150?text=Butter", quantity=5),
        Product(id=25, name="Eggs (Dozen)", category_id=5, image_url="https://via.placeholder.com/150?text=Eggs", quantity=31),
        Product(id=26, name="White Bread", category_id=6, image_url="https://via.placeholder.com/150?text=White+Bread", quantity=20),
        Product(id=27, name="Croissant", category_id=6, image_url="https://via.placeholder.com/150?text=Croissant", quantity=10),
        Product(id=28, name="Bagel", category_id=6, image_url="https://via.placeholder.com/150?text=Bagel", quantity=15),
        Product(id=29, name="Multigrain Loaf", category_id=6, image_url="https://via.placeholder.com/150?text=Multigrain+Loaf", quantity=8),
        Product(id=30, name="Donuts", category_id=6, image_url="https://via.placeholder.com/150?text=Donuts", quantity=13),
        Product(id=31, name="Frozen Pizza", category_id=7, image_url="https://via.placeholder.com/150?text=Frozen+Pizza", quantity=8),
        Product(id=32, name="Ice Cream", category_id=7, image_url="https://via.placeholder.com/150?text=Ice+Cream", quantity=23),
        Product(id=33, name="Waffles", category_id=7, image_url="https://via.placeholder.com/150?text=Waffles", quantity=10),
        Product(id=34, name="Vegetable Mix", category_id=7, image_url="https://via.placeholder.com/150?text=Vegetable+Mix", quantity=16),
        Product(id=35, name="French Fries", category_id=7, image_url="https://via.placeholder.com/150?text=French+Fries", quantity=21),
        Product(id=36, name="Canned Beans", category_id=8, image_url="https://via.placeholder.com/150?text=Canned+Beans", quantity=27),
        Product(id=37, name="Canned Corn", category_id=8, image_url="https://via.placeholder.com/150?text=Canned+Corn", quantity=18),
        Product(id=38, name="Tuna", category_id=8, image_url="https://via.placeholder.com/150?text=Tuna", quantity=20),
        Product(id=39, name="Tomato Soup", category_id=8, image_url="https://via.placeholder.com/150?text=Tomato+Soup", quantity=12),
        Product(id=40, name="Chili", category_id=8, image_url="https://via.placeholder.com/150?text=Chili", quantity=8),
        Product(id=41, name="Ketchup", category_id=9, image_url="https://via.placeholder.com/150?text=Ketchup", quantity=14),
        Product(id=42, name="Mayonnaise", category_id=9, image_url="https://via.placeholder.com/150?text=Mayonnaise", quantity=6),
        Product(id=43, name="Mustard", category_id=9, image_url="https://via.placeholder.com/150?text=Mustard", quantity=11),
        Product(id=44, name="Soy Sauce", category_id=9, image_url="https://via.placeholder.com/150?text=Soy+Sauce", quantity=5),
        Product(id=45, name="BBQ Sauce", category_id=9, image_url="https://via.placeholder.com/150?text=BBQ+Sauce", quantity=8),
        Product(id=46, name="Detergent", category_id=10, image_url="https://via.placeholder.com/150?text=Detergent", quantity=10),
        Product(id=47, name="Sponge", category_id=10, image_url="https://via.placeholder.com/150?text=Sponge", quantity=18),
        Product(id=48, name="Glass Cleaner", category_id=10, image_url="https://via.placeholder.com/150?text=Glass+Cleaner", quantity=11),
        Product(id=49, name="Disinfectant", category_id=10, image_url="https://via.placeholder.com/150?text=Disinfectant", quantity=12),
        Product(id=50, name="Broom", category_id=10, image_url="https://via.placeholder.com/150?text=Broom", quantity=4),
        Product(id=51, name="Herbal Tea", category_id=1, image_url="https://via.placeholder.com/150?text=Herbal+Tea", quantity=12),
        Product(id=52, name="Granola Bar", category_id=2, image_url="https://via.placeholder.com/150?text=Granola+Bar", quantity=21),
        Product(id=53, name="Salami", category_id=3, image_url="https://via.placeholder.com/150?text=Salami", quantity=10),
    ]

def get_next_category_id(categories) -> int:
    """Helper for next ID (in-memory, autoincrement)."""
    return max((cat.id for cat in categories), default=0) + 1

def get_next_product_id(products) -> int:
    """Helper for next ID (in-memory, autoincrement)."""
    return max((prod.id for prod in products), default=0) + 1
