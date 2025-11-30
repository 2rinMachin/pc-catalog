from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class Product(BaseModel):
    tenant_id: str
    product_id: str
    name: str
    price: Decimal
    image_url: Optional[str] = None
