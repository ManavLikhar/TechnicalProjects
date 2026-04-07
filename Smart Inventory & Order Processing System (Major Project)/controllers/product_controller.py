from models.product_model import Product
from dbconnect import products_collection
from bson import ObjectId
from bson.errors import InvalidId

# Add product
async def add_product(product: Product, response):
    try:
        # Check if product already exists
        existing_product = await products_collection.find_one({"name": product.name})
        if existing_product:
            response.status_code = 400
            return {"message": "Product already exists"}
        # Insert product
        else:
            await products_collection.insert_one(product.dict())
            response.status_code = 201
            return {"message": "Product added successfully"}
    except Exception as e:
        response.status_code = 500
        return {"message": str(e)}

# Get all products    
async def get_all_products(response):
    try:
        products = []
        async for product in products_collection.find():
            product["_id"] = str(product["_id"])
            products.append(product)
        response.status_code = 200
        return products 
    except Exception as e:
        response.status_code = 500
        return {"message": str(e)}

# Update product
async def update_product(product_id: str, product: Product, response):
    try:
        try:
            oid = ObjectId(product_id)
        except InvalidId:
            response.status_code = 400
            return {"message": "Invalid Product ID"}
        result = await products_collection.update_one({"_id": oid}, {"$set": product.dict()})
        if result.matched_count == 0:
            response.status_code = 404
            return {"message": "Product not found"}
        response.status_code = 200
        return {"message": "Product updated successfully"}
    except Exception as e:
        response.status_code = 500
        return {"message": str(e)}

# Delete product
async def delete_product(product_id: str, response):
    try:
        try:
            oid = ObjectId(product_id)
        except InvalidId:
            response.status_code = 400
            return {"message": "Invalid Product ID"}
        result = await products_collection.delete_one({"_id": oid})
        if result.deleted_count == 0:
            response.status_code = 404
            return {"message": "Product not found"}
        response.status_code = 200
        return {"message": "Product deleted successfully"}
    except Exception as e:
        response.status_code = 500
        return {"message": str(e)}