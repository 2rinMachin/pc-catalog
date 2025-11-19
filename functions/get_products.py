import boto3
from boto3.dynamodb.conditions import Key

from common import resource_name, response

dynamodb = boto3.resource("dynamodb")


def handler(event, context):
    tenant_id = event["pathParameters"]["tenant_id"]

    products = dynamodb.Table(resource_name("products"))

    resp = products.query(KeyConditionExpression=Key("tenant_id").eq(tenant_id))
    products = resp["Items"]

    return response(200, products)
