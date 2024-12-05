from src.p_url_utils import shorten, get_url, write_url
import pytest
import hashlib
import os


@pytest.fixture(scope="function")
def aws_creds():
    os.environ["AWS_ACCESS_KEY_ID"] = "test"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
    os.environ["AWS_SECURITY_TOKEN"] = "test"
    os.environ["AWS_SESSION_TOKEN"] = "test"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


url_prefix = "https://milesjphillips.com/"


class TestShortenUrl:
    def test_returns_value_error_for_invalid_urls(self):
        valids = ["www.google.com", "coda.io/product", "https://example.com/page?name=ferret"]
        invalids = [
            "cheese",
            "https:amazon.com" "www.ex ample.org",
            "http://example.com/file[1].html",
        ]
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


class GetUrl:

    def test_missing_key_raises_keyerror(self, ssm_client):
        with pytest.raises(KeyError):
            get_url("non_existent_table", ssm_client)

    def test_successful_retrieval(self, ssm_client):
        ssm_client.put_parameter(
            Name="1234",
            Value="http://hello.com",
            Type="String",
        )

        ssm_client.put_parameter(
            Name="1234",
            Value="http://hello.com",
            Type="String",
            Overwrite=True,
        )

        url = get_url("example_table", ssm_client)
        assert url == "http://hello.com"


class TestWriteUrl:

    def test_url_written_to_param_store(self, ssm_client):
        write_url("a30n4", "http://dinosaurs.com", ssm_client)
        url = get_url("a30n4", ssm_client)
        assert url == "http://dinosaurs.com"

    def test_write_timestamp_connection_error(self):
        mock_ssm_client = Mock()
        mock_ssm_client.put_parameter.side_effect = ConnectionError("Connection issue")
        with pytest.raises(ConnectionError):
            write_url("a30n4", "http://dinosaurs.com", mock_ssm_client)
