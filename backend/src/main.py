import json
from utils import shorten, get_url, write_url


def lambda_handler(event, context):
    body = json.loads(event["body"])
    method = event["httpMethod"]
    if method == "POST":
        return {"statusCode": 200, "body": json.dumps("url successfully stored")}
