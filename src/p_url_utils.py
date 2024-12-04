from validators import url

def shorten(url: str) -> str:
    """Shortens url using md5 hash

    Args:
        url (str): url to shorten

    Returns:
        str: the shortened url

    Raises:
        ValueError: for invalid url.
    """

