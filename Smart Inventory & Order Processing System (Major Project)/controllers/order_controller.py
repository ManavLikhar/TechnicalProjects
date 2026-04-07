from models.order_model import Order
from dbconnect import orders_collection, products_collection
from datetime import datetime

# Place order
async def place_order(order: Order, username: str, response):
    try:
        if order.quantity <= 0:
            response.status_code = 400
            return {"message": "Quantity must be greater than 0"}

        # Atomically check stock and update
        result = await products_collection.update_one(
            {"name": order.product_name, "stock": {"$gte": order.quantity}},
            {"$inc": {"stock": -order.quantity}}
        )
        
        if result.modified_count == 0:
            product = await products_collection.find_one({"name": order.product_name})
            if not product:
                response.status_code = 404
                return {"message": "Product not found"}
            response.status_code = 400
            return {"message": "Insufficient stock for the product"}
        
        # Insert order
        order_data = {
            "product_name": order.product_name,
            "quantity": order.quantity,
            "username": username,
            "order_date": datetime.utcnow()
        }

        await orders_collection.insert_one(order_data)
        response.status_code = 201
        return {"message": "Order placed successfully"}
    except Exception as e:
        response.status_code = 500
        return {"message": str(e)}

# Get all orders
async def get_all_orders(response):
    try:
        orders = []
        async for order in orders_collection.find():
            order["_id"] = str(order["_id"])
            orders.append(order)
        response.status_code = 200
        return orders
    except Exception as e:
        response.status_code = 500
        return {"message": str(e)}