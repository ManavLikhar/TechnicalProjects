from pydantic import BaseModel

class Order(BaseModel):

    product_name: str
    quantity: int