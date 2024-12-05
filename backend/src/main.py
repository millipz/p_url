import json
import boto3
from utils import shorten, get_url, write_url

PATH = "/testpath/"

def lambda_handler(event, context):
    body = json.loads(event["body"])
    print(body)
    method = event["httpMethod"]
    ssm_client = boto3.client("ssm")
    if method == "POST":
        url = body["url"]
        short = shorten(url)
        write_url(short, url, PATH, ssm_client)
        response = {
            "success": True,
            "short_url": PATH + short,
            "message": "url successfully stored"
        }
        return {"statusCode": 201, "body": json.dumps(response)}
    if method == "GET":
        key = body["key"]
        long = get_url(key, PATH, ssm_client)
        response = {
            "success": True,
            "long_url": long,
            "message": "url successfully retrieved"
        }
        return {"statusCode": 200, "body": json.dumps(response)}

