from decimal import Decimal

import boto3
from pydantic import BaseModel

from common import parse_body, resource_name, response

dynamodb = boto3.resource("dynamodb")
products = dynamodb.Table(resource_name("products"))


class UpdateProductRequest(BaseModel):
    name: str
    price: Decimal


def handler(event, context):
    tenant_id = event["pathParameters"]["tenant_id"]
    product_id = event["pathParameters"]["product_id"]

    data, err = parse_body(UpdateProductRequest, event)
    if err != None:
        return err

    assert data != None

    resp = products.update_item(
        Key={"tenant_id": tenant_id, "product_id": product_id},
        UpdateExpression="""
            SET #nm = :name,
                price = :price
        """,
        ExpressionAttributeNames={"#nm": "name"},
        ExpressionAttributeValues={
            ":name": data.name,
            ":price": data.price,
        },
        ReturnValues="ALL_NEW",
    )
    return response(200, resp["Attributes"])
