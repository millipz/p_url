from src.p_url_utils import shorten
import pytest
import hashlib

url_prefix = "https://milesjphillips.com/"

class TestShortenUrl:
    def test_returns_value_error_for_invalid_urls(self):
        valids = ["www.google.com", "coda.io/product", "https://example.com/page?name=ferret"]
        invalids = ["cheese", "https:amazon.com" "www.ex ample.org", "http://example.com/file[1].html"]
        [shorten(url) for url in valids]
        for url in invalids:
            with pytest.raises(ValueError):
                shorten(url)
    
    def test_url_is_prefixed_correctly(self):
        url = "www.perspectum.com"
        short_url = shorten(url)
        assert short_url.startswith(url_prefix)

    def test_short_url_is_checksum_prefix(self):
        url = "https://modular.com/page?name=befaco"
        short_url = shorten(url)
        checksum = hashlib.md5(url.encode()).hexdigest() 
        expected_short_url = checksum[:6]
        assert short_url == url_prefix + expected_short_url