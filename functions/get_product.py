import boto3

from common import resource_name, response

dynamodb = boto3.resource("dynamodb")
products = dynamodb.Table(resource_name("products"))


def handler(event, context):
    tenant_id = event["pathParameters"]["tenant_id"]
    product_id = event["pathParameters"]["product_id"]

    resp = products.get_item(Key={"tenant_id": tenant_id, "product_id": product_id})
    item: dict | None = resp.get("Item")

    if item == None:
        return response(404, {"message": "Product not found."})

    return response(200, item)
