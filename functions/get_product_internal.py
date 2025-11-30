import boto3

from common import resource_name

dynamodb = boto3.resource("dynamodb")
products = dynamodb.Table(resource_name("products"))


def handler(event, context):
    tenant_id = event["tenant_id"]
    product_id = event["product_id"]

    resp = products.get_item(Key={"tenant_id": tenant_id, "product_id": product_id})
    return resp.get("Item")
