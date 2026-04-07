from fastapi import APIRouter, Response
from models.product_model import Product
from controllers.product_controller import add_product, get_all_products, update_product, delete_product

router = APIRouter(prefix="/products")

@router.post("/add")
async def add_product_route(product: Product, response: Response):
    return await add_product(product, response)

@router.get("/all")
async def get_all_products_route(response: Response):
    return await get_all_products(response)

@router.put("/update/{product_id}")
async def update_product_route(product_id: str, product: Product, response: Response):
    return await update_product(product_id, product, response)

@router.delete("/delete/{product_id}")
async def delete_product_route(product_id: str, response: Response):
    return await delete_product(product_id, response)