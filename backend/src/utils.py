from validators import url as validate_url
import hashlib
import botocore.exceptions


def shorten(url: str) -> str:
    """Shortens url using md5 hash to path

    Args:
        url (str): url to shorten

    Returns:
        str: the shortened url

    Raises:
        ValueError: for invalid url.
    """

    print(f"running validation on {url}")
    if not validate_url(url):
        url = "http://" + url
        if not validate_url(url):
            raise ValueError

    return hashlib.md5(url.encode(), usedforsecurity=False).hexdigest()[:6]


def get_url(key: str, path, ssm_client) -> str:
    """get url stored in AWS parameter store by key

    Args:
        key (str): key
        path (str): path prefix
        client (boto3 SSM Client)

    Raises:
        KeyError: key does not exist
        ConnectionError : connection issue to parameter store

    Returns:
        str: full url
    """
    try:
        response = ssm_client.get_parameter(Name=(path + key))
    except ssm_client.exceptions.ParameterNotFound:
        raise KeyError
    return response["Parameter"]["Value"]


def write_url(key, url, path, ssm_client):
    """wites url to AWS parameter store with key

    Args:
        key (str): key
        url (str): url to write
        path (str): path prefix
        client (boto3 SSM Client)

    Raises:
        ConnectionError : connection issue to parameter store

    Returns:
        None
    """
    name = path + "/" + key
    print(name)
    try:
        ssm_client.put_parameter(
            Name=name,
            Type="String",
            Description="url stored by p_url service",
            Value=url,
            Overwrite=True,
        )
    except botocore.exceptions.ClientError as e:
        raise ConnectionError(f"url could not be written: {e}")
