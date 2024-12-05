import json
import boto3
from utils import shorten, get_url, write_url


def lambda_handler(event, context):
    body = json.loads(event["body"])
    print(body)
    method = event["httpMethod"]
    ssm_client = boto3.client("ssm")
    if method == "POST":
        url = body["url"]
        # try:
        short = shorten(url)
        write_url(short, url, ssm_client)
        return {"statusCode": 200, "body": json.dumps("url successfully stored")}
        # except Exception as e:
        #     return {"statusCode": 500, "body": e}
    if method == "GET":
        key = body["key"]
        # try:
        get_url(key, ssm_client)
        # except Exception as e:
        #     return {"statusCode": 500, "body": e}
