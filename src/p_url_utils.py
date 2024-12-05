from validators import url as validate_url
import hashlib


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

    return url_prefix + hashlib.md5(url.encode()).hexdigest()[:6]

def get_url():
    pass

def write_url():
    pass