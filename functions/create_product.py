import base64
import uuid
from decimal import Decimal
from typing import Optional

import boto3
from pydantic import BaseModel

from common import parse_body, resource_name, response
from common.images import product_image_key
from schemas import Product

BUCKET_NAME = resource_name("product-images")


class CreateProductRequest(BaseModel):
    name: str
    price: Decimal
    image: Optional[str] = None


dynamodb = boto3.resource("dynamodb")
s3 = boto3.resource("s3")

products = dynamodb.Table(resource_name("products"))
product_images = s3.Bucket(resource_name("product-images"))


def handler(event, context):
    tenant_id = event["pathParameters"]["tenant_id"]

    data, err = parse_body(CreateProductRequest, event)
    if err != None:
        return err

    assert data != None

    new_product = Product(
        tenant_id=tenant_id,
        product_id=str(uuid.uuid4()),
        name=data.name,
        price=data.price,
    )

    if data.image != None:
        key = product_image_key(new_product)

        product_images.Object(key).put(Body=base64.b64decode(data.image))
        new_product.image_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{key}"

    products.put_item(Item=new_product.model_dump())
    return response(201, new_product)
