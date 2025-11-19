import boto3

from common import resource_name, response
from common.images import product_image_key
from schemas import Product

BUCKET_NAME = resource_name("product-images")

dynamodb = boto3.resource("dynamodb")
s3 = boto3.resource("s3")

products = dynamodb.Table(resource_name("products"))
product_images = s3.Bucket(resource_name("product-images"))


def handler(event, context):
    tenant_id = event["pathParameters"]["tenant_id"]
    product_id = event["pathParameters"]["product_id"]

    resp = products.get_item(Key={"tenant_id": tenant_id, "product_id": product_id})
    item: dict | None = resp.get("Item")

    if item == None:
        return response(404, {"message": "Product not found"})

    product = Product(**item)
    image_key = product_image_key(product)
    product_images.Object(image_key).delete()

    products.delete_item(Key={"tenant_id": tenant_id, "product_id": product_id})
    return response(204, None)
