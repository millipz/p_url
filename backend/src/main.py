import json
import boto3
from src.utils import shorten, get_url, write_url

PATH = "/testpath"


def lambda_handler(event, context):
    print(event)
    method = event["httpMethod"]
    ssm_client = boto3.client("ssm")

    # CORS headers
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
    }

    if method == "OPTIONS":
        return {"statusCode": 200, "headers": headers, "body": ""}

    try:
        if method == "POST":
            body = json.loads(event["body"])
            url = body["url"]
            short = shorten(url)
            write_url(short, url, PATH, ssm_client)
            response = {"success": True, "short_url": short, "message": "url successfully stored"}
            return {"statusCode": 200, "headers": headers, "body": json.dumps(response)}

        if method == "GET":
            key = event["path"]
            if not key:
                response = {"success": True, "message": "no url requested"}
                return {"statusCode": 200, "headers": headers, "body": json.dumps(response)}
            long = get_url(key, PATH, ssm_client)
            response = {"success": True, "long_url": long, "message": "url successfully retrieved"}
            return {"statusCode": 200, "headers": headers, "body": json.dumps(response)}

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"success": False, "message": str(e)}),
        }
