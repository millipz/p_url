from src.p_url_utils import shorten
import pytest

class TestShortenUrl:
    def test_returns_value_error_for_invalid_urls(self):
        valids = ["www.google.com", "coda.io/product", "https://example.com/page?name=ferret"]
        invalids = ["cheese", "https:amazon.com" "www.ex ample.org", "http://example.com/file[1].html"]
        [shorten(url) for url in valids]
        for url in invalids:
            with pytest.raises(ValueError):
                shorten(url)
        