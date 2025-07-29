"""FastAPI app for stock management backend (public browsing, admin management)."""

from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from src.api.models import (
    LoginRequest,
    LoginResponse,
    Category,
    Product,
    CategoryCreate,
    CategoryUpdate,
    ProductCreate,
    ProductUpdate,
)
from src.api.utils import (
    authenticate_admin_token,
    generate_admin_token,
    ADMIN_USERNAME, ADMIN_PASSWORD,
    load_initial_categories,
    load_initial_products,
    get_next_category_id,
    get_next_product_id,
)

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

# In-memory data storage
CATEGORIES: List[Category] = load_initial_categories(__import__('src.api.models', fromlist=['Category']))
PRODUCTS: List[Product] = load_initial_products(__import__('src.api.models', fromlist=['Product']))


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
        token = generate_admin_token(data.username)
        return LoginResponse(access_token=token, token_type="bearer")
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
    )


# --- PUBLIC ENDPOINTS ---

# PUBLIC_INTERFACE
@app.get("/", tags=["Public"])
def health_check():
    """Health check endpoint for the Stock Management API."""
    return {"message": "Healthy"}


# PUBLIC_INTERFACE
@app.get(
    "/categories",
    response_model=List[Category],
    tags=["Public"],
    summary="List all categories",
    description="Retrieve all stock categories (public, read-only)"
)
def list_categories():
    """Returns a list of all product categories."""
    return CATEGORIES


# PUBLIC_INTERFACE
@app.get(
    "/products",
    response_model=List[Product],
    tags=["Public"],
    summary="List all products",
    description="Retrieve all products with associated categories (public, read-only)"
)
def list_products():
    """Returns a list of all products with details."""
    return PRODUCTS


# --- ADMIN PROTECTED ENDPOINTS (CRUD: CATEGORIES) ---

# PUBLIC_INTERFACE
@app.post(
    "/categories",
    response_model=Category,
    tags=["Admin"],
    summary="Create a new category",
    description="Admin-only; create a new category.",
    dependencies=[Depends(authenticate_admin_token)],
    status_code=201
)
def create_category(data: CategoryCreate):
    """
    Add a new category (in-memory).
    - Admin only.
    """
    cat = Category(id=get_next_category_id(CATEGORIES), name=data.name)
    CATEGORIES.append(cat)
    return cat


# PUBLIC_INTERFACE
@app.put(
    "/categories/{category_id}",
    response_model=Category,
    tags=["Admin"],
    summary="Update a category",
    description="Admin-only; update an existing category (full update).",
    dependencies=[Depends(authenticate_admin_token)]
)
def update_category(category_id: int, data: CategoryCreate):
    """
    Update category (replace all fields).
    - Admin only.
    """
    for cat in CATEGORIES:
        if cat.id == category_id:
            cat.name = data.name
            return cat
    raise HTTPException(status_code=404, detail="Category not found.")


# PUBLIC_INTERFACE
@app.patch(
    "/categories/{category_id}",
    response_model=Category,
    tags=["Admin"],
    summary="Partially update a category",
    description="Admin-only; update category fields.",
    dependencies=[Depends(authenticate_admin_token)]
)
def partial_update_category(category_id: int, data: CategoryUpdate):
    """
    Partially update category fields.
    - Admin only.
    """
    for cat in CATEGORIES:
        if cat.id == category_id:
            if data.name is not None:
                cat.name = data.name
            return cat
    raise HTTPException(status_code=404, detail="Category not found.")


# PUBLIC_INTERFACE
@app.delete(
    "/categories/{category_id}",
    tags=["Admin"],
    summary="Delete a category",
    description="Admin-only; delete the specified category.",
    dependencies=[Depends(authenticate_admin_token)],
    status_code=204
)
def delete_category(category_id: int):
    """
    Delete category (admin only).
    - Also removes associated products (in-memory).
    """
    idx = next((i for i, cat in enumerate(CATEGORIES) if cat.id == category_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="Category not found.")
    CATEGORIES.pop(idx)
    # Remove all products in this category
    global PRODUCTS
    PRODUCTS = [p for p in PRODUCTS if p.category_id != category_id]
    return


# --- ADMIN PROTECTED ENDPOINTS (CRUD: PRODUCTS) ---

# PUBLIC_INTERFACE
@app.post(
    "/products",
    response_model=Product,
    tags=["Admin"],
    summary="Create a new product",
    description="Admin-only; create a new product.",
    dependencies=[Depends(authenticate_admin_token)],
    status_code=201
)
def create_product(data: ProductCreate):
    """
    Add a new product (in-memory).
    - Admin only.
    """
    if not any(cat.id == data.category_id for cat in CATEGORIES):
        raise HTTPException(status_code=400, detail="Category does not exist.")
    prod = Product(
        id=get_next_product_id(PRODUCTS),
        name=data.name,
        category_id=data.category_id,
        image_url=data.image_url,
        quantity=data.quantity
    )
    PRODUCTS.append(prod)
    return prod


# PUBLIC_INTERFACE
@app.put(
    "/products/{product_id}",
    response_model=Product,
    tags=["Admin"],
    summary="Update a product",
    description="Admin-only; update an existing product (full update).",
    dependencies=[Depends(authenticate_admin_token)]
)
def update_product(product_id: int, data: ProductCreate):
    """
    Update a product (replace all fields).
    - Admin only.
    """
    for prod in PRODUCTS:
        if prod.id == product_id:
            prod.name = data.name
            prod.category_id = data.category_id
            prod.image_url = data.image_url
            prod.quantity = data.quantity
            return prod
    raise HTTPException(status_code=404, detail="Product not found.")


# PUBLIC_INTERFACE
@app.patch(
    "/products/{product_id}",
    response_model=Product,
    tags=["Admin"],
    summary="Partially update a product",
    description="Admin-only; partial update of product fields.",
    dependencies=[Depends(authenticate_admin_token)]
)
def partial_update_product(product_id: int, data: ProductUpdate):
    """
    Partially update a product (admin only).
    """
    for prod in PRODUCTS:
        if prod.id == product_id:
            if data.name is not None:
                prod.name = data.name
            if data.category_id is not None:
                if not any(cat.id == data.category_id for cat in CATEGORIES):
                    raise HTTPException(status_code=400, detail="Category does not exist.")
                prod.category_id = data.category_id
            if data.image_url is not None:
                prod.image_url = data.image_url
            if data.quantity is not None:
                prod.quantity = data.quantity
            return prod
    raise HTTPException(status_code=404, detail="Product not found.")


# PUBLIC_INTERFACE
@app.delete(
    "/products/{product_id}",
    tags=["Admin"],
    summary="Delete a product",
    description="Admin-only; delete specified product.",
    dependencies=[Depends(authenticate_admin_token)],
    status_code=204
)
def delete_product(product_id: int):
    """
    Delete product (admin only).
    """
    idx = next((i for i, prod in enumerate(PRODUCTS) if prod.id == product_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="Product not found.")
    PRODUCTS.pop(idx)
    return
