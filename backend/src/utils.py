from validators import url as validate_url
import hashlib
import botocore.exceptions


def shorten(url: str) -> str:
    """Shortens url using md5 hash

    Args:
        url (str): url to shorten

    Returns:
        str: the shortened url

    Raises:
        ValueError: for invalid url.
    """

    url_prefix = "https://milesjphillips.com/"

    print(f"running validation on {url}")
    if not validate_url(url):
        url = "http://" + url
        if not validate_url(url):
            raise ValueError

    return url_prefix + hashlib.md5(url.encode(), usedforsecurity=False).hexdigest()[:6]


def get_url(key: str, ssm_client) -> str:
    """get url stored in AWS parameter store by key

    Args:
        key (str): key
        client (boto3 SSM Client)

    Raises:
        KeyError: key does not exist
        ConnectionError : connection issue to parameter store

    Returns:
        str: full url
    """
    try:
        response = ssm_client.get_parameter(Name=(key))
    except ssm_client.exceptions.ParameterNotFound:
        raise KeyError
    return response["Parameter"]["Value"]


def write_url(key, url, ssm_client):
    """wites url to AWS parameter store with key

    Args:
        key (str): key
        url (str): url to write
        client (boto3 SSM Client)

    Raises:
        ConnectionError : connection issue to parameter store

    Returns:
        None
    """
    try:
        ssm_client.put_parameter(
            Name=key,
            Type="String",
            Description="url stored by p_url service",
            Value=url,
            Overwrite=True,
        )
    except botocore.exceptions.ClientError as e:
        raise ConnectionError(f"url could not be written: {e}")
